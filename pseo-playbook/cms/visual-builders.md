# Publishing on visual builders (Framer, Webflow and similar)

Visual builders are easy for non-technical teams to edit, and their CMS collections suit
programmatic pages well. Their limits are usually around custom schema, breadcrumbs and
sitemap control, so check those before scaling.

## Set up

1. **One CMS collection per page type** (for example "Industry solutions", "Comparisons").
   Add a field for every column in the content sheet tab for that type.
2. **Page template per collection.** The designer builds the layout once and binds each
   section to its field. Optional sections are hidden when their field is empty (both Framer
   and Webflow support conditional visibility).
3. **Slug field** controls the URL. The collection's base path sets the folder
   (`/solutions/`).
4. **Reference fields** link items to other collections: a case study, a parent hub. Use a
   "parent" reference field to drive breadcrumbs and related-pages lists.
5. **Analytics:** paste GA4 and Clarity into the site-wide custom code (head) setting.

## Publishing from the sheet

- **CSV import:** export the sheet tab as CSV and import into the collection. Map columns to
  fields on the import screen. Match on slug to update rather than duplicate.
- **Sync plugins and integrations:** both platforms have plugins or third-party tools that
  sync a Google Sheet or Airtable base into a collection. Check field-type support (rich text,
  references, images) before committing.
- **API (Webflow):** Webflow's CMS API lets a script create and update items, so a Google Apps
  Script or automation tool can publish rows directly.

## SEO settings to check

| Need | What to check |
|---|---|
| Meta title and description | Bind the page settings to CMS fields, not one static value |
| Canonical | Defaults to the page itself; confirm it is not overridden site-wide |
| Schema | Can the builder output a custom code block that uses CMS field values on collection pages? Webflow supports CMS fields inside embeds. If yours cannot, ask the developer for a workaround before scaling |
| Breadcrumbs | Build a breadcrumb component from the parent reference field; add BreadcrumbList to the same schema block |
| XML sitemap | Generated automatically; check that new items appear and that excluded pages are left out. Segmenting by section may be limited, so the HTML sitemap and folder structure carry more of the grouping |
| Redirects | Both offer a redirects panel; keep the redirect map sheet as the master copy |
| Collection limits | Plans cap the number of CMS items. Check the cap against the planned page count before choosing the platform |

## Watch out for

- Desktop and mobile versions of a section built as separate copies. Both copies land in the
  HTML and look like duplicated content. Ask the designer to use one responsive section.
- Text set inside images or animations, which Google cannot read.
- Heavy animations and large images on the template, which slow every page at once.
