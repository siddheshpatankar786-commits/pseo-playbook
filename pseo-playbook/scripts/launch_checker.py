#!/usr/bin/env python3
"""Run the stage 10 launch checks on each page and report pass / fail with reasons.

Checks: status 200, self-referencing canonical, no noindex, title and meta description
present and within length, exactly one H1, enough main text, no repeated sections, no
placeholder text, valid JSON-LD (not escaped, ideally one @graph), BreadcrumbList present,
a visible breadcrumb.

Inputs (pick one):
  --urls FILE         URLs to fetch, one per line (needs open internet)
  --html-dir FOLDER   saved HTML pages (status cannot be checked, and the canonical is shown
                      for you to confirm rather than compared, since file names are not URLs)

Example:
  python launch_checker.py --urls new_pages.txt --out launch_report.csv
"""
import argparse
import csv
import json
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pagetools  # noqa: E402

PLACEHOLDER = re.compile(r"(\bTBD\b|\bTODO\b|lorem ipsum|\[insert|\{\{|\}\}|if the layout allows|placeholder text)", re.I)


def check(url, html, status, saved_file=False):
    p = pagetools.parse(html)
    problems, warnings = [], []
    if status is not None and status != 200:
        problems.append(f"status {status}" + (" (redirect)" if 300 <= status < 400 else ""))
    if not html:
        return problems or ["no HTML returned"], warnings, {}

    canon = p.canonical.strip()
    if not canon:
        problems.append("no canonical tag")
    elif not canon.startswith("http"):
        problems.append(f"canonical is not a full URL: {canon}")
    elif saved_file:
        warnings.append(f"canonical is {canon}: confirm this is the page's own URL")
    elif pagetools.norm_url(canon) != pagetools.norm_url(url):
        problems.append(f"canonical points elsewhere: {canon}")
    if PLACEHOLDER.search(canon):
        problems.append("placeholder text in canonical")

    robots = (p.meta.get("robots", "") + " " + p.meta.get("googlebot", "")).lower()
    if "noindex" in robots:
        problems.append("noindex in meta robots")

    if not p.title:
        problems.append("no title")
    elif not 30 <= len(p.title) <= 65:
        warnings.append(f"title {len(p.title)} characters")
    desc = p.meta.get("description", "")
    if not desc:
        warnings.append("no meta description")
    elif not 110 <= len(desc) <= 165:
        warnings.append(f"meta description {len(desc)} characters")

    if len(p.h1) != 1:
        problems.append(f"{len(p.h1)} H1 tags (should be 1)")

    words = len(" ".join(p.main_text).split())
    if words < 300:
        warnings.append(f"only {words} words of main text")

    h2_rep = [h for h, n in Counter(x.lower() for x in p.h2 if x).items() if n > 1]
    long_rep = [t for t, n in Counter(t for t in p.main_text if len(t) > 80).items() if n > 1]
    if h2_rep or long_rep:
        problems.append(f"repeated sections ({len(h2_rep)} headings, {len(long_rep)} text blocks appear more than once)")

    visible = " ".join(p.text)
    m = PLACEHOLDER.search(visible)
    if m:
        problems.append(f"placeholder text on page: '{m.group(0)}'")

    types, graph, bad = set(), False, 0
    for raw in p.jsonld:
        if "&quot;" in raw:
            problems.append("JSON-LD is HTML-escaped (&quot;), search engines cannot read it")
            bad += 1
            continue
        try:
            data = json.loads(raw)
        except ValueError:
            problems.append("JSON-LD does not parse")
            bad += 1
            continue
        items = data if isinstance(data, list) else [data]
        for it in items:
            if isinstance(it, dict) and "@graph" in it:
                graph = True
                items.extend(x for x in it["@graph"] if isinstance(x, dict))
            if isinstance(it, dict):
                t = it.get("@type")
                types.update(t if isinstance(t, list) else [t])
    if not p.jsonld:
        warnings.append("no JSON-LD schema")
    elif len(p.jsonld) - bad > 1:
        warnings.append(f"{len(p.jsonld)} JSON-LD scripts (prefer one @graph)")
    elif p.jsonld and not graph and not bad:
        warnings.append("schema not in a single @graph")
    if "BreadcrumbList" not in types:
        warnings.append("no BreadcrumbList schema")

    no_jsonld = re.sub(r"<script[^>]*ld\+json[^>]*>.*?</script>", "", html, flags=re.S | re.I)
    if not re.search(r"breadcrumb", no_jsonld, re.I):
        warnings.append("no visible breadcrumb found")

    return problems, warnings, {"words": words, "schema_types": ", ".join(sorted(t for t in types if t))}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--urls")
    ap.add_argument("--html-dir")
    ap.add_argument("--out", default="launch_report.csv")
    a = ap.parse_args()

    results = []
    if a.urls:
        for u in pagetools.read_url_list(a.urls):
            code, _, html, err = pagetools.fetch(u)
            if code == 0:
                results.append((u, ["could not fetch: " + err[:120]], [], {}))
                continue
            results.append((u, *check(u, html, code)))
    elif a.html_dir:
        for path, html in pagetools.read_html_dir(a.html_dir):
            results.append((path, *check(path, html, None, saved_file=True)))
    else:
        sys.exit("Give --urls or --html-dir.")

    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["url", "result", "problems", "warnings", "main_words", "schema_types"])
        for u, probs, warns, info in results:
            w.writerow([u, "FAIL" if probs else ("CHECK" if warns else "PASS"), "; ".join(probs),
                        "; ".join(warns), info.get("words", ""), info.get("schema_types", "")])

    fails = [r for r in results if r[1]]
    checks = [r for r in results if not r[1] and r[2]]
    print(f"\n{len(results)} pages checked: {len(results) - len(fails) - len(checks)} pass, "
          f"{len(checks)} pass with warnings, {len(fails)} fail.")
    common = Counter(p.split(":")[0].split(" (")[0] for r in fails for p in r[1])
    for k, v in common.most_common(8):
        print(f"  {v:>4} x {k}")
    if any("could not fetch" in p for r in fails for p in r[1]):
        print("\nSome pages could not be fetched. If you are in the Claude.ai sandbox, save the pages "
              "as HTML and use --html-dir, or run this in Claude Code or Cowork.")
    print(f"\nSaved: {a.out}")


if __name__ == "__main__":
    main()
