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

## Writing 

When asked to write or edit content, always load the technical writing skills you find, either globally or in this project, to mimic the operator's voice *before* you start writing or editing. 

## Writing Overrides 

This platform (Jekyll) and this theme (Just the Docs) generates a Table of Contents at the bottom of every file that has children. Therefore, do not generate Related Topics headings on these pages. Generate Related Topics only on leaf nodes (files that have no children in the navigation). 

## Package References

Always verify DNF package names against the OpenMandriva package database at [pkgs.org](https://pkgs.org). Do not assume package names from other distributions (e.g., Fedora's `gstreamer1.0-codec-installer` does not exist in OpenMandriva). Search by distribution to confirm:
- `gstreamer1.0-plugins-ugly` — in the Restricted repository
- `gstreamer1.0-libav` — in the Main repository
- `lib64dvdcss` — in the Restricted repository
