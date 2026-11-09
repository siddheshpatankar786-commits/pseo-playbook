# Stage 10: Go live and indexing

**Purpose:** confirm every published page is technically ready for Google, then help Google
find it quickly.

---

## Step 10.1: Run the launch checks on every page

**What it means:** a short technical check per page, the same every time.

| Check | Pass looks like |
|---|---|
| Status | The page returns 200 (loads normally), not a redirect or error |
| Canonical | Points to the page's own URL |
| Robots | No `noindex` |
| Title and description | Present, within length, unique |
| H1 | Exactly one, matches the page's topic |
| Content in source | Main text, FAQs and links appear in View Page Source, not only after the page loads |
| No repeated blocks | Sections are not duplicated (a common desktop/mobile template issue) |
| No placeholders | No leftover template text such as "TBD", "lorem ipsum", "If the layout allows" |
| Schema | Valid JSON-LD, one @graph, BreadcrumbList present |
| Breadcrumb | Visible, every level clickable and live |
| Sitemap | The URL is in the right section sitemap with a current lastmod |
| Inbound links | At least 3 to 5 internal links point to it |

**How to do it**

```bash
# fetch live pages (needs open internet: Claude Code or Cowork)
python scripts/launch_checker.py --urls new_pages.txt --out launch_report.csv
# or check saved HTML files (works anywhere)
python scripts/launch_checker.py --html-dir saved_pages/ --out launch_report.csv
```

Then confirm inbound links with `scripts/internal_links.py` (stage 6) and spot-check two or
three pages with Search Console's URL Inspection › Test live URL › View tested page.

Use `templates/launch-checklist.md` for teams that prefer ticking a list.

**Done when:** every page passes or has a fix ticket.

---

## Step 10.2: Ask Google and Bing to visit

**What it means:** letting the search engines know the pages exist.

**How to do it**
1. **Sitemap:** the CMS updates it automatically. In Search Console › Sitemaps, check the
   last read date is recent. Resubmitting is optional.
2. **Request indexing:** in URL Inspection, click Request indexing for the most important
   new pages (hubs, the test batch, the best pages of each type). The daily limit is small,
   so do not spend it on every page of a large batch.
3. **Bing and other engines:** use IndexNow (many CMSs and plugins support it) or submit
   URLs in Bing Webmaster Tools. IndexNow is not used by Google.
4. **Do not use Google's Indexing API** for these pages. Google supports it only for job
   posting and livestream pages.
5. Log the date in the change log.

---

## Step 10.3: Watch the first weeks

**What to check, weekly for four weeks**
- Search Console › Pages, filtered to the section sitemap: indexed versus not indexed.
- URL Inspection on a sample: last crawl date.
- Performance › Pages, filtered to the section folder or URL pattern: first impressions.

**Normal timing:** strong sites see new pages crawled within days and indexed within one to
two weeks. Sites recovering from a cleanup may take much longer. If after about four weeks
most pages show "Discovered - currently not indexed", the issue is crawl priority (add
links from frequently crawled pages, check the sitemap). If they show "Crawled - currently
not indexed", it is quality or duplication (see `library/troubleshooting.md`).

## Pacing releases

Release in steady batches, check each batch's indexing rate, then release the next. If the
indexing rate falls sharply, pause and look before adding more pages.

## Checkpoint for stage 10

All new pages pass launch checks, priority pages requested, IndexNow or Bing submission
done, and weekly monitoring scheduled.
