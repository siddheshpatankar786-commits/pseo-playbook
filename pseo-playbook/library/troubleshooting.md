# Troubleshooting by symptom

Find the symptom, then work through the causes in the order listed (most likely and
cheapest to check first).

---

## 1. Many pages "Crawled - currently not indexed"

Google visited and chose not to store them.

| Likely cause | How to check | Fix |
|---|---|---|
| Near-duplicate pages | `scripts/near_duplicates.py` on the group | Consolidate or rework around distinct angles (stage 3) |
| Thin content, mostly shared boilerplate | Compare two pages of the type side by side; estimate the unique share | Rework with real material; cut shared blocks |
| Template repeats sections or shows placeholders | View Page Source, scroll the whole page | Developer fixes the template once |
| Content only loads in the browser | URL Inspection › View crawled page › HTML | Server-side rendering for content and links |
| Large thin pool dragging the whole site | Share of not-indexed pages per group (stage 2) | Cleanup first, then rebuild with hubs and links |

## 2. Many pages "Discovered - currently not indexed"

Google knows the URLs but has not visited.

| Likely cause | How to check | Fix |
|---|---|---|
| Few or no inbound links | `scripts/internal_links.py`; URL Inspection referring pages | 3 to 5 links from frequently crawled pages |
| Too many low-value URLs competing for attention | Ratio of template pages to strong pages | Prune and consolidate |
| Sitemap problems | Search Console › Sitemaps status and last read | Fix errors, keep only live pages, real lastmod dates |
| Server slow or erroring under crawl | Search Console › Settings › Crawl stats (response time, errors) | Developer improves speed and stability |

## 3. Rewritten pages still show an old crawl date

| Likely cause | How to check | Fix |
|---|---|---|
| Google has no reason to come back | Only one or two links point to the page | Add links from frequently crawled pages, then request indexing |
| lastmod not updated in the sitemap | Open the sitemap, find the URL | Make lastmod reflect real content changes |
| Sitemap error ("couldn't fetch", "temporary processing error") | Search Console › Sitemaps | Validate the XML, check it loads quickly, resubmit |
| Site-wide low priority | Many sections show the same pattern | Continue cleanup; expect weeks to months |

## 4. A specific important page is not indexed

Check in this order: URL Inspection live test → noindex in source → canonical pointing
elsewhere or containing placeholder text → status code → content in crawled HTML →
inbound links → duplicate of another page.

## 5. "Duplicate without user-selected canonical"

Google sees two of your pages as the same and picked one.
Fix: add a self-referencing canonical on every page; consolidate true duplicates with a 301;
differentiate pages that should both exist.

## 6. "Alternate page with proper canonical" on pages you want indexed

The page's canonical points to another URL. Check the CMS canonical field and template
defaults. Canonical should point to the page itself unless it truly is a copy.

## 7. Soft 404 on redirected pages

Redirects point to unrelated pages (often the homepage). Point each old page to its closest
equivalent or parent hub; if nothing is close, return 410 instead.

## 8. Breadcrumb errors in Search Console

| Error | Cause | Fix |
|---|---|---|
| Missing field "item" | A middle level has no URL | Every level except the last needs a URL |
| Invalid URL | Relative or placeholder URLs | Use full URLs generated from the CMS |
| Mismatch with visible trail | Schema and visible trail built separately | Generate both from the same parent field |

## 9. Schema not detected or "unparsable structured data"

The JSON-LD is escaped (shows `&quot;` instead of quotes), broken by a stray character, or
split across conflicting scripts. Fix in the template: output raw JSON-LD, one script, one
@graph. Validate with the Rich Results Test.

## 10. Pages indexed but no impressions

The page type does not match what people search, or the core page outranks it for the same
query. Check the target keyword's live results, adjust the angle, or merge into the core
page.

## 11. Impressions but no clicks

Titles and descriptions look like every other result. Rewrite meta titles around the specific
situation; check the page answers what the searcher wants in the first screen.

## 12. Traffic but no leads

Check in Clarity: do visitors scroll to the proof and CTA? Is the form working on mobile?
Does the CTA match the intent (a buyer comparing options may want pricing or a case study,
not "book a call")?

## 13. Zero AI citations despite good rankings

| Likely cause | How to check | Fix |
|---|---|---|
| AI crawlers blocked | robots.txt; hosting or CDN bot settings | Allow the search-oriented AI bots the business wants |
| Content not quotable | Answers buried in long paragraphs | Lead sections with a direct, specific answer; use clear tables |
| Content only in the browser | Crawled HTML check | Server-side rendering |

## 14. Pages dropped after a Google update

Compare which page types fell. If template pages with little unique value fell most, treat it
as a quality problem: consolidate and rework the weakest groups first. There is no
reconsideration request for algorithmic drops; recovery comes from improving the site and
waiting for re-assessment.
