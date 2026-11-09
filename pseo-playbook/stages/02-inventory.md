# Stage 2: Know the site

**Purpose:** get one list of every URL on the site, grouped by what kind of page it is, with
its index status. Every later decision (cleanup, hubs, breadcrumbs, linking) works off this
list.

**Everyday comparison:** before reorganizing a warehouse, you count what is on the shelves
and label each shelf.

---

## Step 2.1: Collect the URL lists

**What it means:** pulling the same site from three angles, because each one misses
something.

**How to do it:** collect as many of these as you can:

1. **XML sitemap:** open /sitemap.xml (or /sitemap_index.xml) and save the file. If it is
   an index of several sitemaps, save each one.
2. **Search Console Pages report:** export the indexed list and each "not indexed" reason
   (Crawled - currently not indexed, Discovered - currently not indexed, Duplicate without
   user-selected canonical, Excluded by noindex, Page with redirect, Not found 404, Soft
   404, Alternate page with proper canonical).
3. **Search Console Performance › Pages:** last 12 months, with clicks, impressions,
   CTR and position.
4. **Optional crawl:** a crawler such as Screaming Frog (free up to 500 URLs) finds pages
   the sitemap forgot and pages that link nowhere.

**Done when:** the files are saved in one folder with dates in their names.

---

## Step 2.2: Group the URLs

**What it means:** sorting URLs into buckets by folder and by naming pattern, for example
everything starting with `hire-`, everything containing `-vs-`, everything under `/blog/`.

**Why it matters:** template pages share naming patterns. Grouping shows how many of each
template exist, which is the first clue about thin or duplicated page types.

**How to do it:** run the grouper on the sitemap file(s) or any URL list.

```bash
python scripts/url_grouper.py sitemap.xml --out url_groups.csv
python scripts/url_grouper.py urls.txt --out url_groups.csv      # one URL per line
```

The script reports:
- how many URLs sit at root level versus inside folders,
- counts per first folder (`/blog/`, `/services/`, ...),
- counts per slug pattern (`hire-*`, `*-vs-*`, `*-development-services`, ...),
- a CSV with each URL, its folder, depth and detected pattern.

Then add the index status from the Search Console exports to the same sheet (the triage
script in stage 3 does this automatically if you are on the Fix track).

**Worked example:** a services site with about 580 pages finds that roughly 500 sit at root
level with no folders, and that one pattern (`hire-[technology]-developers`) accounts for
over 200 of them. Several technologies have six or seven near-identical pages each. That
single view explained most of its indexing problem.

**Done when:** every URL has a group, and you can say in one sentence what each large group
is.

---

## Step 2.3: Name each group's job

**What it means:** writing next to each group what the pages are for: selling (commercial),
teaching (informational), proof (case studies), navigation (hubs), or legacy (old
positioning no longer used).

**Why it matters:** commercial and informational pages get different parents, breadcrumbs
and layouts later. Legacy pages are the first candidates for consolidation.

**How to do it:** add a "job" column to the grouped sheet and fill it per group, not per
URL. Ask the business owner about any group whose purpose is unclear.

**Done when:** every group has a job, and any group with no clear job is flagged for
stage 3.

---

## Common mistakes

- Trusting the sitemap alone. Sitemaps often miss pages and often still list deleted ones.
- Looking at counts only. Ten pages in a group with 9 not indexed is a stronger signal than
  a hundred pages with 5 not indexed.
- Skipping the "job" column, then mixing selling and teaching pages under the same parent.

## Checkpoint for stage 2

One sheet with every URL, its group, folder depth, job, and index status. Build track
projects move to stage 4. Fix track projects move to stage 3.
