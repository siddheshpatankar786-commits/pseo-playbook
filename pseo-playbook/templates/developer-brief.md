# Developer brief

Write one brief per page type, plus one fix ticket for technical issues. Keep the tone
collaborative: you are asking for help, with everything needed to do it well.

---

## Page type brief

**Hi [name], could we set up the [page type] pages as described below? Happy to walk
through it on a call.**

**What these pages are for:** one or two sentences on the search intent and the business
goal.

**Collection / content type:** `[name]`
**URL pattern:** `/[folder]/[slug]/`
**Breadcrumb:** Home › [Parent] › [Page name], generated from the `breadcrumb_parent` field

**Fields**
| Field | Type | Required | Notes |
|---|---|---|---|
| h1 | text | yes | |
| intro | rich text | yes | |
| [section fields] | | | |
| meta_title | text | yes | |
| meta_description | text | yes | |
| canonical | URL | no | default to the page's own URL when empty |
| breadcrumb_parent | reference | yes | |

**Automatic parts**
- Related pages: same parent, up to 6, plus the commercial parent.
- Schema: WebPage + BreadcrumbList (+ FAQPage when FAQs exist) in one JSON-LD @graph.
- Sitemap: include in the `[section]` sitemap with real lastmod.

**References:** [link] for [what to look at]; [link] for [what to look at].

**Done looks like:** a test entry imported from the sheet renders with every section,
correct breadcrumb and schema (Rich Results Test passes), appears in its section sitemap,
and passes `launch_checker.py`.

---

## Fix ticket

**Hi [name], I found a few template-level issues that are likely holding these pages back
from Google. Could we look at them together?**

| # | Issue | Affected URLs | How to see it | Expected result |
|---|---|---|---|---|
| 1 | e.g. sections repeated 2 to 3 times in the HTML | [list or sheet link] | View Page Source, search for the H2 text | Each section appears once |
| 2 | e.g. JSON-LD escaped | | Rich Results Test shows no items | Valid schema detected |

**Priority:** which ones block indexing (do first) and which are improvements.
