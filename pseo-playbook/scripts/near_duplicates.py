#!/usr/bin/env python3
"""Find pages whose main text is so similar that Google may treat them as duplicates.

Text inside nav, header, footer, aside and forms is ignored, so shared menus do not inflate
the score. Similarity is cosine similarity of word and word-pair counts: 1.0 means
identical wording, 0.8 and above usually means "the same page with a few words swapped".

Inputs (pick one):
  --html-dir FOLDER   saved HTML pages (Save Page As, or a crawler's HTML export)
  --csv FILE          CSV with columns url,text
  --urls FILE         text file of URLs to fetch (needs open internet)

Outputs:
  --out FILE          pairs at or above the threshold (url_a, url_b, similarity)
  --clusters FILE     groups of pages connected by those pairs (default: <out>_clusters.csv)

Example:
  python near_duplicates.py --html-dir pages/ --threshold 0.8 --out dupes.csv
"""
import argparse
import csv
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pagetools  # noqa: E402

csv.field_size_limit(10_000_000)


def load(args):
    docs = []
    if args.html_dir:
        for path, html in pagetools.read_html_dir(args.html_dir):
            p = pagetools.parse(html)
            docs.append((pagetools.guess_url(path, html, args.base), " ".join(p.main_text)))
    elif args.csv:
        with open(args.csv, newline="", encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                docs.append((r.get("url", ""), r.get("text", "")))
    elif args.urls:
        for u in pagetools.read_url_list(args.urls):
            code, _, html, err = pagetools.fetch(u)
            if code != 200:
                print(f"  skipped {u}: {err or 'status ' + str(code)}")
                continue
            docs.append((u, " ".join(pagetools.parse(html).main_text)))
    else:
        sys.exit("Give one of --html-dir, --csv or --urls.")
    docs = [(u, t) for u, t in docs if len(t.split()) >= 30]
    if len(docs) < 2:
        sys.exit("Fewer than two pages with enough text to compare.")
    return docs


def tokens(text):
    words = re.findall(r"[a-z0-9]+", text.lower())
    return words + [a + "_" + b for a, b in zip(words, words[1:])]


def pairs_sklearn(texts, threshold):
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.preprocessing import normalize
    X = normalize(CountVectorizer(analyzer=tokens).fit_transform(texts))
    S = (X @ X.T).tocoo()
    return [(i, j, v) for i, j, v in zip(S.row, S.col, S.data) if i < j and v >= threshold]


def pairs_pure(texts, threshold):
    import math
    vecs = []
    for t in texts:
        c = Counter(tokens(t))
        n = math.sqrt(sum(v * v for v in c.values())) or 1
        vecs.append({k: v / n for k, v in c.items()})
    out = []
    for i in range(len(vecs)):
        for j in range(i + 1, len(vecs)):
            a, b = (vecs[i], vecs[j]) if len(vecs[i]) < len(vecs[j]) else (vecs[j], vecs[i])
            s = sum(v * b.get(k, 0) for k, v in a.items())
            if s >= threshold:
                out.append((i, j, s))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--html-dir")
    ap.add_argument("--csv")
    ap.add_argument("--urls")
    ap.add_argument("--base", help="site base URL, used to name saved files that have no canonical")
    ap.add_argument("--threshold", type=float, default=0.8)
    ap.add_argument("--out", default="near_duplicates.csv")
    ap.add_argument("--clusters")
    args = ap.parse_args()

    docs = load(args)
    urls, texts = [d[0] for d in docs], [d[1] for d in docs]
    try:
        pairs = pairs_sklearn(texts, args.threshold)
    except ImportError:
        if len(texts) > 500:
            print("Note: scikit-learn not installed; comparing many pages without it is slow.")
        pairs = pairs_pure(texts, args.threshold)
    pairs.sort(key=lambda x: -x[2])

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["url_a", "url_b", "similarity"])
        for i, j, s in pairs:
            w.writerow([urls[i], urls[j], f"{s:.3f}"])

    parent = list(range(len(urls)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i, j, _ in pairs:
        parent[find(i)] = find(j)
    groups = {}
    for i in range(len(urls)):
        groups.setdefault(find(i), []).append(urls[i])
    clusters = sorted([g for g in groups.values() if len(g) > 1], key=len, reverse=True)

    cpath = args.clusters or os.path.splitext(args.out)[0] + "_clusters.csv"
    with open(cpath, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["cluster", "size", "url"])
        for n, g in enumerate(clusters, 1):
            for u in g:
                w.writerow([n, len(g), u])

    in_clusters = sum(len(g) for g in clusters)
    print(f"\nCompared {len(urls)} pages. {len(pairs)} pairs at or above {args.threshold:.0%} similarity.")
    print(f"{in_clusters} pages fall into {len(clusters)} near-duplicate clusters.")
    for n, g in enumerate(clusters[:10], 1):
        print(f"  cluster {n}: {len(g)} pages, e.g. {g[0]}")
    print(f"\nSaved pairs: {args.out}\nSaved clusters: {cpath}")
    print("Next: keep the strongest page in each cluster; rework the others around a distinct angle or consolidate them (stage 3).")


if __name__ == "__main__":
    main()
