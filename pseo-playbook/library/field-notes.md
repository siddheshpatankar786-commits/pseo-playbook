# Field notes: what happened on real projects

Anonymized notes from three programmatic SEO projects on B2B sites. Use them as evidence
when explaining why a rule exists. Each lesson is labelled:

- **Proven here:** observed directly on these projects. Not a controlled experiment, so
  treat as strong practical evidence, not proof of cause.
- **Google guidance:** stated in Google's own documentation or policies.
- **Being tested:** a reasonable bet, not yet confirmed. Do not promise it to anyone.

---

## Project A: GRC software company, build from zero

**Starting point:** a legacy site with no SEO foundation, migrated to a visual builder
(Framer). No analytics were capturing data before the migration.

**What was done**
- Migration with redirects for old blog URLs into a new blog folder; analytics, Clarity and
  Bing Webmaster Tools set up through site-wide custom code.
- Four programmatic page types built around the existing product pages, not on their
  keywords: workflow solutions, industry-specific solutions, AI capability use cases, and
  location-based pages.
- Content generated with Claude from a Google Sheet, published straight into the CMS through
  an integration, with a human SEO lead reviewing strategy and quality. Publishing time went
  from about 10 minutes per page to seconds.
- A steady pace of about 60 pages a month, reaching roughly 300 pages over five months.

**What happened**
- Almost all programmatic pages were indexed, with none flagged "crawled - currently not
  indexed" at the time of reporting.
- Qualified inbound leads from organic search started within about a month of publishing at
  scale, from mid-size and large companies.
- AI citations in Bing grew from zero and roughly doubled month on month in the period
  reported.

**Lessons**
- Several page types around core pages, rather than one template, kept pages distinct.
  *Proven here.*
- Sheet-to-CMS automation made steady batches possible without a developer per release.
  *Proven here.*
- Leads are the metric that justifies the work; impressions alone undersell it. *Proven
  here.*

---

## Project B: data and AI services firm, cleanup of legacy template pages

**Starting point:** about 580 programmatic pages at root level with no folders, most from an
older positioning (developer hiring and staffing). Around 350 were "crawled - currently not
indexed" at the worst point.

**What was found**
- Several technologies had six or seven near-identical pages each.
- Page templates repeated sections two or three times in the HTML (separate desktop and
  mobile copies), carried a stale banner repeated above the H1, and in one case a placeholder
  heading left live.
- JSON-LD on older templates was HTML-escaped, so schema could not be read; some FAQ answers
  loaded only in the browser.
- One blog post had a placeholder pasted into its canonical field.
- Rewritten pages still showed a last crawl date about seven weeks old. Only one internal
  link pointed to them, and the sitemap showed a temporary processing error.

**What was done**
- An earlier round of layout and content rework on not-indexed pages brought the count down
  from about 350 to about 220.
- Every root-level page triaged with the three-measure rule (top-20 position in 6 months,
  real clicks, 1,000+ impressions in 12 months). About 180 pages planned for redirection to
  about 19 hub pages built around engagement models and technologies; pages with no clicks and
  no impressions in 12 months deleted; the rest kept and improved.
- A test batch of 5 to 6 rewritten pages, plus about 10 rewritten solution pages, to check
  whether content alone gets pages indexed, while the developer checked templates for
  code-level issues.
- XML sitemap restructured to mirror the categories of the HTML sitemap.

**Lessons**
- Check templates and page-level settings before rewriting content. *Proven here.*
- Rewrites without new inbound links may not even be recrawled. *Proven here.*
- Keep legacy pages under existing commercial parents rather than force-fitting them into new
  pillars. *Proven here (as a working method).*
- Mirroring HTML sitemap categories in segmented XML sitemaps speeds up indexing. *Being
  tested.*
- Whether rewrites alone fix indexing when a large thin pool remains. *Being tested.*

---

## Project C: software services firm, large-scale indexing cleanup

**Starting point:** about 1,900 pages "crawled" or "discovered - not indexed". Earlier
programmatic pages had all shared one content structure and layout.

**What was found**
- 9 of 11 unindexed case studies carried a `noindex,nofollow` tag set page by page, plus one
  dead URL needing a redirect. Content was not the problem for those pages.
- One indexable case study stayed unindexed with thin content and a very large "related"
  carousel diluting the page.

**What was done**
- Not-indexed lists exported, grouped, needless pages removed, and about 230 flagged pages
  queued for real rework across programmatic, case study and core service pages.
- After a few hundred redirects, further duplicates were kept live and linked to each other
  as "see also" pages instead of redirecting more.
- About 190 surviving programmatic pages mapped to 14 existing service and industry parent
  pages, each parent rebuilt with a related-pages section listing its children. An HTML
  sitemap page added.
- New content pillars defined from the company's narrative and real case studies, reserved
  for new content.
- Case study rewrites built on a strict facts rule (existing facts, arithmetic on them,
  cited public sources), with a stage-based structure but no fixed template.

**Lessons**
- Cheap technical checks first: a page-level noindex explains more than any content review.
  *Proven here.*
- One layout for every programmatic page is the failure pattern; vary layouts by page type.
  *Proven here, consistent with Google's scaled content abuse policy.*
- Server logs are needed to confirm whether structure changes increase crawling. *Being
  tested; logs requested.*

---

## Cross-project lessons

| Lesson | Label |
|---|---|
| Pages made mainly to rank, at scale, risk being ignored or demoted regardless of how they were produced | Google guidance |
| Breadcrumbs should reflect a typical user path, not necessarily the URL | Google guidance |
| Check noindex, canonical, rendering and templates before content | Proven here |
| New pages need 3 to 5 links from frequently crawled pages | Proven here (as a working target) |
| Several page types around core pages beat one template | Proven here |
| Test batch before scaling a rewrite method | Proven here (as a working method) |
| Prune using leads and backlinks as well as search numbers | Lesson from a gap: the original rule used search data only |
| Log every change with a date | Lesson from a gap: overlapping fixes made results hard to attribute |
| Segmented XML sitemaps speed up indexing | Being tested |
