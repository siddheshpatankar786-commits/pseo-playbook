# Stage 8: Production

**Purpose:** produce page content at scale without losing quality: a content sheet that acts
as the database, clear sourcing rules, writing per page type, automatic QA, human review,
and a test batch before anything is scaled.

This stage covers both new pages and rewrites of existing pages from the stage 3 Rework
bucket.

---

## Step 8.1: Set up the content sheet

**What it means:** one spreadsheet (Google Sheets works well) where each row is one page and
each column is one field the CMS will receive.

**Why it matters:** the sheet is the source of truth. Writers fill it, QA checks it, the
publishing pipeline reads it. Nothing gets typed directly into the CMS.

**How to do it:** copy `templates/content-sheet.csv`. One tab per page type, because each
type has different fields. Core columns:

| Group | Columns |
|---|---|
| Identity | page_id, page_type, pillar, status |
| URL and structure | slug, url, breadcrumb_parent, commercial_parent |
| SEO block | focus_keyword, meta_title, meta_description, canonical |
| Content | h1, intro, then one column per section in the page anatomy (pain_points, workflow, proof, faqs...) |
| Linking | links_up, related_override, inbound_links_planned |
| Sources | source_notes (where each fact came from) |
| Review | reviewer, qa_status, published_date |

**Done when:** the sheet has the columns for each page type and the first rows filled from
the pillar map.

---

## Step 8.2: Gather the material before writing

**The facts rule.** Every fact on a page comes from one of three places:
1. material the company already has (case studies, product docs, its own data),
2. arithmetic done on that material,
3. cited public sources (regulations, official statistics, standards bodies).

Never invent figures, clients, quotes or results. If a row cannot be filled honestly, leave
it out of this batch.

**Avoid bottlenecks:** do not plan on back-and-forth with subject experts for every page. It
stalls production. Collect material once per pillar (case studies, product walkthroughs, a
short expert interview), store it in a shared folder, and write from that.

**Done when:** each row's source_notes column says where its unique material comes from.

---

## Step 8.3: Write the pages

**How to do it with Claude**
1. Write one instruction block per page type: the narrative, the page anatomy, the tone,
   words to avoid, and the facts rule. Keep it in the sheet or a shared doc so every writer
   uses the same one.
2. Give Claude the row's material and the instruction block, and ask for the section fields
   as separate outputs that map to the sheet columns.
3. Generate in small batches (10 to 20 rows) so problems are caught early.

**Writing rules**
- Meta titles, meta descriptions and H2s must be meaningfully different across pages, not
  the same sentence with the keyword swapped. Read five of them in a row; if they sound the
  same, rewrite.
- Open the page with the reader's situation or problem, not with the company.
- FAQs only where the answer adds something beyond the question.
- Run a humanizer pass (no em dashes, no filler vocabulary, no inflated claims).
- Keep the company's current positioning. Retire outdated terms everywhere at once (for
  example a company moving away from "staff augmentation" language).

**Rewriting existing pages (Rework bucket):** keep the URL, rewrite around a distinct angle
the page's siblings do not cover, change the layout to the page type's anatomy, fix the SEO
block, and add the planned inbound links. A rewrite without new inbound links often does
nothing, because Google may not come back to see it.

---

## Step 8.4: The test batch (do this before scaling)

**What it means:** rewriting or creating 5 to 10 pages to the full standard, publishing
them, and watching what Google does before committing the team to hundreds.

**Why it matters:** it tells you whether content alone fixes the problem, or whether
structure (hubs, links, cleanup) is the blocker. It costs a week instead of a quarter.

**How to do it**
1. Pick 5 to 10 pages from one page type, mixing a few strong and a few weak topics.
2. Write them to the full standard (steps 8.2 and 8.3) and pass QA (step 8.5).
3. Before publishing, add 3 to 5 inbound links to each from frequently crawled pages.
4. Publish, then check each with the launch checklist (stage 10).
5. Request indexing for each in Search Console. Note the date in the change log.
6. Check URL Inspection weekly for **two to four weeks**: last crawl date, and indexed or
   not.

**Reading the result:** see stage 3, step 3.4. In short: indexed means scale the method;
not indexed usually means the site-level structure and cleanup must come first, not that
the writing failed.

**Done when:** the result is recorded in the change log with a decision: scale, adjust, or
fix structure first.

---

## Step 8.5: QA every row before publishing

**Automatic checks**

```bash
python scripts/sheet_qa.py --sheet content_sheet.csv --out qa_report.csv
```

The script flags, per row:
- missing required fields (slug, h1, meta_title, meta_description, breadcrumb_parent)
- meta title or description too long or too short
- duplicate slugs, H1s, meta titles or meta descriptions
- slugs with capitals, spaces or underscores
- placeholder text left in (TBD, lorem ipsum, [insert...], {{...}})
- em dashes and common filler words
- body text too similar to another row (near-duplicate risk)
- fewer than the planned inbound links

Use `--required` and `--similarity` to adjust the checks to the sheet.

**Human review**
- Review every page in the test batch.
- After that, review a random sample of at least 1 in 10 rows per batch, and every row
  that touches regulated claims.
- The reviewer signs the reviewer column. Rows without a reviewer do not publish.

**Done when:** the QA report is clean or every flag is consciously accepted, and the sample
is signed off.

---

## Pacing

Publish in steady batches rather than all at once. A pace around 60 pages a month per site
worked well on a build-from-zero project with almost all pages indexed. Bigger sites with
strong authority can go faster; sites recovering from a cleanup should go slower until
indexing rates look healthy.

## Checkpoint for stage 8

Content sheet set up, sources recorded, writing instructions per page type, test batch
published and read, QA passing, and a publishing pace agreed.
