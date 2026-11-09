# CMS requirements checklist

Go through this with the developer before building any page type. Mark each line Yes,
Yes with work (add an estimate), or No (add the workaround).

| # | Capability | Why it matters, in plain words | Answer |
|---|---|---|---|
| 1 | A separate collection or content type per page type | Each page type has different fields and layouts | |
| 2 | Control over the slug and folder of each page | URLs must follow the agreed pattern | |
| 3 | Editable meta title and meta description per page | Every page needs its own search result text | |
| 4 | Editable canonical and robots per page, defaulting to self and index | Prevents pages accidentally pointing elsewhere or hiding from Google | |
| 5 | Schema output generated from fields as one JSON-LD @graph | Describes each page to search engines without hand-typing | |
| 6 | Breadcrumbs generated from a parent field (visible trail and schema from the same data) | Gives every page a home address that never drifts out of sync | |
| 7 | A related-pages block filled automatically from the same parent | Every page gets sibling links without manual work | |
| 8 | Hub pages that list their children automatically | New children appear on their hub the moment they publish | |
| 9 | Automatic XML sitemap with real lastmod dates, split by section | Google sees new and changed pages, grouped by type | |
| 10 | Bulk import from a sheet (CSV) or API publishing | Publishing hundreds of pages without copying by hand | |
| 11 | Draft and publish status | Pages can be reviewed before going live | |
| 12 | Flexible sections that can be added, removed or reordered per page | Pages of the same type do not all look identical | |
| 13 | Content, links and FAQs present in the page source (server-rendered) | Google reads the source; content loaded later may be missed | |
| 14 | One responsive version of each section (not separate desktop and mobile copies) | Duplicated blocks look like repeated content | |
| 15 | Redirect management (301 and 410) | Cleanup and future changes without losing value | |
| 16 | Site-wide custom code for analytics (GA4, Clarity) | Tracking visits and leads by page | |
| 17 | Staging or preview kept out of search (password or noindex) | Avoids duplicate copies of the site in Google | |
| 18 | Page speed acceptable on the template (PageSpeed Insights) | One slow template means hundreds of slow pages | |
