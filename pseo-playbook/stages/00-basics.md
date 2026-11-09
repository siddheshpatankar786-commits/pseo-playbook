# Stage 0: Basics in plain words

Use this stage to make sure the person and you mean the same thing by each word. Do not
read the whole list out. Explain a term the first time it comes up in a later stage, using
the plain version below, and come back here when they ask.

## What programmatic SEO actually is

**Plain words:** instead of writing every page from scratch, you design a page type once
(for example "our software for [industry]"), collect the information for each version in a
spreadsheet, and publish many pages from that sheet. Each row becomes one page.

**What it is not:** swapping a keyword into the same text hundreds of times. Search engines
treat that as spam, and it usually ends with most pages ignored or the whole site trusted
less.

**Everyday comparison:** a good programmatic page is like a product spec sheet in a
catalogue. The layout repeats, but each sheet describes a genuinely different product.

## Words about getting found

| Term | Plain meaning |
|---|---|
| **Crawling** | Google's bot visiting a page and reading it. |
| **Indexing** | Google deciding to store the page so it can appear in search results. A page can be crawled and still not indexed. |
| **Crawled - currently not indexed** | Google visited the page and decided it was not worth storing for now. Usually a quality or duplication signal. |
| **Discovered - currently not indexed** | Google knows the URL exists but has not bothered to visit yet. Usually a priority or site trust signal. |
| **Search Console (GSC)** | Google's free dashboard showing which pages are indexed, what people searched, and problems found. |
| **Bing Webmaster Tools** | Bing's version. It also reports how often pages are cited in Bing's AI answers. |
| **Impressions / clicks / position** | How often a page appeared in results, how often it was clicked, and its average rank. |
| **Request indexing** | A button in Search Console that asks Google to visit a page soon. It is a request, not a guarantee, and has a small daily limit. |

## Words about page settings

| Term | Plain meaning |
|---|---|
| **Meta title / meta description** | The headline and short summary shown in search results. Set in the CMS, not visible on the page. |
| **H1, H2** | The main heading of the page, then section headings. |
| **Canonical tag** | A hidden note saying "this is the main version of this page". Normally a page points to itself. If it points somewhere else, Google may ignore the page. |
| **Noindex** | A hidden instruction telling Google "do not put this page in search results". Useful for private pages, harmful when left on by mistake. |
| **Schema (structured data)** | Hidden labels in a standard format (JSON-LD) that describe the page to search engines: what kind of page it is, its breadcrumb, its FAQs. |
| **@graph** | A way to put all of a page's schema in one block where the pieces reference each other. One script per page, not several. |

## Words about moving and removing pages

| Term | Plain meaning |
|---|---|
| **301 redirect** | A permanent forward. Anyone (and Google) visiting the old address is sent to the new one, and most of the old page's value moves with them. |
| **404** | "Page not found." Fine for pages that never mattered. |
| **410** | "Gone on purpose." Tells Google more firmly that the page was removed. |
| **Redirect chain** | A forward to a forward. Slows things down and leaks value. Always point straight to the final page. |
| **Soft 404** | A page that technically exists but looks empty or irrelevant to Google, or a redirect to an unrelated page. Google treats it like a 404. |

## Words about site structure

| Term | Plain meaning |
|---|---|
| **XML sitemap** | A machine-readable list of the pages you want indexed, with the date each was last changed (lastmod). Submitted in Search Console. |
| **HTML sitemap** | A normal web page listing the site's pages for people, grouped by topic. |
| **Hub page / parent page** | A page that introduces a topic and links to all the more specific pages under it. |
| **Pillar** | One of the few big topics the company wants to be known for. Each pillar has a pillar page and layers of supporting pages (stage 5). |
| **Breadcrumb** | The page's home address shown above the heading, like Home › Solutions › Healthcare. One per page. |
| **Internal links** | Links from one page of your site to another. They are the roads that lead to a page. A page has one home address but can have many roads. |
| **Inbound internal links** | Links pointing to a page from other pages on your site. These are what tell Google the page matters. Links on the page pointing outward help the other pages, not this one. |
| **Orphan page** | A page no other page links to. Google rarely finds or values it. |
| **Anchor text** | The clickable words of a link. They tell Google what the linked page is about. |

## Words about content quality

| Term | Plain meaning |
|---|---|
| **Thin content** | A page with little real substance, often mostly boilerplate shared with other pages. |
| **Near-duplicate** | Two pages so similar that Google picks one and ignores the other. |
| **Cannibalization** | Two of your own pages competing for the same search, so neither ranks well. |
| **Scaled content abuse** | Google's spam policy against publishing many pages mainly to rank rather than to help people. The method (AI, template, human) does not matter; the lack of value does. |
| **E-E-A-T** | Experience, Expertise, Authoritativeness, Trust: the signals Google's guidelines use to judge whether content comes from people who know the subject. |

## Words about tracking

| Term | Plain meaning |
|---|---|
| **GA4** | Google Analytics 4. Counts visitors, where they came from, and conversions. |
| **Microsoft Clarity** | Free session recordings and heatmaps. Shows the page each visitor entered on, so it can link a form submission to the programmatic page that started the visit. |
| **Conversion / lead** | The action that matters to the business, usually a form submission or demo request. |
| **Server logs** | The website server's own record of every visit, including Google's bot. The most direct proof of how often Google crawls each section. |
| **AI citations** | Times an AI assistant (ChatGPT, Perplexity, Gemini, Claude, Copilot) referenced your page in an answer. |

## Checkpoint

The person can explain, in their own words, the difference between crawled and indexed,
between a breadcrumb and an internal link, and between a 301 and a 410. If not, revisit
those three before stage 1.
