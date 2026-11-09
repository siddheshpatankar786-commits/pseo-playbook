# Publishing on a headless CMS (Strapi, Contentful, Sanity and similar)

A headless CMS stores content and serves it through an API; a separate front-end (often
Next.js or similar) builds the pages. This gives full control and easy automation, but every
SEO feature has to be built on purpose by the developer.

## Set up

1. **One content type per page type**, with a field per content sheet column.
2. **Relations:** a "parent" relation (for breadcrumbs and hubs), a "case study" relation, and
   optionally "related pages".
3. **An SEO component** reused across content types: meta title, meta description, canonical,
   robots, focus keyword.
4. **Front-end rendering:** confirm with the developer that pages are rendered on the server or
   built ahead of time, so content, links and FAQs appear in the page source. Content fetched
   in the browser after load is a common reason pages look thin to Google.

## Publishing from the sheet (example: Google Sheets to Strapi)

A Google Apps Script attached to the sheet reads approved rows and sends them to the CMS
REST API.

1. The developer creates an API token with create and update permissions on the content types
   needed, and nothing else. The token goes into the script's Script Properties, never into a
   sheet cell.
2. The script looks up each row's slug. If an entry exists, it updates it; if not, it creates
   one.
3. New entries are created as drafts for review.
4. The script writes the entry ID, status and date back to the row.

**Problems hit in practice with Strapi, and their fixes**
- **Drafts not created as drafts (Strapi v5):** the draft status had to be sent as a query
  parameter on the request (`?status=draft`), not only in the body.
- **403 Forbidden errors:** the API token lacked permission for that content type or action.
  Fix the token's permissions in the admin panel.
- **Old values surviving updates:** partial updates merged with stale field values. A "full
  overwrite" mode that sends every field on update fixed it.

## SEO features the developer must build

| Need | How |
|---|---|
| Meta tags and canonical | Rendered from the SEO component in the page head |
| Schema | One JSON-LD @graph generated per page from fields (see stage 7) |
| Breadcrumbs | Walk the parent relation up to the top; render the visible trail and BreadcrumbList from the same data |
| XML sitemaps | Generated from the API: a sitemap index plus one sitemap per content type, with lastmod from the entry's real update date |
| Redirects | Managed in the front-end config or the hosting layer from the redirect map |

## Watch out for

- Placeholder values pasted into SEO fields (for example a canonical or Open Graph field
  holding sample text). Make canonical default to the page URL when the field is empty.
- Preview or staging front-ends being indexed. Keep them behind a password or noindex.
- Changing a content type's fields after hundreds of entries exist. Plan fields with the
  page anatomy first (stage 7).
