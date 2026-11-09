---
name: pseo-playbook
description: >
  Beginner-friendly, end-to-end playbook for programmatic SEO (pSEO): site inventory,
  fixing "crawled - currently not indexed" pages, keep/rework/redirect/delete decisions,
  pillar and content hierarchy, breadcrumbs, internal linking, page types and layouts, CMS
  requirements, developer and designer handoffs, content sheets, sheet-to-CMS publishing
  (Framer, Webflow, Strapi, WordPress), test batches, launch checks, indexing and lead
  tracking, with scripts for URL grouping, Search Console triage, near-duplicates, launch
  checks, link counts, sitemaps and sheet QA. Use it whenever someone wants to plan, build,
  clean up or launch pages at scale from templates or a spreadsheet, fix unindexed or thin
  template pages, design hub or pillar pages, decide breadcrumbs or interlinking, brief
  developers on SEO page builds, or asks how to get pages live and indexed, even if they
  never say "programmatic SEO".
---

# Programmatic SEO playbook

This skill walks a person from zero to live, indexed programmatic pages. It is written for
someone who may not be technical, so you (Claude) act as a patient guide: one stage at a
time, every term explained in plain words the first time it appears, and a clear "done"
check before moving on.

The guidance comes from real programmatic SEO projects on B2B SaaS and B2B services sites,
covering both a build-from-zero program and two large cleanups of unindexed template pages.
`library/field-notes.md` records what happened on those projects and which lessons are
proven versus still being tested. Treat it as evidence, not as a script to copy.

## How to guide the person

1. **Run the intake first** (below). Never start building before you know the starting
   point, platform, business type, size and team.
2. **Work one stage at a time.** Read the stage file, explain what the stage is for in two
   or three plain sentences, then walk through its steps. End every stage at its
   checkpoint and confirm before moving on.
3. **Explain, then instruct.** Every step in the stage files follows the same pattern:
   what it means, why it matters, a worked example, who does what, how to check it is
   done, and common mistakes. Keep that order when you teach it. If the person asks "what
   does that mean?", answer with the plain-words version and an everyday comparison
   before any technical detail.
4. **Use their data, not generic advice.** Wherever a stage has a script, ask for the
   export it needs and run it. Show results as a short summary plus a downloadable sheet.
5. **Separate roles.** Many people following this cannot code or design. Their job is to
   decide and to brief well. Use the handoff templates so developers and designers get
   clear, collaborative requests with references, not vague asks or orders.
6. **Label confidence.** When you pass on a lesson, say whether it is proven in practice,
   standard Google guidance, or still being tested. Never present a hunch as a rule.
7. **Write like a person.** All copy you produce (pages, briefs, emails) gets a humanizer
   pass if that skill is available: no em dashes, no filler vocabulary, no inflated claims.

## Intake (ask these first, in plain words)

Ask conversationally, a couple at a time, and skip anything already answered.

1. **Do you already have programmatic or template pages live?** If yes, roughly how many,
   and does Search Console show many as "crawled - currently not indexed" or
   "discovered - currently not indexed"?
2. **What is the website built on?** (Framer, Webflow, WordPress, Strapi or another
   headless CMS, custom code, not sure.)
3. **What kind of business is it?** (SaaS product, services firm or agency, marketplace,
   ecommerce, local business, publisher.) This decides where each page's unique value comes
   from.
4. **Roughly how big is the site's search presence?** Monthly impressions and clicks from
   Search Console are enough. This scales the thresholds in stage 3.
5. **Who is on the team?** Writer, designer, developer, and whether the person can publish
   to the CMS themselves.
6. **What is the goal?** Leads, signups, AI search visibility (citations in ChatGPT,
   Perplexity, Gemini, Claude), or all of these.

Then confirm the track and write a one-paragraph project brief the later stages can refer
back to (template: `templates/project-brief.md`).

## Two tracks, one pipeline

| Track | Who it is for | Stages |
|---|---|---|
| **Build** | No programmatic pages yet, or a new site or migration | 0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11 |
| **Fix** | Template pages exist and many are not indexed, thin or duplicated | 0, 1, 2, 3, then 4 to 11 for rebuilding and growth |

Both tracks meet at stage 5. A Fix project usually runs stage 3 cleanup and the stage 8
test batch before scaling anything new.

## Stage map

Read only the file for the stage you are on.

| # | Stage | File | What it produces |
|---|---|---|---|
| 0 | Basics | `stages/00-basics.md` | Shared vocabulary in plain words |
| 1 | Setup and access | `stages/01-setup.md` | Search Console, Bing, GA4, Clarity, CMS access, roles, change log |
| 2 | Know the site | `stages/02-inventory.md` | Every URL grouped by type, with status |
| 3 | Health check and cleanup (Fix track) | `stages/03-health-check.md` | Keep / rework / redirect / delete sheet, technical fix ticket |
| 4 | Find the opportunities | `stages/04-opportunities.md` | Keyword patterns, page types, priority list |
| 5 | Narrative and content framework | `stages/05-content-framework.md` | Pillars, four content layers, pillar map |
| 6 | Site structure | `stages/06-site-structure.md` | Hubs, URLs, breadcrumbs, interlinking rules, sitemaps |
| 7 | Page design and the handoff kit | `stages/07-page-design.md` | Page anatomy per type, CMS requirements, dev and design briefs |
| 8 | Production | `stages/08-production.md` | Content sheet, writing rules, QA, test batch |
| 9 | Publishing | `stages/09-publishing.md` | Sheet-to-CMS pipeline for the platform in use |
| 10 | Go live and indexing | `stages/10-go-live.md` | Launch checks, release pacing, indexing requests |
| 11 | Measure and maintain | `stages/11-measure.md` | Tracking, lead attribution, reporting, pruning cycle |

Platform guides for stage 9 live in `cms/` (`visual-builders.md`, `headless.md`,
`wordpress.md`, `custom.md`). Read only the one that matches the site.

## Ground rules that apply in every stage

These come from what went wrong or right on real projects. Explain the reason when you
apply one, so the person learns the principle and not just the rule.

- **Every page must deserve to exist without search engines.** Before any page type is
  approved, name what is unique on each page: its own data, a real case study, a working
  tool, a specific workflow. If the honest answer is "only the keyword changes", the page
  type is not ready. Google's scaled content abuse policy targets pages made mainly to
  rank, whether written by AI, templates or people.
- **Facts come from three places only:** facts the company already has (case studies,
  product docs, its own data), arithmetic done on those facts, or cited public sources.
  Never invent figures, clients, quotes or results to fill a template.
- **One template for every page is the main failure pattern.** Use different layouts per
  page type and intent, and vary section order and components so pages do not look
  mass-produced.
- **Programmatic pages support the core pages, they do not compete with them.** Build
  around product and service pages, never on their main keywords.
- **Test small before scaling.** Publish a batch of about 5 to 10 pages, request indexing,
  and wait at least two weeks before rolling a method out to hundreds of pages.
- **Log every change with a date** (`templates/change-log.csv`). When several fixes land
  together, the log is the only way to tell what worked.
- **Check leads and backlinks before deleting or redirecting anything.** Search numbers
  alone can hide a page that brought a real customer.
- **Breadcrumbs, schema and sitemaps are generated by the CMS from fields, never typed by
  hand page by page.**
- **Handoffs are requests with references.** Developers and designers get one consolidated,
  clearly written brief per piece of work, with example pages to look at.
- **AI search visibility needs access first.** Check that AI crawlers are not blocked
  before blaming content for zero citations (stage 1).

## Scripts

All scripts are in `scripts/`, run with Python 3, and print a plain-language summary. They
work from uploaded exports, so the person never touches code: ask for the file, run the
script, share the output. Run any script with `--help` to see its options.

| Script | Stage | Input | Output |
|---|---|---|---|
| `url_grouper.py` | 2 | sitemap XML or a URL list | URLs grouped by folder and slug pattern |
| `gsc_triage.py` | 3 | Search Console page exports (+ optional indexing list, leads, backlinks) | keep / rework / redirect / delete sheet with reasons |
| `near_duplicates.py` | 3, 8 | saved HTML pages, a text CSV, or URLs to fetch | near-duplicate pairs and clusters |
| `internal_links.py` | 6, 10 | crawler inlinks export or saved HTML | inbound link count per page, orphan list |
| `sitemap_builder.py` | 6 | CSV of url, section, lastmod | sitemap index, one XML sitemap per section, HTML sitemap |
| `sheet_qa.py` | 8 | content sheet CSV | row-by-row QA report |
| `launch_checker.py` | 10 | URLs to fetch or saved HTML | pass/fail launch report per page |

Fetching live URLs needs open internet. In the Claude.ai chat sandbox, outbound access is
limited, so use uploaded files there; run fetch modes in Claude Code or Cowork.

## Templates and library

- `templates/`: project brief, change log, triage sheet columns, pillar map, content sheet,
  CMS requirements checklist, developer brief, designer brief, launch checklist, monthly
  report outline.
- `library/page-types.md`: page type catalogue with intent, URL, breadcrumb, sections and
  where the uniqueness comes from.
- `library/reference-gallery.md`: real programmatic page examples to show developers and
  designers, with notes on what to point out and what a smaller company can copy.
- `library/troubleshooting.md`: symptom, likely causes, how to check, fix.
- `library/field-notes.md`: anonymized project evidence, proven versus being tested.

## Related tools

- **Skills:** a content gap or competitor sitemap analysis skill (stage 4), a humanizer
  skill (stage 8), a spreadsheet skill for building sheets.
- **Data connectors, if available:** Google Search Console (community MCP servers or the
  API; CSV exports always work), Bing Webmaster Tools, a keyword data source such as
  DataForSEO, Ahrefs or Semrush, Notion or Google Drive for trackers. Never block a stage
  on a connector; every stage works from exports.

## Output style

Short summaries, then the deliverable. Sheets for lists of pages, plain-text briefs for
people, tables only where comparing options. Avoid jargon; when a technical term is
unavoidable, define it in one line.
