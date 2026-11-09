#!/usr/bin/env python3
"""Check every row of a content sheet before publishing.

Flags missing required fields, title and description length, duplicate slugs / H1s /
meta titles / meta descriptions, badly formed slugs, placeholder text, em dashes, common
filler words, rows whose body text is too similar to another row, too few planned inbound
links, and rows without a reviewer.

Input: the content sheet exported as CSV (one tab = one CSV). Column names follow
templates/content-sheet.csv; extra columns are fine.

Example:
  python sheet_qa.py --sheet industry_pages.csv --out qa_report.csv
  python sheet_qa.py --sheet pages.csv --required slug h1 meta_title --similarity 0.75
"""
import argparse
import csv
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from near_duplicates import pairs_pure, pairs_sklearn  # noqa: E402

csv.field_size_limit(10_000_000)

DEFAULT_REQUIRED = ["slug", "h1", "meta_title", "meta_description", "breadcrumb_parent"]
NON_BODY = {"page_id", "page_type", "pillar", "status", "slug", "url", "breadcrumb_parent",
            "commercial_parent", "focus_keyword", "meta_title", "meta_description", "canonical",
            "links_up", "related_override", "inbound_links_planned", "source_notes", "reviewer",
            "qa_status", "published_date"}
PLACEHOLDER = re.compile(r"(\bTBD\b|\bTODO\b|lorem ipsum|\[insert|\{\{|\}\}|xxx|placeholder|if the layout allows|"
                         r"\[company\]|\[client\]|\[industry\]|\[keyword\])", re.I)
FILLER = ["delve", "tapestry", "testament", "seamless", "seamlessly", "cutting-edge", "game-changer",
          "unlock the power", "in today's fast-paced", "ever-evolving", "landscape of", "leverage the power",
          "robust solution", "elevate your", "harness the power", "it's important to note"]
SLUG_OK = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sheet", required=True)
    ap.add_argument("--required", nargs="*", default=DEFAULT_REQUIRED)
    ap.add_argument("--similarity", type=float, default=0.8, help="flag rows whose body text is this similar")
    ap.add_argument("--min-links", type=int, default=3)
    ap.add_argument("--out", default="qa_report.csv")
    a = ap.parse_args()

    with open(a.sheet, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        sys.exit("The sheet is empty.")
    cols = list(rows[0].keys())
    issues = []

    def add(i, sev, msg):
        r = rows[i]
        issues.append({"row": i + 2, "page_id": r.get("page_id", ""), "slug": r.get("slug", ""),
                       "severity": sev, "issue": msg})

    missing_cols = [c for c in a.required if c not in cols]
    if missing_cols:
        print(f"Note: required columns not in sheet: {', '.join(missing_cols)}")

    seen = {k: defaultdict(list) for k in ("slug", "h1", "meta_title", "meta_description")}
    for i, r in enumerate(rows):
        for c in a.required:
            if c in cols and not (r.get(c) or "").strip():
                add(i, "error", f"missing {c}")
        t, d = (r.get("meta_title") or "").strip(), (r.get("meta_description") or "").strip()
        if t and not 30 <= len(t) <= 60:
            add(i, "warning", f"meta_title is {len(t)} characters (aim for 30 to 60)")
        if d and not 120 <= len(d) <= 160:
            add(i, "warning", f"meta_description is {len(d)} characters (aim for 120 to 160)")
        slug = (r.get("slug") or "").strip()
        if slug and not SLUG_OK.match(slug):
            add(i, "error", "slug should be lowercase words joined by hyphens, no spaces, underscores or slashes")
        bp = (r.get("breadcrumb_parent") or "").strip()
        if bp and not bp.startswith("http"):
            add(i, "warning", "breadcrumb_parent should be a full URL of a live page")
        for k in seen:
            v = re.sub(r"\s+", " ", (r.get(k) or "").strip().lower())
            if v:
                seen[k][v].append(i)
        for c in cols:
            val = r.get(c) or ""
            if PLACEHOLDER.search(val) and c not in ("source_notes",):
                add(i, "error", f"placeholder text in {c}: '{PLACEHOLDER.search(val).group(0)}'")
            if c not in NON_BODY or c in ("meta_title", "meta_description", "h1"):
                if "\u2014" in val or "\u2013" in val:
                    add(i, "warning", f"em or en dash in {c}")
                low = val.lower()
                hits = [w for w in FILLER if w in low]
                if hits:
                    add(i, "warning", f"filler wording in {c}: {', '.join(hits)}")
        if "inbound_links_planned" in cols:
            try:
                if int(float(r.get("inbound_links_planned") or 0)) < a.min_links:
                    add(i, "warning", f"fewer than {a.min_links} inbound links planned")
            except ValueError:
                add(i, "warning", "inbound_links_planned is not a number")
        if "reviewer" in cols and not (r.get("reviewer") or "").strip():
            add(i, "info", "no reviewer signed off yet")

    for k, groups in seen.items():
        for v, idxs in groups.items():
            if len(idxs) > 1:
                for i in idxs:
                    others = ", ".join(str(j + 2) for j in idxs if j != i)
                    add(i, "error", f"duplicate {k} (same as row {others})")

    body_cols = [c for c in cols if c not in NON_BODY]
    texts = [" ".join((r.get(c) or "") for c in body_cols) for r in rows]
    valid = [i for i, t in enumerate(texts) if len(t.split()) >= 30]
    if len(valid) >= 2:
        sub = [texts[i] for i in valid]
        try:
            pairs = pairs_sklearn(sub, a.similarity)
        except ImportError:
            pairs = pairs_pure(sub, a.similarity)
        for x, y, s in pairs:
            i, j = valid[x], valid[y]
            add(i, "error", f"body text {s:.0%} similar to row {j + 2}: differentiate the angle")
            add(j, "error", f"body text {s:.0%} similar to row {i + 2}: differentiate the angle")

    issues.sort(key=lambda x: (x["row"], {"error": 0, "warning": 1, "info": 2}[x["severity"]]))
    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["row", "page_id", "slug", "severity", "issue"])
        w.writeheader()
        w.writerows(issues)

    err_rows = {x["row"] for x in issues if x["severity"] == "error"}
    print(f"\n{len(rows)} rows checked.")
    print(f"  rows with errors (do not publish yet): {len(err_rows)}")
    print(f"  warnings: {sum(x['severity'] == 'warning' for x in issues)}")
    print(f"  rows ready: {len(rows) - len(err_rows)}")
    for x in [x for x in issues if x["severity"] == "error"][:10]:
        print(f"    row {x['row']}: {x['issue']}")
    print(f"\nSaved: {a.out}")


if __name__ == "__main__":
    main()
