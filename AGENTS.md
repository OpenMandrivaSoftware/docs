# Agent Documentation

This repository contains the documentation site for the OpenMandriva Linux distribution.

## Technical Stack
- **Static Site Generator:** Jekyll
- **Theme:** [Just the Docs](https://github.com/just-the-docs/just-the-docs)
- **Customization:** Custom CSS and Liquid templates.

## Custom Implementations
This site includes several custom modifications to the base theme. For detailed instructions on how these were implemented and how to maintain them, please refer to the skills documented in the `.agents` directory:

- [Cards Functionality](./.agents/cards/): Implementation of the dynamic home page cards.
- [Layout Customizations](./.agents/layout/): Overrides for the theme's default centering and width constraints.
- [Multilingual Support](./.agents/multilingual/): Multilingual implementation with the jekyll-polyglot plugin.
- [Removable Theme Footer](./.agents/remove-theme-footer/): Removing the default theme footer messages.
- [Right Sidebar (Page TOC)](./.agents/right-sidebar/): Right sidebar that displays a table of contents.

## Images 

In this site, 

- Images that are global, reusable images go in `./assets/images`. 
- Images that go with their individual documentation are stored in a subfolder called `./images` wherever that documentation is. 
- Images that go with their individual documentation should be named the same as their documentation file but numbered sequentially in the order they appear in the file. For example, if the file they go with is `installing-openmandriva.en.md`, images should be named `installing-openmandriva-01.png`, `installing-openmandriva-02.png`, etc. 
- Resize all images wider than 800px to 800px wide, keeping the aspect ratio. 

Use `./getting-started/installing-openmandriva.en.md` as an example. 

## Writing 

When asked to write or edit content, always load the technical writing skills you find, either globally or in this project, to mimic the operator's voice *before* you start writing or editing. 

## Writing Overrides 

This platform (Jekyll) and this theme (Just the Docs) generates a Table of Contents at the bottom of every file that has children. Therefore, do not generate Related Topics headings on these pages. Generate Related Topics only on leaf nodes (files that have no children in the navigation). 

## Multilingual Grep Scoping

This repository uses language-specific file suffixes (`.en.md`, `.fr.md`, `.pt.md`, `.ja.md`). The technical writing skills use generic grep patterns (`--include="*.md"`). When running those greps against this repository, override the include pattern to scope to English only:

```bash
grep -rnE '<pattern>' --include="*.en.md" .
```

This prevents false positives from non-English content that the English-language writing rules do not apply to.

## File Naming Conventions

Files should be named the same as their titles, using hyphen case. For example, a Markdown with the title "Downloading OpenMandriva" should be in a file called `downloading-openmandriva.en.md`. Similarly, a file titled "Copying OpenMandriva to a USB Stick" should have the file name `copying-openmandriva-to-a-usb-stick.en.md`. 

If you find files names that do not match their titles, offer to rename them, and then scan the rest of the repository for links to the old file name (which will have a `.en.html` extension, as Jekyll converts the Markdown to HTML when publishing) and fix them. 

The exception to this rule is when you have a hierarchy. A parent file's children go in a directory named for that parent file. For example, a file called `installing-openmandriva.en.md` that has children should have a corresponding subdirectory next to the file called `installing-openmandriva`. The "first-born child," or the first child in the navigation becomes `index.en.md` in this directory, and the rest of the children are named according to their titles like normal. 

## Callouts

This theme uses [Just the Docs callouts](https://just-the-docs.com/docs/ui-components/callouts/), which require kramdown **block IALs** (`{: .TYPE }`) — not Markdown blockquotes with bold labels (e.g., `> **Note**`). The available callout types are configured in `_config.yml`:

| Type | Title | Use for |
| --- | --- | --- |
| `note` | Note | Supplementary information |
| `warning` | Warning | Potentially harmful actions |
| `important` | Important | Critical instructions |
| `tip` | Tip | Helpful shortcuts or best practices |

### Syntax

Place the `{: .TYPE }` IAL **before** the content it styles. For a single paragraph:

```
{: .note }
This is a note.
```

For multi-line content, combine with blockquote syntax:

```
{: .warning }
> This is a warning.
>
> This is a second paragraph.
```

## Package References

Always verify DNF package names against the OpenMandriva package database at [pkgs.org](https://pkgs.org). Do not assume package names from other distributions (e.g., Fedora's `gstreamer1.0-codec-installer` does not exist in OpenMandriva). Search by distribution to confirm:
- `gstreamer1.0-plugins-ugly` — in the Restricted repository
- `gstreamer1.0-libav` — in the Main repository
- `lib64dvdcss` — in the Restricted repository
