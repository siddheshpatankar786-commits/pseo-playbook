# Stage 3: Health check and cleanup (Fix track)

**Purpose:** find out why existing pages are not indexed or not performing, fix the
technical causes, and decide for every page whether to keep it, rework it, merge it into
another page, or remove it.

**Everyday comparison:** before renovating a house, check the wiring and plumbing first,
then decide which rooms to keep, merge or knock down.

The order matters. Cheap, site-wide checks come first, because one wrong setting can affect
hundreds of pages and no amount of rewriting will fix it.

---

## Step 3.1: Rule out the big blockers

Go down this list in order. Stop and fix anything you find before going further.

| # | Check | How to check | What a problem looks like | Who fixes |
|---|---|---|---|---|
| 1 | Manual action | Search Console › Security & Manual actions › Manual actions | Any listed action | SEO owner + developer |
| 2 | Security issues | Same menu › Security issues | Hacked content, malware | Developer |
| 3 | Google can reach the page | URL Inspection › Test live URL on 3 to 5 affected pages | "URL is not available to Google", blocked by robots.txt | Developer |
| 4 | Page-level noindex | View page source (right-click › View Page Source), search for `noindex` | `<meta name="robots" content="noindex...">` on pages that should rank | Developer or CMS editor |
| 5 | Canonical | In the source, search for `rel="canonical"` | Missing, pointing to another page, or containing placeholder text | Developer or CMS editor |
| 6 | Status code | URL Inspection, or a crawler | 404, 5xx, or a redirect chain | Developer |
| 7 | What Google actually sees | URL Inspection › View crawled page › HTML, compared with the live page | Main content, FAQs or links missing from the crawled HTML because they load later in the browser | Developer |
| 8 | Template problems | View source and scroll the whole page | The same section repeated two or three times (often separate desktop and mobile copies), leftover placeholder text, a stale ticker or banner repeated above the H1 | Developer + designer |
| 9 | Schema | Paste the URL into Google's Rich Results Test | Errors, or JSON-LD shown as escaped text (`&quot;`) so it cannot be read | Developer |
| 10 | Sitemap health | Search Console › Sitemaps | "Couldn't fetch", "Temporary processing error", old Last read date, lastmod dates never changing | Developer |
| 11 | Inbound internal links | URL Inspection › "Referring page", or `scripts/internal_links.py` | Zero or one internal link pointing to the page | SEO owner (stage 6) |
| 12 | Near-duplicates | `scripts/near_duplicates.py` | Clusters of pages over 80 percent similar | SEO owner (step 3.2) |
| 13 | Site-wide thin pool | Ratio of not-indexed to indexed pages, by group from stage 2 | Large template groups mostly not indexed | Whole plan (steps 3.2 to 3.4) |

**Why the order matters, with a real example:** on one services site, 9 of 11 unindexed
case studies turned out to have a `noindex` tag set page by page. No content work would
have fixed them. On another site, the rewritten pages still showed a last crawl date seven
weeks old: Google was simply not coming back, because the site had a large pool of thin
template pages, a sitemap error, and only one internal link pointing to each rewritten
page. Both were found with the checks above in under an hour.

**Running the near-duplicate check**

```bash
# from saved HTML files (save pages with your browser or a crawler)
python scripts/near_duplicates.py --html-dir pages/ --threshold 0.8 --out dupes.csv
# from a CSV with url,text columns
python scripts/near_duplicates.py --csv page_text.csv --threshold 0.8 --out dupes.csv
# fetch live pages (needs open internet: Claude Code or Cowork)
python scripts/near_duplicates.py --urls urls.txt --threshold 0.8 --out dupes.csv
```

**Output of this step:** one consolidated technical ticket for the developer
(`templates/developer-brief.md`, "Fix ticket" section) listing every issue, the affected
URLs, how to see the problem, and the expected result. One ticket, written as a request,
beats ten scattered messages.

**Done when:** blockers 1 to 10 are fixed or confirmed clean, and you have the inbound link
counts and duplicate clusters ready for the next step.

---

## Step 3.2: Decide what happens to each page

**What it means:** putting every template page into one bucket:

| Bucket | Meaning | Action |
|---|---|---|
| **Keep** | Performing, unique | Leave it, add internal links |
| **Rework** | Has some signal or a genuinely distinct topic, but weak content | Rewrite around a distinct angle (stage 8) |
| **Consolidate** | Weak, and a close equivalent exists | 301 redirect to the best equivalent or the parent hub |
| **Delete** | No traffic, no value, no close equivalent | Remove, return 410 (or 404), drop from sitemap |
| **Needs decision** | Business input required | Ask the owner |

**The default rule** (adjust the numbers to the site's size, see below):

- **Delete** only if all are true: zero clicks and zero impressions in 12 months, no
  backlinks from other sites, no leads in Clarity, GA4 or the CRM, and no structural role
  (it is not a parent page).
- **Consolidate** only if weak on all three: never in the top 20 positions in the last 6
  months, no meaningful clicks, and under 1,000 impressions in 12 months, AND a close
  equivalent page exists to redirect to.
- **Rework** if it is weak but covers a topic nothing else covers, or has some positive
  signal on any of the three measures.
- **Keep** if it is ranking and getting clicks.
- **Near-duplicates:** keep the strongest page of each cluster. The others are either
  reworked around a clearly different angle, or consolidated into the strongest one.

**Scaling the thresholds**

| Site size (sitewide impressions per month) | "Under X impressions in 12 months" |
|---|---|
| Under 20,000 | 100 |
| 20,000 to 500,000 | 1,000 (default) |
| Over 500,000 | 5,000 |

These are starting points, not laws. Explain them to the business owner and agree them
before running the script.

**Why leads and backlinks come before search numbers:** a page with 40 impressions a year
that brought in one enterprise lead is worth more than a page with 4,000 impressions and no
leads. A page with links from other websites carries value that a delete would throw away;
redirect it instead.

**How to do it**

```bash
python scripts/gsc_triage.py \
  --perf-12m gsc_pages_12m.csv \
  --perf-6m gsc_pages_6m.csv \
  --not-indexed crawled_not_indexed.csv discovered_not_indexed.csv \
  --leads lead_landing_pages.csv \
  --backlinks backlinks.csv \
  --urls sitemap.xml \
  --duplicates dupes.csv \
  --protect hubs.txt \
  --impressions-threshold 1000 \
  --scope-prefix https://example.com/ \
  --out triage.csv
```

Only the 12-month export is required. Every optional file makes the decision safer, and
two matter most: `--urls` (performance exports leave out pages with zero impressions, so
without the full URL list those pages are invisible) and `--protect` (a list of hub and
parent pages that must never be deleted or redirected). Then
open the sheet with the business owner and walk through the Consolidate and Delete
buckets group by group, not page by page. Use `templates/triage-sheet.csv` for the column
layout if you are building it by hand.

**Choosing redirect targets**
- Redirect to the closest equivalent: the strongest page in the duplicate cluster, or the
  hub page for that technology, industry or service.
- Never redirect a batch of pages to the homepage. Google treats unrelated redirects as soft
  404s and the value is lost.
- If several hundred redirects have already been done on the site, stop adding more for
  duplicates. Keep both pages live and link them to each other as "see also" pages instead,
  and revisit canonical tags later.

**Done when:** every page has a bucket and a reason, and the owner has agreed the
Consolidate and Delete lists.

---

## Step 3.3: Carry out the cleanup

**How to do it**
1. **Redirect map:** one sheet with old URL and new URL, every redirect pointing straight
   to the final page (no chains). The developer implements it on the server or in the CMS
   redirect settings.
2. **Fix internal links:** any link on the site still pointing to a redirected or deleted
   page gets updated to the new page.
3. **Deleted pages:** return 410 (or 404), and remove them from the sitemap and the HTML
   sitemap.
4. **Sitemap:** only live, indexable, canonical pages should remain listed.
5. **Change log:** one dated entry per batch ("142 pages redirected to 14 hubs").

**Done when:** a crawl shows no internal links to redirected or deleted pages, no redirect
chains, and the sitemap lists only live pages.

---

## Step 3.4: Test before reworking everything

Before rewriting hundreds of Rework pages, run the test batch in stage 8 (step 8.4): rewrite
5 to 10 pages properly, give each 3 to 5 inbound internal links, publish, request indexing,
and wait at least two weeks.

**How to read the result**
- **Most get indexed:** the content approach works. Roll it out in batches.
- **Few or none get indexed:** do not conclude the rewrites were bad. When Google is
  holding back a whole site because of a large thin pool, even good pages wait until the
  cleanup is done. The answer then is structure: finish consolidation, build the hub pages
  (stage 6), strengthen internal links, and test again.
- Either way, the hub pages are usually needed, because consolidated pages redirect to
  them.

---

## Expectations to set

- Technical fixes can show results in days to weeks.
- Site-wide recovery after a large thin-page cleanup often takes months, because Google has
  to recrawl and re-judge the site.
- Cleanup of a few hundred pages, with a small team working in parallel, typically takes
  about two months. A few thousand can take three.

## Checkpoint for stage 3

Technical blockers fixed, every page in a bucket with a reason, redirects and deletions
live without chains, sitemap cleaned, change log updated, and the test batch planned.
