#!/usr/bin/env python3
"""Group a site's URLs by folder and slug pattern.

Input: one or more XML sitemaps (or sitemap index files saved locally), or a text/CSV file
with one URL per line (first column used for CSV).

Output: a CSV with each URL, its first folder, depth, and detected slug pattern, plus a
plain-language summary printed to the screen.

Examples:
  python url_grouper.py sitemap.xml --out url_groups.csv
  python url_grouper.py sitemap-1.xml sitemap-2.xml --out url_groups.csv
  python url_grouper.py urls.txt --out url_groups.csv
"""
import argparse
import csv
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from urllib.parse import urlparse

# Common programmatic slug shapes. Order matters: first match wins.
PATTERNS = [
    ("*-vs-*", re.compile(r".+-vs-.+")),
    ("*-alternatives", re.compile(r".+-alternatives?$")),
    ("hire-*", re.compile(r"^hire-.+")),
    ("best-*", re.compile(r"^best-.+")),
    ("how-to-*", re.compile(r"^how-to-.+")),
    ("what-is-*", re.compile(r"^what-is-.+")),
    ("*-for-*", re.compile(r".+-for-.+")),
    ("*-in-*", re.compile(r".+-in-[a-z]+(-[a-z]+)?$")),
    ("*-integration(s)", re.compile(r".+-integrations?$")),
    ("*-development-services", re.compile(r".+-development-services?$")),
    ("*-development-company", re.compile(r".+-development-compan(y|ies)$")),
    ("*-development", re.compile(r".+-development$")),
    ("*-consulting", re.compile(r".+-consult(ing|ants?)$")),
    ("*-services", re.compile(r".+-services?$")),
    ("*-outsourcing", re.compile(r".+-outsourcing$")),
    ("*-developers", re.compile(r".+-developers?$")),
    ("*-software", re.compile(r".+-software$")),
    ("*-template(s)", re.compile(r".+-templates?$")),
    ("*-case-study", re.compile(r".+-case-stud(y|ies)$")),
]


def read_urls(path):
    urls = []
    if path.lower().endswith(".xml"):
        try:
            tree = ET.parse(path)
        except ET.ParseError as e:
            sys.exit(f"Could not read {path} as XML: {e}")
        for el in tree.iter():
            if el.tag.endswith("loc") and el.text:
                urls.append(el.text.strip())
        return urls
    with open(path, newline="", encoding="utf-8-sig") as f:
        if path.lower().endswith(".csv"):
            for row in csv.reader(f):
                if row and row[0].strip().startswith("http"):
                    urls.append(row[0].strip())
        else:
            for line in f:
                line = line.strip()
                if line.startswith("http"):
                    urls.append(line)
    return urls


def slug_pattern(slug):
    for name, rx in PATTERNS:
        if rx.match(slug):
            return name
    return "(other)"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", help="sitemap XML files or URL lists")
    ap.add_argument("--out", default="url_groups.csv")
    args = ap.parse_args()

    urls = []
    for p in args.inputs:
        urls.extend(read_urls(p))
    urls = list(dict.fromkeys(urls))  # de-duplicate, keep order
    if not urls:
        sys.exit("No URLs found. Check the input files.")

    sitemap_like = [u for u in urls if u.lower().endswith(".xml")]
    rows = []
    for u in urls:
        path = urlparse(u).path.strip("/")
        parts = [p for p in path.split("/") if p]
        depth = len(parts)
        folder = "(root)" if depth <= 1 else "/" + parts[0] + "/"
        slug = parts[-1].lower() if parts else "(home)"
        slug = re.sub(r"\.(html?|php|aspx?)$", "", slug)
        rows.append({
            "url": u,
            "folder": folder if depth else "(home)",
            "depth": depth,
            "slug": slug,
            "pattern": slug_pattern(slug) if depth else "(home)",
        })

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["url", "folder", "depth", "slug", "pattern"])
        w.writeheader()
        w.writerows(rows)

    total = len(rows)
    root = sum(1 for r in rows if r["folder"] == "(root)")
    print(f"\n{total} unique URLs.")
    if sitemap_like:
        print(f"Note: {len(sitemap_like)} entries are sitemap files themselves (a sitemap index). "
              "Save those child sitemaps and run them too.")
    print(f"{root} sit at root level ({root * 100 // total}%), {total - root - sum(1 for r in rows if r['folder']=='(home)')} inside folders.\n")
    print("Pages per folder:")
    for k, v in Counter(r["folder"] for r in rows).most_common(15):
        print(f"  {k:<40} {v}")
    print("\nPages per slug pattern:")
    for k, v in Counter(r["pattern"] for r in rows).most_common(20):
        print(f"  {k:<40} {v}")
    print(f"\nSaved: {args.out}")


if __name__ == "__main__":
    main()
