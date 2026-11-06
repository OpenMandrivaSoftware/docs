---
name: Navigation
description: This Jekyll site uses the Just the Docs theme which automatically generates sidebar navigation based on page frontmatter hierarchy. Understanding the navigation structure is key to organizing documentation properly.
---

# Sidebar Navigation Implementation

This document describes how sidebar navigation works in the Just the Docs theme and important lessons learned for creating maintainable page hierarchies.

## Key Concept: Page Hierarchy

Just the Docs generates sidebar navigation from page frontmatter `parent:` fields and directory structure. The theme:
- Uses `nav_order:` to determine the display order of items
- Uses `parent:` to create nested navigation structure (must match the **exact title** of the parent page)
- Automatically discovers children based on file location and parent references

## Critical Rule: Section Index Pages Must NOT Have a Parent

**Problem Encountered**: When section index pages have `parent: SectionName`, it creates a circular reference that breaks navigation generation.

**Examples of BROKEN config**:
```yaml
# DON'T DO THIS - Creates circular reference
---
title: User Guide
nav_order: 20
parent: User Guide  # ← WRONG! This page is the section root
---
```

**Correct config for section indices**:
```yaml
# CORRECT - No parent for section root
---
title: User Guide
nav_order: 20
# No parent field - this is a top-level section
---
```

### Files That Must NOT Have Parents
These are section/root index files that appear as top-level navigation items:
- `getting-started/index.en.md` (title: "Getting Started")
- `user-guide/index.en.md` (title: "User Guide")
- `dev/index.en.md` (title: "Developer Docs")
- `community/index.en.md` (title: "OpenMandriva Community")

### Files That SHOULD Have Parents
These are children within sections. The `parent:` value must match the **exact title** of the parent page:
```yaml
# Example: A page under User Guide that should be nested
---
title: Network Configuration
nav_order: 30
parent: User Guide  # Must EXACTLY match the parent page's title
has_toc: true
---
```

## Parent Files and Child Directories

Each section may contain **parent files**---regular markdown files (`*.en.md`)
that act as landing pages for a group of related child pages. When a parent
file has children, a **child directory** with the same name (minus `.en.md`)
is created to hold the child pages.

The parent file:
- Has `card_columns:` and a `cards:` frontmatter list pointing to its children
- Contains `{% include section_cards.html %}` in its body
- Its `parent:` field points to the section index (e.g., `parent: User Guide`)

Children in the child directory:
- Have their own `nav_order:` values that determine their position in the navigation
- Have `parent:` set to the **parent file's** title (e.g., `parent: Managing Software`)
- Are named by their own titles, following the file naming convention

### Parent File vs. Card URL Format

- **Section landing page cards** point to the parent file: `/user-guide/managing-software.en.html`
- **Parent file's own cards** point to child files: `/user-guide/managing-software/index.en.html`

Card URLs in section index files (e.g., `user-guide/index.en.md`) should
target the parent file (`.en.html`)---**not** the child directory's `index.en.html`.
The parent file is the section landing page; its cards point to the child pages.

## Navigation Structure

The sidebar shows 5 top-level sections:

1. **Home** - Link to index.en.html
2. **Getting Started** - Expanded by default with sub-items
   - System Requirements
   - Downloading OpenMandriva
   - Copying OpenMandriva to a USB Stick
   - Installing OpenMandriva → (expandable)
     - Partitioning
     - Disk Encryption
     - Partitioning Schemas
3. **User Guide** - Expandable with nested content
   - Maintaining Your System → (expandable)
     - Update Your System
     - Switch Update Channels
     - List Recent Updates
     - Compile Custom Software
   - Managing Software → (expandable)
     - Using DNF
     - Software Repository Selector
     - DnfDrake Overview
     - List Packages in the ISO
     - OpenMandriva Welcome
     - Install Steam
   - Post Installation Configuration → (expandable)
     - Set Your User Avatar
     - Restore Your Files After Installation
     - Configure a Printer
   - First Ten Tasks After Installation
   - Desktop Environments
   - Network Configuration
   - Troubleshooting → (expandable)
     - Fix a Broken Bootloader
     - Connect to the Internet in Recovery Mode
     - Fix Incorrect Time in Dual Boot
4. **Developer Docs** - Expandable with technical content
   - Build System
   - How to Build and Submit Packages
   - OpenMandriva Cooker
   - Contributing to OpenMandriva
   - How to Report a Bug
   - Getting Started with QA → (expandable)
     - Bug Report Tool
     - Release QA Checklist
     - Report Bugs Effectively
5. **OpenMandriva Community** - Expandable with nested content
   - Chat with OpenMandriva
   - About OpenMandriva → (expandable)
     - Bylaws
     - Governance
     - Statutes
   - Artwork
   - Donation
   - Links
   - Releases → (expandable)
     - Release Plan and Repositories
     - Repository Policies
     - Release Life Cycle
     - Setting Up a Mirror
     - Release Codenames
   - Official Naming Policy
   - Trademark License
   - Terms of Service

## File Naming Convention

Per the Jekyll Polyglot setup,
- Extensionless `.md` files (no `.en` suffix) → render to `{slug}.html`
- `.en.md` files → render to `{slug}.en.html`

For sidebar links,
- Section indices like `getting-started/index.en.md` → `/getting-started/index.en.html`
- Pages use relative links based on current file location

## Determining Correct URLs

To determine the correct relative path for a link in a markdown file,

### Step 1: Identify the Source File Location
Note the full path of the file containing the link. For example,
- `user-guide/desktop.en.md` → located in `/docs/user-guide/`

### Step 2: Identify the Target File Location
Note the full path of the target file. For example,
- `getting-started/downloading-openmandriva.en.md` → located in `/docs/getting-started/`

### Step 3: Calculate the Relative Path

To calculate the relative path from a source file to a target file,

**Example: From `user-guide/desktop.en.md` to `getting-started/downloading-openmandriva.en.md`**
- From `user-guide/` directory, you need to go up one level to reach `docs/`
- Then descend into `getting-started/` and access the file
- Relative path: `../../getting-started/downloading-openmandriva.en.html`
  - `..` (from `user-guide` to `docs`)
  - `../getting-started/` (down into `getting-started`)
  - `downloading-openmandriva.en.html` (the target file with correct extension)

### Step 4: Apply URL Extension
Always use the `.en.html` extension for English pages, not `.md`.

**Common Patterns:**
- Same directory: `./page.en.html` or just `page.en.html`
- Parent directory: `../page.en.html`
- Sibling directory: `./sibling/page.en.html`

**Example: Linking to a sibling section**
If you're in `user-guide/managing-software/software-repository-selector.en.md` and want to link to `managing-software.en.md` in the parent `user-guide/` directory:
- Source: `user-guide/managing-software/software-repository-selector.en.md`
- Target: `user-guide/managing-software.en.md`
- Relative path: `../managing-software.en.html` (go up from `managing-software/` to `user-guide/`, then access `managing-software.en.md`)

### Step 5: Verify the Link
Before committing, verify the target file exists at the calculated path.

## Common Pitfalls

### 1. Circular Parent References
**Symptom**: Section doesn't appear in sidebar, or navigation breaks
**Fix**: Ensure section root pages have no `parent` field

### 2. Wrong Parent Title Reference
**Symptom**: Child pages don't nest properly under the correct parent
**Fix**: The `parent:` value must match the **exact title** of the parent page
```yaml
# WRONG - Parent title is "OpenMandriva Community"
parent: Community  # Won't match!

# CORRECT
parent: OpenMandriva Community  # Matches exactly
```

### 3. Broken Internal Links
**Symptom**: Links lead to 404 errors
**Fix**: 
- Use `.en.html` extension for English pages
- Use relative paths (e.g., `./how-to-build-and-submit-packages.en.html` not `./packaging.md`)
- Check that target files exist before linking

### 4. Missing Pages for Home Cards
**Symptom**: Home card links point to non-existent pages
**Fix**: Create the required pages before adding cards to `home_cards.yml`

## Creating New Sections

To add a new documentation section:

1. Create a new directory under `/docs/` (e.g., `new-section/`)
2. Create an `index.en.md` file with NO `parent` field
3. Set appropriate `nav_order` value
4. Set `title` to the section name
5. Create child pages with `parent: Exact Title of Section` (must match the section index title)
6. Update `home_cards.yml` if adding to home page cards

### Example Section Index (CORRECT):
```yaml
---
layout: default
title: Your New Section
nav_order: 25
has_toc: true
lang: en
---
# Your New Section

Welcome to the documentation.
```

### Example Child Page (CORRECT):
```yaml
---
layout: default
title: Sub Page
nav_order: 10
parent: Your New Section  # Must EXACTLY match the section index title
has_toc: true
lang: en
---
# Sub Page

Content here.
```
