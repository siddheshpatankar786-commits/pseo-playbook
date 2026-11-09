# Stage 9: Publishing

**Purpose:** get approved rows from the content sheet into the CMS reliably, without someone
copying and pasting every field by hand.

On one build-from-zero project, moving from manual publishing (about 10 minutes per page)
to a sheet-to-CMS pipeline cut publishing to seconds per page. That is what makes steady
batches possible without a developer for every release.

---

## Step 9.1: Choose the publishing method

| Method | How it works | Good for | Watch out for |
|---|---|---|---|
| Manual entry | Copy fields into the CMS | Under about 30 pages, or the test batch | Slow, typos, inconsistent fields |
| CSV import | Export the sheet tab as CSV, import into the CMS collection | Visual builders and WordPress import plugins | Re-imports can create duplicates if not matched by slug |
| Sheet-to-CMS automation | A script or connector reads the sheet and creates or updates entries through the CMS API | Steady batches, frequent updates | Needs a developer once to set up keys and field mapping |
| Sync tools | A third-party tool keeps a sheet or Airtable in sync with the CMS | Teams without a developer | Monthly cost, check field support |

Read the platform guide that matches the site:
- Framer, Webflow and similar: `cms/visual-builders.md`
- Strapi, Contentful, Sanity and other headless CMSs: `cms/headless.md`
- WordPress: `cms/wordpress.md`
- Custom-built sites: `cms/custom.md`

**Done when:** a method is chosen and the developer agrees to set up whatever access it
needs.

---

## Step 9.2: Map sheet columns to CMS fields

**What it means:** a two-column table: sheet column on the left, CMS field on the right.
Every column the page needs must have a home.

**How to do it:** list the CMS fields (the developer can export the collection's field
list), match them to the content sheet columns, and note any field format differences:
rich text versus plain text, a reference to another collection (for example a case study),
image fields, dates.

**Done when:** every content and SEO column maps to a field, and nothing on the page is left
to be filled by hand after import.

---

## Step 9.3: Safety rules for any pipeline

1. **Create as draft first.** New entries land as drafts; someone checks a few in the CMS
   preview before publishing the batch.
2. **Match on slug.** The pipeline updates an existing entry when the slug exists and creates
   one only when it does not. This prevents duplicates on re-runs.
3. **Full overwrite on update.** When updating, send every field, so an old value in a field
   left blank in the sheet does not quietly survive.
4. **Write back status.** The pipeline writes "published", the date and the CMS entry ID back
   to the sheet row.
5. **Keep keys private.** API tokens live in the script's secure settings, never in the sheet
   or in shared docs. Give the token only the permissions it needs.
6. **Log every run** in the change log.

**Done when:** a test run on 2 or 3 rows creates drafts with every field filled correctly,
and a second run updates them without creating duplicates.

---

## Step 9.4: Publish the batch

1. Run the pipeline on the approved rows (qa_status = passed, reviewer filled).
2. Spot-check at least three drafts in the CMS preview, one per section layout.
3. Publish.
4. Run the stage 10 launch checks straight away.

## Checkpoint for stage 9

Publishing method set up, field mapping complete, safety rules in place, and a first batch
published and checked.
