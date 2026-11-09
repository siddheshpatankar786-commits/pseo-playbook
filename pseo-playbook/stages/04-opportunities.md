# Stage 4: Find the opportunities

**Purpose:** decide which page types to build, based on what buyers search for, what
competitors cover or ignore, and what the company can genuinely say something useful about.

**Everyday comparison:** before opening a new shop section, you check what customers ask
for, what nearby shops stock, and what you can supply better than them.

---

## Step 4.1: Look at what competitors publish

**What it means:** pulling competitors' sitemaps and sorting their pages into content
types, to see where they invest and what they leave empty.

**Why it matters:** on several B2B projects, even competitors with large SEO teams put most
of their output into capability and showcase content ("AI for [industry]", "[service] for
[use case]") and almost none into awareness topics (literacy, readiness, adoption,
implementation). The imbalance is the opening.

**How to do it**
1. List 4 to 6 real competitors, ideally including one much larger and one similar in
   size. Ask the business owner who they lose deals to.
2. Download each one's sitemap. Keep only pages in the main language, and drop news, careers
   and legal pages.
3. If a content gap or sitemap analysis skill is available, use it to classify pages into
   content pillars. Otherwise run `scripts/url_grouper.py` on each sitemap and compare the
   pattern counts side by side.
4. Note per competitor: which page types they run at scale (hire pages, industry pages,
   comparisons, integrations, locations) and which topics are thin or missing.

**Done when:** you have one table: page type or pillar by competitor, with counts, and three
to five gaps written in plain words.

---

## Step 4.2: Find keyword patterns, not single keywords

**What it means:** programmatic pages target a pattern with a fixed part and a changing
part. "[Software category] for [industry]", "[tool A] vs [tool B]", "hire [technology]
developers", "[service] in [city]".

**How to do it**
1. Write down the fixed "head" terms the business sells (its products, services,
   capabilities).
2. List the "modifiers" buyers add: industries, use cases, workflows, roles, technologies,
   integrations, competitor names, locations.
3. Combine them and check search volume and cost-per-click with a keyword tool (DataForSEO,
   Ahrefs, Semrush, or Google Keyword Planner). Prioritize high cost-per-click patterns for
   lead generation: advertisers pay more where buyers are closer to spending.
4. Search 3 to 5 examples of each pattern in Google yourself. Look at what ranks: product
   pages, listicles, comparison pages, forums. Your page type should match that intent.
5. Drop patterns where the top results are all quick definitions; AI answers now satisfy
   most of those searches directly.

**Done when:** you have a sheet of patterns with example keywords, volume, cost-per-click,
intent (learning, comparing, buying) and what currently ranks.

---

## Step 4.3: Check the uniqueness source for each pattern

**What it means:** for every pattern, naming what will make each page genuinely different
from its siblings.

**Where uniqueness comes from, by business type**

| Business type | Typical uniqueness sources |
|---|---|
| SaaS product | Real workflows inside the product, feature combinations per use case, integrations, product screenshots, pricing logic |
| Services firm or agency | Case studies, delivery approach per industry, engagement models, team expertise, typical timelines and costs |
| Data-rich business | Its own dataset: prices, rates, availability, benchmarks |
| Marketplace | Listings, supply counts, reviews per category or location |
| Local business | Real locations, local staff, local projects |

**The test:** if you cannot fill the unique fields for at least 20 rows of the pattern from
real material, the pattern is not ready. Either collect the material first or drop it.

**Done when:** each shortlisted pattern has named uniqueness sources and a realistic number
of rows that can be filled honestly.

---

## Step 4.4: Pick page types and protect the core pages

**What it means:** turning patterns into page types (see `library/page-types.md`) and
checking none of them steals the main keywords of the product or service pages.

**How to do it**
1. Map each pattern to a page type from the library, or define a new one.
2. Next to each, write which existing core page it supports. The programmatic page targets
   the narrower search ("audit software for hospitals"); the core page keeps the broad one
   ("audit software").
3. Rank page types by: lead value (cost-per-click, intent), uniqueness available, effort to
   build, and number of rows.
4. Pick two or three page types to start. Different layouts for each.

**Worked example:** a GRC software company built four page types around its existing
product pages instead of on them: workflow solutions, industry-specific solutions, AI
capability use cases, and location-based pages. About 300 pages went live over five months
with almost all indexed, and qualified leads arrived within roughly a month of publishing
at scale.

**Done when:** two or three page types are chosen, each with its supporting core page,
uniqueness source, and estimated row count.

---

## Common mistakes

- Picking patterns by volume alone, ignoring whether the company can say anything specific.
- Building one page type for every pattern.
- Location pages for places where the business has no presence. That is the classic
  doorway-page pattern Google's policies warn against.

## Checkpoint for stage 4

A short list of page types, each with keyword pattern, intent, uniqueness source, supported
core page, and row count. The business owner agrees with the list.
