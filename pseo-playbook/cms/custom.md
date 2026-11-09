# Publishing on a custom-built site

When the site is custom code with no CMS, every capability in
`templates/cms-requirements.md` has to be built. Treat that checklist as the specification.

## What to ask the developer for

1. **A data source per page type:** a database table, JSON files or a lightweight admin.
   The content sheet columns define the fields.
2. **An import path** from the content sheet: a CSV upload screen or a script that reads the
   sheet, updates by slug, and creates new pages as drafts.
3. **Server-side rendering** so all content, links and FAQs are in the page source.
4. **Per-page SEO fields** in the page head: meta title, description, canonical, robots.
5. **Schema** as one JSON-LD @graph generated from fields.
6. **Breadcrumbs** generated from a parent field, visible trail and schema from the same data.
7. **Sitemaps** generated automatically: an index plus one sitemap per page type with real
   lastmod dates.
8. **Related pages** block filled from the same parent.
9. **Redirect handling** from a maintained redirect list.
10. **Draft status**, so pages can be reviewed before going live.

## How to brief it

Use `templates/developer-brief.md` for each page type and attach the CMS requirements
checklist. Ask for an estimate per item; build the breadcrumb, schema and sitemap pieces
before the first batch, not after.

## Watch out for

- "We will add SEO later." Retrofitting breadcrumbs, schema and sitemaps onto hundreds of live
  pages costs far more than building them into the template.
- Client-side frameworks that render content only in the browser. Confirm rendering with URL
  Inspection's crawled HTML before launch.
