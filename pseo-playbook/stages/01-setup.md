# Stage 1: Setup and access

**Purpose:** before changing anything, make sure you can see what Google and visitors do on
the site, that the right people can make changes, and that today's numbers are saved as a
baseline. Skipping this is why many projects later cannot prove what worked.

Work through the steps in order. Each ends with a "done when" check.

---

## Step 1.1: Google Search Console

**What it means:** Search Console is Google's report card for the site: which pages are
indexed, which searches show them, and what problems Google found.

**Why it matters:** almost every decision in stages 2, 3, 10 and 11 uses its exports.

**How to do it**
1. Go to search.google.com/search-console and add a **Domain** property (covers http,
   https, www and non-www together). If DNS access is not available, use a URL-prefix
   property for the main version of the site.
2. Verify ownership. Domain properties need a DNS TXT record; whoever manages the domain
   (often the developer or IT) adds it. Send them the record with a one-line request.
3. Under **Sitemaps**, submit the XML sitemap URL (usually /sitemap.xml).
4. Give the SEO owner "Full" access and others "Restricted" under Settings › Users.

**Who does what:** SEO owner sets up; developer or IT adds the DNS record.

**Done when:** the property shows data, the sitemap status says "Success", and the Pages
report loads.

**Common mistakes**
- Verifying only the www or non-www version, then missing half the data.
- Submitting a sitemap that still lists deleted or redirected pages.

---

## Step 1.2: Bing Webmaster Tools

**What it means:** Bing's version of Search Console. It powers Copilot and feeds several AI
assistants, and it reports AI citations.

**How to do it:** sign in at bing.com/webmasters and choose **Import from Google Search
Console**. This copies the verified sites and sitemaps in one step.

**Done when:** the site appears with its sitemap, and you can find the AI performance or
citations report.

---

## Step 1.3: Analytics and lead tracking (GA4 and Microsoft Clarity)

**What it means:** GA4 counts visits and conversions. Clarity records sessions and shows the
page each visitor first landed on, which is how a lead gets traced back to the
programmatic page that brought them.

**How to do it**
1. Install GA4 and Clarity on every page. On visual builders like Framer or Webflow this is
   usually pasted into the site-wide custom code (head) setting. On WordPress, use a plugin
   or the theme header. On custom sites, ask the developer.
2. In GA4, mark the form submission (or thank-you page view) as a **key event**.
3. In Clarity, set up a **smart event** for the form submission. Then a filter like
   "submitted the form + came from organic search" shows each converting session with its
   **entry URL**.
4. If the CRM needs to match a named lead to a page, ask the developer to add a hidden
   "landing page" field to the form, or to set Clarity's custom user ID.

**Limits to explain to the person**
- Clarity keeps recordings for about 30 days, then only a small sample. Save lead sessions
  as favourites, or log their entry pages in a sheet, every month.
- Clarity shows the entry page of the session that converted. If someone first found a
  programmatic page last week and came back directly to submit, the entry page will be the
  return visit's page.

**Done when:** a test form submission shows up in GA4 as a key event and in Clarity with
the right entry URL.

---

## Step 1.4: CMS access and roles

**What it means:** deciding who can publish, who builds templates, and who approves.

**How to do it:** fill in the roles section of `templates/project-brief.md`:

| Role | Typical owner | Responsibility |
|---|---|---|
| SEO owner | the person running this playbook | strategy, sheets, QA, Search Console, decisions |
| Writer or editor | content team | long-form pieces, reviewing programmatic copy |
| Designer | design team | page layouts and components per page type |
| Developer | web team | CMS fields, templates, breadcrumbs, schema, sitemaps, redirects |
| Approver | founder, CTO or marketing lead | positioning and claims sign-off |

Find out whether the SEO owner can publish in the CMS directly. If every batch needs a
developer, plan for the publishing automation in stage 9 early, because the developer will
otherwise become the bottleneck.

**Done when:** every role has a name, and you know the path from "row in a sheet" to "live
page".

---

## Step 1.5: Make sure crawlers can get in (search and AI)

**What it means:** checking that nothing is blocking Google, Bing or AI assistants from
reading the site.

**Why it matters:** a single line in robots.txt, or a security setting at the hosting or
CDN layer (Cloudflare and similar), can block AI crawlers while the site looks normal to
people. If AI visibility is a goal, this is a five-minute check that can explain zero
citations.

**How to do it**
1. Open yoursite.com/robots.txt. Look for `Disallow` lines under `User-agent: *` or under
   bots such as Googlebot, Bingbot, GPTBot, OAI-SearchBot, PerplexityBot, ClaudeBot,
   Google-Extended.
2. Ask whoever manages hosting or the CDN whether any bot-blocking or "AI crawler" setting
   is switched on, and what it blocks.
3. Decide with the business which AI crawlers to allow. Search-oriented ones (for example
   OAI-SearchBot, PerplexityBot) affect whether you can be cited in AI answers.
4. Check that staging or preview sites are password-protected or set to noindex, so they
   never compete with the live site.

**Done when:** robots.txt allows the bots the business wants, the hosting layer is not
silently blocking them, and staging is hidden.

---

## Step 1.6: Baseline and change log

**What it means:** saving today's numbers and starting a dated list of every change.

**Why it matters:** on real projects, rewrites, sitemap changes and new links often land in
the same few weeks. Without a log nobody can say which change moved the numbers.

**How to do it**
1. Export from Search Console: Performance by page for the last 12 months and last 3
   months, and the Pages (indexing) report with each "not indexed" reason exported
   separately. Save them with the date in the filename.
2. Note the headline numbers in the project brief: indexed pages, not-indexed pages by
   reason, monthly clicks, impressions, leads.
3. Copy `templates/change-log.csv` and add the first entry: "Baseline exported".

**Done when:** the baseline files are saved and the change log exists.

---

## Checkpoint for stage 1

- Search Console and Bing are verified, with the sitemap submitted.
- GA4 and Clarity record a test lead with its entry page.
- Roles are named and the publishing path is known.
- Crawlers are not blocked; staging is hidden.
- Baseline exports and the change log exist.
