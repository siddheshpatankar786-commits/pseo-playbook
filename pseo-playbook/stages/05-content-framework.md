# Stage 5: Narrative and content framework

**Purpose:** decide what the company wants to be known for, turn that into a small number of
pillars, and place every page (long-form and programmatic) inside a clear hierarchy.
Without this, programmatic pages float on their own, get few links, and are the first
pages Google ignores.

**Everyday comparison:** a library does not shelve books by the date they arrived. It has
sections, shelves within sections, and a catalogue. Pillars are the sections.

---

## Step 5.1: Agree the narrative first

**What it means:** a few sentences on who the company serves, what problem it solves, and
what makes it different. Not a tagline; the position it wants to own.

**Why it matters:** pillars chosen before the narrative is agreed get renamed later, and
every page built under them has to move. On one project the pillars only settled once the
company agreed it was "AI-native engineering for workflow-intensive industries".

**How to do it:** with the business owner, answer:
1. Which customers bring the most value, and in which industries?
2. What do they buy, in the customer's words?
3. What can the company prove with real case studies?
4. What do competitors all say, and what can only this company say?

Write the answer as three to five sentences in the project brief.

**Done when:** the approver signs off the narrative in writing.

---

## Step 5.2: Choose the pillars

**What it means:** six to eight big topics, each one something the company actually sells
and can prove.

**Rules**
- Every pillar is backed by real case studies or product capability. Decide from evidence,
  not assumptions.
- Name pillars the way buyers read them. On one project "application development" was read
  as "mobile apps", so it became Product Engineering, with Product Design as its own
  pillar.
- Do not force awareness angles (literacy, readiness, adoption, implementation, ROI) onto
  every pillar. Use them where buyers genuinely need educating, usually around newer topics
  such as AI.
- Fewer, stronger pillars beat many thin ones.

**Done when:** each pillar has a name, a one-line focus, and the case studies or product
areas that support it.

---

## Step 5.3: Build each pillar in four layers

```
Company narrative
└── Pillar (one of 6 to 8)
    ├── Layer 1: Pillar page      the broad, authoritative piece on the whole topic
    ├── Layer 2: Cluster pages    deep dives, one subtopic each
    ├── Layer 3: Timely pieces    trends, regulation changes, emerging questions
    └── Layer 4: Programmatic     the "work with us" layer: use cases, industries,
                                  workflows, comparisons, case-study-led pages
```

| Layer | Written by | Typical length | Job |
|---|---|---|---|
| 1 Pillar page | Human, with subject experts | 2,500 to 4,000 words | Earns authority on the topic, links to everything below |
| 2 Cluster | Human, AI-assisted research | 1,500 to 2,500 words | Answers one subtopic in depth |
| 3 Timely | Human | 800 to 1,500 words | Keeps the pillar fresh, catches new searches |
| 4 Programmatic | Generated from the sheet, human-reviewed | 600 to 1,500 words, mostly unique | Captures commercial searches, converts |

A reasonable starting split is around 70 percent long-form and 30 percent programmatic by
word count. Long-form builds the authority that helps programmatic pages get indexed;
programmatic pages turn that authority into leads.

**Done when:** each pillar lists its pillar page, 5 to 15 cluster topics, a few timely
topics, and the programmatic page types (from stage 4) that sit under it.

---

## Step 5.4: Connect the topic tree to the commercial tree

**What it means:** every site has two trees.

- **Commercial tree:** what the navigation shows. Services, products, industries,
  solutions.
- **Topical tree:** pillars and their four layers.

They have to be connected, or the authority built by long-form never reaches the pages that
sell.

**Rules**
1. Each pillar maps to one or more commercial pages (for example, the Data & Analytics
   pillar maps to the Data Analytics service page).
2. **Legacy template pages stay under their existing commercial parents.** Do not force old
   pages into new pillars. On one project, 189 surviving programmatic pages were mapped to
   14 existing service and industry parents, while the new pillars were kept for new
   content.
3. **New programmatic pages are built inside a pillar from day one**, linked up to it and
   from it.
4. **Programmatic pages support commercial pages, never compete with them.** They target
   narrower searches around the core page.
5. When a pillar page is itself a service page (for example a Web Development service page
   with child "hire React developers" pages), the two trees overlap. That is fine and
   simpler: the child pages follow the pillar page's narrative.

---

## Step 5.5: Fill in the pillar map

**How to do it:** copy `templates/pillar-map.csv` and fill one row per planned page:

| Column | What to write |
|---|---|
| pillar | the pillar name |
| layer | 1, 2, 3 or 4 |
| page_type | pillar page, cluster, timely, or the programmatic page type |
| title | working title |
| target_keyword | main search it answers |
| commercial_parent | the service or product page it supports |
| breadcrumb_parent | the page directly above it in the breadcrumb (stage 6) |
| links_up | pages it must link to |
| links_down | pages that must link to it |
| status | planned, writing, review, live |

This sheet becomes the single source for breadcrumbs, internal links and the HTML sitemap
in stage 6.

**Done when:** every planned and existing page appears once, with its pillar, layer,
commercial parent and breadcrumb parent.

---

## Common mistakes

- Choosing pillars from keyword volume instead of from what the company sells.
- Treating programmatic pages as a separate project from long-form.
- Moving legacy pages into new pillars and causing another round of URL changes.

## Checkpoint for stage 5

Approved narrative, six to eight evidence-backed pillars, four layers per pillar, and a
filled pillar map linking every page to a pillar and a commercial parent.
