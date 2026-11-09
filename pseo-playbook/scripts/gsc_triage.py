#!/usr/bin/env python3
"""Sort pages into keep / rework / consolidate / delete / needs-decision, with reasons.

Required:
  --perf-12m   Search Console Performance > Pages export for the last 12 months
               (CSV with a page/URL column, Clicks, Impressions, Position).

Optional (each one makes decisions safer):
  --perf-6m      same export for the last 6 months (used for the position test)
  --not-indexed  one or more exports from Search Console > Pages for a "not indexed" reason
                 (the reason is taken from the file name)
  --urls         full list of URLs in scope (sitemap XML, url_groups.csv, or a text list).
                 Important: performance exports leave out pages with zero impressions, so
                 without this list those pages are invisible.
  --leads        CSV of landing pages that produced leads (one row per lead, or a count column)
  --backlinks    CSV of pages with backlinks (url column + optional count column)
  --duplicates   output of near_duplicates.py (url_a, url_b, similarity)

Default rule (adjust thresholds to the site's size, see stage 3):
  delete       zero clicks and zero impressions in 12 months, no leads, no backlinks,
               and not a protected parent page (--protect)
  consolidate  weak on all three (avg position worse than 20 in 6 months, fewer than
               --min-clicks clicks, under --impressions-threshold impressions in 12 months)
               AND a near-duplicate exists to redirect to
  needs decision  weak on all three but no obvious redirect target
  rework       some signal on any measure, or a near-duplicate of a stronger page
  keep         ranking (avg position 20 or better) with at least --keep-clicks clicks
Pages with leads, the homepage, and pages passed to --protect are never deleted or
consolidated. Pass your hub and parent pages to --protect.

Note: Search Console gives an average position, not the best position, so "never in the
top 20" is approximated by "average position worse than 20".

Example:
  python gsc_triage.py --perf-12m pages_12m.csv --perf-6m pages_6m.csv \\
      --not-indexed crawled_not_indexed.csv --urls sitemap.xml \\
      --scope-prefix https://example.com/ --exclude /blog/ --out triage.csv
"""
import argparse
import csv
import os
import re
import sys
from collections import Counter, defaultdict
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from url_grouper import read_urls, slug_pattern  # noqa: E402

URL_HEADERS = {"top pages", "page", "pages", "url", "urls", "landing page", "address",
               "page url", "target url", "url_a", "entry url", "landing_page"}


def norm(u):
    u = (u or "").strip()
    u = re.sub(r"#.*$", "", u)
    return u.rstrip("/") if u.count("/") > 3 else u


def num(v):
    if v is None:
        return 0.0
    v = str(v).strip().replace(",", "").replace("%", "")
    try:
        return float(v)
    except ValueError:
        return 0.0


def read_table(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        sample = f.read(4096)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",\t;")
        except csv.Error:
            dialect = csv.excel
        rows = list(csv.DictReader(f, dialect=dialect))
    return rows


def url_col(rows, path):
    if not rows:
        return None
    cols = list(rows[0].keys())
    for c in cols:
        if c and c.strip().lower() in URL_HEADERS:
            return c
    for c in cols:
        if any(str(r.get(c, "")).startswith("http") for r in rows[:20]):
            return c
    sys.exit(f"Could not find a URL column in {path}. Columns: {cols}")


def find_col(rows, *names):
    if not rows:
        return None
    for c in rows[0].keys():
        lc = (c or "").strip().lower()
        if any(n in lc for n in names):
            return c
    return None


def load_perf(path):
    rows = read_table(path)
    uc = url_col(rows, path)
    cc, ic, pc = find_col(rows, "click"), find_col(rows, "impression"), find_col(rows, "position")
    data = {}
    for r in rows:
        u = norm(r.get(uc))
        if not u.startswith("http"):
            continue
        data[u] = {
            "clicks": num(r.get(cc)) if cc else 0,
            "impressions": num(r.get(ic)) if ic else 0,
            "position": num(r.get(pc)) if pc and str(r.get(pc, "")).strip() else None,
        }
    return data


def load_counts(path):
    rows = read_table(path)
    uc = url_col(rows, path)
    cnt_col = find_col(rows, "referring", "domains", "backlinks", "count", "leads")
    counts = defaultdict(float)
    for r in rows:
        u = norm(r.get(uc))
        if not u.startswith("http"):
            continue
        counts[u] += num(r.get(cnt_col)) if cnt_col and str(r.get(cnt_col, "")).strip() else 1
    return counts


def reason_from_filename(path):
    name = os.path.splitext(os.path.basename(path))[0].replace("_", " ").replace("-", " ").lower()
    for key, label in [("crawled", "crawled - not indexed"), ("discovered", "discovered - not indexed"),
                       ("duplicate", "duplicate"), ("noindex", "excluded by noindex"),
                       ("soft", "soft 404"), ("404", "not found (404)"), ("redirect", "page with redirect"),
                       ("canonical", "alternate canonical")]:
        if key in name:
            return label
    return name


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--perf-12m", required=True)
    ap.add_argument("--perf-6m")
    ap.add_argument("--not-indexed", nargs="*", default=[])
    ap.add_argument("--urls", nargs="*", default=[])
    ap.add_argument("--leads")
    ap.add_argument("--backlinks")
    ap.add_argument("--duplicates")
    ap.add_argument("--impressions-threshold", type=float, default=1000)
    ap.add_argument("--position-threshold", type=float, default=20)
    ap.add_argument("--min-clicks", type=float, default=3, help="clicks below this count as 'no meaningful clicks'")
    ap.add_argument("--keep-clicks", type=float, default=10)
    ap.add_argument("--scope-prefix", help="only include URLs starting with this")
    ap.add_argument("--exclude", nargs="*", default=[], help="skip URLs containing any of these strings, e.g. /blog/")
    ap.add_argument("--protect", nargs="*", default=[],
                    help="parent/hub pages that must never be deleted or redirected: URLs, or a text file of URLs")
    ap.add_argument("--out", default="triage.csv")
    a = ap.parse_args()

    p12 = load_perf(a.perf_12m)
    p6 = load_perf(a.perf_6m) if a.perf_6m else {}
    status = {}
    for path in a.not_indexed:
        reason = reason_from_filename(path)
        rows = read_table(path)
        uc = url_col(rows, path)
        for r in rows:
            u = norm(r.get(uc))
            if u.startswith("http"):
                status[u] = reason
    leads = load_counts(a.leads) if a.leads else {}
    links = load_counts(a.backlinks) if a.backlinks else {}

    universe = set(p12) | set(status)
    for path in a.urls:
        universe |= {norm(u) for u in read_urls(path)}
    if a.scope_prefix:
        universe = {u for u in universe if u.startswith(a.scope_prefix.rstrip("/"))}
    if a.exclude:
        universe = {u for u in universe if not any(x in u for x in a.exclude)}
    if not universe:
        sys.exit("No URLs in scope. Check --scope-prefix and --exclude.")

    protected = set()
    for item in a.protect:
        if os.path.isfile(item):
            protected |= {norm(u) for u in read_urls(item)}
        else:
            protected.add(norm(item))

    def strength(u):
        d = p12.get(u, {})
        return (d.get("clicks", 0), d.get("impressions", 0))

    dup_of, dup_sim = {}, {}
    if a.duplicates:
        for r in read_table(a.duplicates):
            ua, ub = norm(r.get("url_a")), norm(r.get("url_b"))
            sim = num(r.get("similarity"))
            if ua not in universe and ub not in universe:
                continue
            weaker, stronger = (ua, ub) if strength(ua) < strength(ub) else (ub, ua)
            if sim > dup_sim.get(weaker, 0):
                dup_of[weaker], dup_sim[weaker] = stronger, sim

    out = []
    for u in sorted(universe):
        d12 = p12.get(u, {"clicks": 0, "impressions": 0, "position": None})
        pos6 = p6.get(u, {}).get("position") if p6 else d12.get("position")
        clicks, impr = d12["clicks"], d12["impressions"]
        nlead, nlink = leads.get(u, 0), links.get(u, 0)
        dup = dup_of.get(u, "")
        weak_pos = pos6 is None or pos6 > a.position_threshold
        weak_clicks = clicks < a.min_clicks
        weak_impr = impr < a.impressions_threshold
        weak_all = weak_pos and weak_clicks and weak_impr
        zero_all = clicks == 0 and impr == 0
        target = ""


        if urlparse(u).path in ("", "/"):
            bucket, reason = "keep", "homepage"
        elif u in protected:
            bucket = "rework" if weak_all else "keep"
            reason = "protected parent or hub page: never delete or redirect"
        elif nlead > 0:
            bucket = "rework" if weak_all else "keep"
            reason = f"brought {int(nlead)} lead(s): never delete or redirect"
        elif zero_all and nlink == 0:
            bucket, reason = "delete", "zero clicks and zero impressions in 12 months, no leads, no backlinks"
        elif zero_all and nlink > 0:
            bucket = "consolidate" if dup else "needs decision"
            reason = f"no search activity but {int(nlink)} backlink(s): redirect to keep link value"
            target = dup
        elif weak_all and dup:
            bucket, target = "consolidate", dup
            reason = f"weak on all three measures; {dup_sim[u]:.0%} similar to a stronger page"
        elif weak_all:
            bucket = "needs decision"
            reason = "weak on all three measures, no near-duplicate found: redirect to parent hub, rework, or delete"
        elif dup:
            bucket = "rework"
            reason = f"some search signal but {dup_sim[u]:.0%} similar to a stronger page: rewrite around a distinct angle"
        elif not weak_pos and clicks >= a.keep_clicks:
            bucket, reason = "keep", "ranking in the top 20 with clicks"
        else:
            signals = [s for s, weak in (("position", weak_pos), ("clicks", weak_clicks), ("impressions", weak_impr)) if not weak]
            bucket, reason = "rework", "some signal on: " + ", ".join(signals)

        slug = u.rstrip("/").rsplit("/", 1)[-1].lower()
        out.append({
            "url": u, "pattern": slug_pattern(slug), "index_status": status.get(u, "indexed or unknown"),
            "clicks_12m": int(clicks), "impressions_12m": int(impr),
            "avg_position_6m": "" if pos6 is None else round(pos6, 1),
            "leads": int(nlead), "backlinks": int(nlink),
            "duplicate_of": dup, "similarity": f"{dup_sim[u]:.2f}" if u in dup_sim else "",
            "bucket": bucket, "reason": reason, "redirect_target": target,
            "owner_decision": "", "done": "",
        })

    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)

    c = Counter(r["bucket"] for r in out)
    print(f"\n{len(out)} pages triaged (thresholds: {int(a.impressions_threshold)} impressions, "
          f"position {int(a.position_threshold)}, {a.min_clicks:g} clicks).")
    for b in ["keep", "rework", "consolidate", "needs decision", "delete"]:
        print(f"  {b:<16} {c.get(b, 0)}")
    if not a.urls:
        print("\nWarning: no --urls list given. Pages with zero impressions are missing from performance "
              "exports, so the delete bucket is probably undercounted.")
    if not a.leads:
        print("Warning: no --leads file. Check lead sources before acting on delete or consolidate.")
    if not a.backlinks:
        print("Warning: no --backlinks file. Check backlinks before deleting pages.")
    by_pattern = defaultdict(Counter)
    for r in out:
        by_pattern[r["pattern"]][r["bucket"]] += 1
    print("\nBy slug pattern (largest groups):")
    for pat, cnt in sorted(by_pattern.items(), key=lambda kv: -sum(kv[1].values()))[:10]:
        print(f"  {pat:<28} " + ", ".join(f"{k} {v}" for k, v in cnt.most_common()))
    print(f"\nSaved: {a.out}\nReview the consolidate, needs-decision and delete buckets with the business owner, group by group.")


if __name__ == "__main__":
    main()
