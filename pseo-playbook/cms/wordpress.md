# Publishing on WordPress

WordPress has mature tools for almost everything programmatic SEO needs, mostly through
plugins. The main risks are heavy page builders and plugin conflicts.

## Set up

1. **A custom post type per page type** (for example "solutions", "comparisons"), registered
   by the developer or with a plugin such as Custom Post Type UI. Each gets its own URL base.
2. **Custom fields** for each content sheet column, usually with Advanced Custom Fields (ACF).
   ACF's flexible content field (Pro) lets editors add, remove and reorder sections, so pages
   of the same type do not have to share one rigid layout.
3. **A template per post type** that renders the fields in the page anatomy order.
4. **A parent field or taxonomy** to drive breadcrumbs, hub listings and related pages.

## Publishing from the sheet

- **Import plugins** such as WP All Import read a CSV or Google Sheet and create or update posts,
  including ACF fields. Set the unique identifier to the slug so re-imports update.
- **REST API:** a script can create and update posts using an application password created
  for a dedicated user with the minimum role needed. ACF fields need to be exposed to the REST
  API.

## SEO plugin (Yoast SEO, Rank Math or similar)

Use one SEO plugin, not two. It typically handles:
- meta title, description, canonical and robots per page (map them from the sheet on import)
- XML sitemaps split by post type automatically
- breadcrumbs with BreadcrumbList schema
- base schema output, which the developer can extend into one @graph

Redirects: the SEO plugin or a dedicated redirection plugin, fed from the redirect map.

## Watch out for

- Page builders that output each section twice for desktop and mobile, or wrap content in
  heavy markup. Check View Page Source on the template before scaling.
- Tag and category archives, author archives and attachment pages creating thin indexable
  pages. Set them to noindex if they are not useful.
- Plugin updates changing output. Re-run the launch checker on a sample after major updates.
- Migrations off WordPress: export a complete URL list first and plan the redirect map before
  the move.
