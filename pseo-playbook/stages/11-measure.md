# Stage 11: Measure and maintain

**Purpose:** show what the pages achieve (traffic, leads, AI visibility), keep them accurate,
and prune the ones that stop earning their place.

---

## Step 11.1: Track by page type, not just sitewide

**What it means:** reporting each page type separately, so you can see that industry pages
work and location pages do not, rather than one blended number.

**How to do it**
- **Search Console:** in Performance, add a page filter for each folder or URL pattern
  ("URLs containing /solutions/"). Save the numbers monthly. In Pages, filter by each section
  sitemap to see indexing rates per type.
- **GA4:** build an exploration or report filtered by landing page pattern, showing organic
  sessions and key events.
- **Large sites:** the Search Console interface exports only 1,000 rows. Use the Search
  Console API or the BigQuery bulk export, or a connector, when you need every page.

---

## Step 11.2: Attribute leads to pages

**How to do it, monthly**
1. In Clarity, filter sessions by the form-submit smart event and organic search traffic.
2. For each converting session, note the entry URL, date, and page type in a "Leads by page"
   sheet. Mark the session as a favourite so it is kept beyond the normal retention window.
3. If the form has a hidden landing-page field, match those entries to CRM leads and add
   company name, size and revenue band where the business shares them.
4. Total leads per page type.

**Why monthly:** Clarity keeps full recordings for about 30 days only. Miss a month and the
detail is gone.

**What it tells you:** the single best signal for what to build more of, and which pages must
never be pruned even if their search numbers are small.

---

## Step 11.3: Track AI visibility

- **Bing Webmaster Tools:** AI performance or citation reports show how often pages are cited
  in Bing and Copilot answers.
- **Other assistants:** dedicated tracking tools exist (several offer MCP connectors), or run
  a fixed set of buyer questions in ChatGPT, Perplexity, Gemini and Claude each month and
  record whether the site is cited.
- Re-check robots.txt and hosting-level bot settings each quarter (stage 1, step 1.5).
  Settings change without anyone announcing it.

---

## Step 11.4: Report effort, result and impact

A useful monthly or quarterly report follows a chain, not a pile of metrics:

| Effort (what was done) | Result (what changed in search) | Impact (what it meant for the business) |
|---|---|---|
| 60 industry pages published | 55 indexed, 2,000 impressions | 2 qualified leads from organic, combined company revenue noted |
| 120 thin pages consolidated | Not-indexed count fell from X to Y | Crawl activity on new pages improved |

Outline: `templates/monthly-report.md`. Label partial months as partial, and explain dips
with context rather than hiding them.

---

## Step 11.5: Maintain and prune

**Freshness:** every page with a year, statistic, price, regulation or product claim goes
stale. Give each page type a refresh owner and a review cycle (quarterly for regulated or
fast-moving topics, twice a year otherwise). The more pages, the more this matters.

**Quarterly pruning:** rerun `scripts/gsc_triage.py` with fresh exports, leads and backlinks.
Pages that have had a fair chance (at least six months live) and fall into Consolidate or
Delete get handled the same way as in stage 3. Pruning is routine maintenance, not a crisis
response.

**Cannibalization check:** in Search Console, look for queries where two or more of your pages
swap positions. Merge or differentiate them.

**Migrations:** any website migration needs a URL-by-URL list before and after, a complete
redirect map, and checks that templates kept their breadcrumbs, schema and canonicals.
Otherwise past cleanup work gets undone.

---

## Checkpoint for stage 11

Monthly tracking by page type, a leads-by-page sheet, AI visibility tracking, a report
format agreed, a refresh owner per page type, and a quarterly pruning date in the calendar.
