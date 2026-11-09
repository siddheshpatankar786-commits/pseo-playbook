# Stage 6: Site structure

**Purpose:** turn the pillar map into a structure Google and visitors can follow: hub pages,
URLs, breadcrumbs, internal links and sitemaps.

This stage has five parts. Teach them one at a time.

1. Hub pages
2. URLs and folders
3. Breadcrumbs
4. Internal linking
5. Sitemaps (XML and HTML)

---

## Part 1: Hub pages

**What it means:** a hub (parent) page introduces a topic and links to every more specific
page under it. "Data Engineering Services" is a hub; "Hire Databricks engineers" and
"Data pipelines for insurance" sit under it.

**Why it matters:** hubs give child pages a home, collect authority, and are where
consolidated pages redirect to. Google finds and values pages that hang off a strong hub
far more than pages that float alone.

**How to do it**
1. From the pillar map, list every distinct parent: pillar pages, service pages, industry
   pages, technology hubs.
2. For each existing page, check whether the parent already exists. Reuse existing service
   and industry pages as parents wherever possible.
3. For missing parents, plan a hub page: a short intro to the topic, what the company does
   in it, proof (one or two case studies), and a grouped list of child pages with one line
   each. Hubs are real pages, not link dumps.
4. Group a hub's children by sub-theme if there are more than about 12 (for example
   "Modern frameworks" and "Legacy and migration" under Web Development).

**Reference:** Zapier's /apps directory is a good model: an app page links to every
integration page for that app. See `library/reference-gallery.md`.

**Done when:** every page in the pillar map has a parent that exists or is planned, and each
planned hub has a content outline.

---

## Part 2: URLs and folders

**What it means:** whether pages sit at the root (`/hire-react-developers`) or inside folders
(`/services/web-development/hire-react-developers`).

**What to decide**
- **New sites or new page types:** use folders that mirror the structure
  (`/solutions/[industry]/`, `/compare/[a]-vs-[b]/`). Folders make reporting by page type
  easy in Search Console and analytics.
- **Existing root-level pages:** do not move them just for neatness. Every URL change needs a
  redirect, and mass redirects carry risk. Breadcrumbs (Part 3) can give flat URLs a clear
  hierarchy without moving anything.
- **Only move existing pages into folders** when a cleanup is already redirecting many of
  them, or when testing shows structure is the blocker. Treat folder moves as a separate,
  logged change.

**URL rules:** lowercase, hyphens, no dates, no stop words where avoidable, no trailing
variations (pick with or without trailing slash and stick to it).

**Done when:** each page type has a URL pattern, and existing URLs are either kept or listed
in the redirect map with a reason.

---

## Part 3: Breadcrumbs

### In plain words

Think of every page as a house.

- The **breadcrumb is its home address**: one fixed path showing where it lives, like
  *Home › Data Analytics › Data warehouse guide*.
- **Internal links are the roads leading to it.** A page can have many roads coming in from
  articles, hubs and related-page boxes, but only one home address.

People mix the two up because both are links. The breadcrumb says where a page belongs.
Internal links say what it is connected to.

### Why breadcrumbs matter

- **Visitors** can go up one level in a click.
- **Google** gets extra crawlable links on every page and a clear picture of how pages are
  grouped. BreadcrumbList schema states the nesting explicitly.
- **Search results:** Google can show the trail instead of the raw URL in desktop results.
  Valid markup makes a page eligible; Google decides each time whether to show it.

### The rule that matters most

The breadcrumb follows how a visitor would find the page, not the URL. Google's own
documentation recommends breadcrumbs that represent a typical user path rather than
mirroring the URL. So pages at root level can still have a proper trail such as
*Home › Solutions › Data analytics for healthcare* without moving URLs or adding
redirects.

### Worked example: one pillar, all four layers

A data consultancy with a pillar called Data Analytics:

| Page | Layer | Breadcrumb | Must link to |
|---|---|---|---|
| The complete guide to data analytics | 1 Pillar | Home › Resources › Data Analytics | All cluster pages, the strongest programmatic pages, the Data Analytics service page |
| Data warehouse vs data lake | 2 Cluster | Home › Resources › Data Analytics › Data warehouse vs data lake | The pillar page, 2 to 3 sibling clusters, 1 to 2 programmatic pages |
| What new AI rules mean for analytics teams | 3 Timely | Home › Blog › Data Analytics › [Post title] | The pillar page, 1 to 2 clusters |
| Data analytics for healthcare | 4 Programmatic | Home › Solutions › Data analytics for healthcare | The service page and the pillar page, plus a related-pages box of sibling industries |

**Why the programmatic page's breadcrumb points to Solutions, not the pillar:** a buyer
looking for "data analytics for healthcare" would find it under Solutions, so that is where
it lives. It still connects to the pillar through links in its body text and the
related-pages box. Commercial pages live under commercial parents, informational pages live
under the pillar, and links join the two trees.

Google allows more than one breadcrumb trail per page, but use one. It is simpler to build
and harder to get wrong.

**When the pillar page is a service page** (for example Web Development, with child hire
pages), the trees overlap and the trail is simply
*Home › Services › Web Development › Hire React developers*.

### Rules

1. Every page except the homepage has a breadcrumb.
2. Every middle level is a real, live page. No level may lead to a 404.
3. The last item is the current page, shown as plain text, not a link.
4. Names match the navigation and the page H1s. The same page is never "AI Services" in one
   place and "AI Development" in another.
5. The visible breadcrumb and the schema match exactly. A mismatch confuses users and
   crawlers and is a common source of Search Console errors.
6. The BreadcrumbList schema sits inside the page's single JSON-LD @graph, not in a
   separate script.

### Who does what

- **SEO owner:** fills the `breadcrumb_parent` column in the pillar map. That one column
  decides every trail.
- **Developer:** builds one breadcrumb component that reads the parent field in the CMS and
  writes both the visible trail and the schema. Never typed by hand page by page.
- **Designer:** places it small, above the H1, identical on every page type.
- **Writer:** nothing to do.

### How to check it is done

1. Open the page: the trail is visible above the heading and every level is clickable.
2. View Page Source: the breadcrumb links are in the HTML itself, not only added after the
   page loads.
3. Rich Results Test: BreadcrumbList detected with no errors.
4. A few weeks after launch: Search Console › Enhancements › Breadcrumbs shows no errors.

### Common mistakes

- "Home › Page name" on every programmatic page. It tells Google nothing about grouping.
- A middle level that is not a real page ("Solutions" in the trail, but /solutions/ does
  not exist).
- Hand-typed breadcrumbs that drift out of sync with the schema.
- Keyword-stuffed or misleading trails, which break Google's structured data policies.

---

## Part 4: Internal linking

### In plain words

Internal links are the roads into a page. Google follows roads from pages it visits often
to find and judge the pages it visits rarely. A new page with one road into it is close to
invisible, however good it is.

**Direction matters.** Links *to* a page from other pages are what help it. Links *on* the
page pointing outward help the other pages. When a page is not getting indexed, the fix is
almost always more links pointing to it, not more links on it.

### The four directions

| Direction | What it means | How many | Where on the page |
|---|---|---|---|
| **Up** | Every page links to its pillar page and its commercial parent | 1 to 2 | Body text early on, plus the breadcrumb |
| **Down** | Pillar and hub pages link to their strongest children | All children for hubs; the best 5 to 15 for pillar pages | A grouped list or cards; body text for the best ones |
| **Across** | Siblings link to each other | 3 to 6 | A "related pages" block, filled automatically from the same parent |
| **Long-form into programmatic** | Articles and guides link to relevant programmatic pages | 1 to 3 per article | Inside the body text, where the topic comes up naturally |

**Target for every new programmatic page at launch: at least 3 to 5 inbound internal links
from pages Google already crawls often** (homepage sections, service pages, hubs, popular
articles). The related-pages block alone does not count as enough, because those blocks are
often on pages that are themselves rarely crawled.

### Anchor text

- Describe the destination in words a reader would use: "data pipelines for insurers",
  not "click here" and not an exact keyword repeated on every page.
- Vary anchors naturally across different linking pages.
- Duplicates you chose not to redirect: link them to each other with a "see also" line.

### Example sentence for a body-text link

On a frequently crawled service page about machine learning:

> We also build adaptive AI systems that keep learning from live data, as covered in our
> [adaptive AI development](/adaptive-ai-development-services) work.

### Who does what

- **SEO owner:** fills `links_up` and `links_down` in the pillar map, and adds body-text
  links in long-form pieces.
- **Developer:** builds the related-pages block (auto-filled from the same parent) and the
  hub child lists from CMS fields.
- **Writer:** adds the planned links while writing, and suggests new ones.

### How to check it is done

```bash
# from a crawler "All Inlinks" export (Source, Destination columns)
python scripts/internal_links.py --inlinks all_inlinks.csv --pages urls.txt --min 3 --out link_report.csv
# from saved HTML files of the site
python scripts/internal_links.py --html-dir site_pages/ --base https://example.com --pages urls.txt --min 3 --out link_report.csv
```

The report lists inbound link counts per page, orphans (zero links) and pages below the
minimum. Search Console's URL Inspection also shows referring pages for a single URL.

---

## Part 5: Sitemaps

### XML sitemap

**What it means:** the machine-readable list of pages you want indexed, with a lastmod date
per page.

**Rules**
1. List only live, indexable, canonical pages. No redirects, 404s or noindex pages.
2. Split by section with a sitemap index: one sitemap per page type or pillar. Search
   Console then shows indexing per section, which makes problems easy to spot.
3. lastmod changes only when the page content genuinely changes. Updating every date on
   every build teaches Google to ignore the dates.
4. Keep each file under 50,000 URLs and 50 MB.

```bash
python scripts/sitemap_builder.py --csv pages.csv --base https://example.com --out-dir sitemaps/
```

`pages.csv` needs `url`, `section`, and optionally `lastmod` and `title`. The script writes a
sitemap index, one sitemap per section, and an HTML sitemap fragment grouped the same way.

### HTML sitemap

A normal page listing all important pages, grouped by the same sections and pillars as the
XML sitemaps. It gives every page at least one more crawlable link and helps visitors.

### Labelled honestly

Mirroring the HTML sitemap's grouping in segmented XML sitemaps is good housekeeping and
makes reporting easier. Whether it changes how fast Google indexes pages is **being tested**
on real projects and is not yet proven. Do not promise it as an indexing fix.

---

## Checkpoint for stage 6

- Every page has an existing or planned parent; hubs are outlined.
- URL patterns decided; no unnecessary URL moves.
- `breadcrumb_parent` filled for every page; breadcrumb component specified.
- Linking rules written per layer; every new page has 3 to 5 planned inbound links.
- Sitemap sections defined to match the HTML sitemap.
