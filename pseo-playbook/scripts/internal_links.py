#!/usr/bin/env python3
"""Count how many pages link TO each page (inbound internal links) and list orphans.

Inputs (pick one):
  --inlinks FILE      a crawler's inlinks export with Source and Destination columns
                      (for example Screaming Frog: Bulk Export > Links > All Inlinks)
  --html-dir FOLDER   saved HTML pages of the site, plus --base https://yoursite.com

Optional:
  --pages FILE        the pages you care about (one URL per line). Pages in this list with
                      no inbound links are reported as orphans.
  --min N             flag pages with fewer than N linking pages (default 3)

With --html-dir, links inside nav, header, footer and aside are counted separately from
links in the page body, because a menu link on every page is not the same as a contextual
link from a relevant article.

Example:
  python internal_links.py --inlinks all_inlinks.csv --pages new_pages.txt --min 3 --out links.csv
"""
import argparse
import csv
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pagetools  # noqa: E402


def from_inlinks(path):
    body, boiler = defaultdict(set), defaultdict(set)
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        sys.exit("The inlinks file is empty.")
    cols = {c.lower(): c for c in rows[0]}
    src, dst = cols.get("source") or cols.get("from"), cols.get("destination") or cols.get("to")
    typ, pos = cols.get("type"), cols.get("link position")
    if not src or not dst:
        sys.exit(f"Need Source and Destination columns. Found: {list(rows[0])}")
    for r in rows:
        if typ and r.get(typ) and r[typ].lower() not in ("hyperlink", "ahref", "a"):
            continue
        s, d = pagetools.norm_url(r[src]), pagetools.norm_url(r[dst])
        if s == d:
            continue
        p = (r.get(pos) or "").lower() if pos else ""
        (boiler if p in ("navigation", "header", "footer", "aside", "sidebar") else body)[d].add(s)
    return body, boiler


def from_html(folder, base):
    if not base:
        sys.exit("--html-dir needs --base, for example --base https://example.com")
    body, boiler = defaultdict(set), defaultdict(set)
    pages = []
    for path, html in pagetools.read_html_dir(folder):
        page_url = pagetools.norm_url(pagetools.guess_url(path, html, base))
        pages.append(page_url)
        for href, _, in_boiler in pagetools.parse(html).links:
            internal, full = pagetools.same_site(href, page_url)
            if not internal:
                continue
            d = pagetools.norm_url(full)
            if d != page_url:
                (boiler if in_boiler else body)[d].add(page_url)
    return body, boiler, pages


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--inlinks")
    ap.add_argument("--html-dir")
    ap.add_argument("--base")
    ap.add_argument("--pages")
    ap.add_argument("--min", type=int, default=3)
    ap.add_argument("--out", default="internal_links.csv")
    a = ap.parse_args()

    crawled = []
    if a.inlinks:
        body, boiler = from_inlinks(a.inlinks)
    elif a.html_dir:
        body, boiler, crawled = from_html(a.html_dir, a.base)
    else:
        sys.exit("Give --inlinks or --html-dir.")

    targets = [pagetools.norm_url(u) for u in pagetools.read_url_list(a.pages)] if a.pages else sorted(set(body) | set(boiler) | set(crawled))
    rows = []
    for u in targets:
        b, n = body.get(u, set()), boiler.get(u, set()) - body.get(u, set())
        total = len(b | n)
        status = "orphan" if total == 0 else ("below minimum" if len(b) < a.min else "ok")
        rows.append({"url": u, "linking_pages_total": total, "from_body_text": len(b),
                     "from_menus_footer_only": len(n), "status": status,
                     "sample_sources": " | ".join(sorted(b)[:5])})
    rows.sort(key=lambda r: (r["from_body_text"], r["linking_pages_total"]))

    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    orphans = sum(r["status"] == "orphan" for r in rows)
    below = sum(r["status"] == "below minimum" for r in rows)
    print(f"\n{len(rows)} pages checked.")
    print(f"  orphans (no page links to them):        {orphans}")
    print(f"  fewer than {a.min} body-text links:          {below}")
    print(f"  ok:                                     {len(rows) - orphans - below}")
    for r in rows[:10]:
        print(f"    {r['from_body_text']:>3} body / {r['linking_pages_total']:>3} total  {r['url']}")
    print(f"\nSaved: {a.out}")
    print("Fix: add links pointing TO these pages from pages Google crawls often (stage 6, part 4).")


if __name__ == "__main__":
    main()
