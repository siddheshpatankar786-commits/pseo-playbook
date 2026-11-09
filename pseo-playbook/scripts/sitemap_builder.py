#!/usr/bin/env python3
"""Build a sitemap index, one XML sitemap per section, and a matching HTML sitemap fragment.

Input CSV columns:
  url       (required) full URL of a live, indexable page
  section   (required) the group it belongs to, e.g. "solutions", "data-analytics"
  lastmod   (optional) date the content last really changed, YYYY-MM-DD
  title     (optional) link text for the HTML sitemap (defaults to the URL slug)

The XML sitemaps and the HTML sitemap use the same sections, so both tell the same story.
Files with more than 50,000 URLs are split automatically.

Example:
  python sitemap_builder.py --csv pages.csv --base https://example.com --out-dir sitemaps/
Then upload the files to the site root (or ask the developer to generate the same structure)
and submit sitemap_index.xml in Search Console.
"""
import argparse
import csv
import html
import os
import re
import sys
from collections import OrderedDict
from datetime import date

LIMIT = 50000


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "pages"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", required=True)
    ap.add_argument("--base", required=True, help="site root, e.g. https://example.com")
    ap.add_argument("--out-dir", default="sitemaps")
    a = ap.parse_args()

    base = a.base.rstrip("/")
    sections = OrderedDict()
    problems = []
    with open(a.csv, newline="", encoding="utf-8-sig") as f:
        for n, r in enumerate(csv.DictReader(f), 2):
            url, sec = (r.get("url") or "").strip(), (r.get("section") or "").strip()
            if not url.startswith("http") or not sec:
                problems.append(f"row {n}: missing url or section")
                continue
            if not url.startswith(base):
                problems.append(f"row {n}: {url} is not on {base}")
                continue
            lm = (r.get("lastmod") or "").strip()
            if lm and not re.match(r"^\d{4}-\d{2}-\d{2}", lm):
                problems.append(f"row {n}: lastmod '{lm}' is not YYYY-MM-DD, left out")
                lm = ""
            sections.setdefault(sec, []).append((url, lm, (r.get("title") or "").strip()))
    if not sections:
        sys.exit("No valid rows. " + "; ".join(problems[:5]))

    os.makedirs(a.out_dir, exist_ok=True)
    index_entries = []
    for sec, items in sections.items():
        seen, uniq = set(), []
        for it in items:
            if it[0] not in seen:
                seen.add(it[0])
                uniq.append(it)
        chunks = [uniq[i:i + LIMIT] for i in range(0, len(uniq), LIMIT)]
        for k, chunk in enumerate(chunks, 1):
            name = f"sitemap-{slugify(sec)}" + (f"-{k}" if len(chunks) > 1 else "") + ".xml"
            lines = ['<?xml version="1.0" encoding="UTF-8"?>',
                     '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
            for url, lm, _ in chunk:
                lines.append("  <url><loc>" + html.escape(url) + "</loc>" + (f"<lastmod>{lm}</lastmod>" if lm else "") + "</url>")
            lines.append("</urlset>")
            with open(os.path.join(a.out_dir, name), "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")
            newest = max((lm for _, lm, _ in chunk if lm), default="")
            index_entries.append((name, newest, len(chunk)))

    idx = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for name, newest, _ in index_entries:
        idx.append(f"  <sitemap><loc>{base}/{name}</loc>" + (f"<lastmod>{newest}</lastmod>" if newest else "") + "</sitemap>")
    idx.append("</sitemapindex>")
    with open(os.path.join(a.out_dir, "sitemap_index.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(idx) + "\n")

    frag = [f"<!-- HTML sitemap generated {date.today().isoformat()}; same sections as the XML sitemaps -->",
            '<nav aria-label="Site map">']
    for sec, items in sections.items():
        frag.append(f"  <section>\n    <h2>{html.escape(sec.replace('-', ' ').title())}</h2>\n    <ul>")
        for url, _, title in sorted(set(items), key=lambda x: (x[2] or x[0]).lower()):
            label = title or url.rstrip("/").rsplit("/", 1)[-1].replace("-", " ").capitalize()
            frag.append(f'      <li><a href="{html.escape(url)}">{html.escape(label)}</a></li>')
        frag.append("    </ul>\n  </section>")
    frag.append("</nav>")
    with open(os.path.join(a.out_dir, "html_sitemap_fragment.html"), "w", encoding="utf-8") as f:
        f.write("\n".join(frag) + "\n")

    print(f"\nBuilt {len(index_entries)} sitemap file(s) across {len(sections)} sections:")
    for name, _, n in index_entries:
        print(f"  {name:<45} {n} URLs")
    print(f"Plus sitemap_index.xml and html_sitemap_fragment.html in {a.out_dir}/")
    if problems:
        print(f"\n{len(problems)} row problem(s), first few:")
        for p in problems[:10]:
            print("  " + p)
    print("\nReminder: list only live, indexable pages, and change lastmod only when content really changes.")


if __name__ == "__main__":
    main()
