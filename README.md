# pSEO playbook (Claude skill)

A beginner-friendly, end-to-end programmatic SEO playbook packaged as a Claude skill. It
walks someone from zero to live, indexed programmatic pages: site inventory, cleanup of
unindexed template pages, pillar and content hierarchy, breadcrumbs and internal linking,
page design and developer/designer handoffs, content sheets, publishing to the CMS, launch
checks, indexing and measurement.

## What's in it

- `pseo-playbook/SKILL.md`: intake, Build and Fix tracks, stage map, ground rules
- `pseo-playbook/stages/`: 12 step-by-step stages, each explained in plain words
- `pseo-playbook/cms/`: guides for visual builders, headless CMSs, WordPress and custom sites
- `pseo-playbook/library/`: page types, reference gallery, troubleshooting, field notes
- `pseo-playbook/templates/`: briefs, checklists and sheet templates
- `pseo-playbook/scripts/`: Python 3 scripts for URL grouping, Search Console triage,
  near-duplicates, internal links, sitemaps, content sheet QA and launch checks

## Install

- **Claude.ai:** download `pseo-playbook.skill` from the releases (or zip the
  `pseo-playbook` folder) and upload it in the skills section of Claude's settings.
- **Claude Code:** copy the `pseo-playbook` folder into `~/.claude/skills/`.

## Scripts

Each script runs with Python 3 and explains its options with `--help`. Only
`near_duplicates.py` and `sheet_qa.py` benefit from scikit-learn, and both fall back to
plain Python without it.
