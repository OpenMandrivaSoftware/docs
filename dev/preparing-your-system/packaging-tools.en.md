---
layout: default
title: Installing Packaging Tools
nav_order: 30
parent: Preparing Your System
has_toc: true
lang: en
---
# Installing Packaging Tools

The `packaging-tools` package provides everything you need to create and build RPM packages on OpenMandriva. It includes spec file templates and the build tools that connect to the ABF build system.

## Install packaging-tools

Install the packaging tools with DNF:

```bash
sudo dnf install packaging-tools
```

This installs the `abb` build tool, the `abf` submission tool, and the `v*` template utilities described below.

## The v\* Template Tools

The `v*` tools create spec file templates with commonly used fields pre-filled. Each tool loads a template appropriate for a specific type of software package.

`vs`: opens a spec file template for general applications. By default it opens in Vim, but it respects the `$EDITOR` and `$VISUAL` environment variables.

`vl`: loads a template for libraries.

`vp`: loads a template for Python modules.

`vpl`: loads a template for Perl modules.

`vj`: loads a template for Java libraries.

`vo`: loads a template for GNU Octave packages.

To create a new spec file, run the tool that matches your package type:

```bash
vs [package-name]
```

The tool creates a `.spec` file in `~/abf/[package-name]`. Work from that directory throughout the build process.

## Related Topics

- [Understanding RPM Spec Files](../understanding-rpm-spec-files.en.html)
- [Preparing Your System](../preparing-your-system.en.html)
- [Building and Submitting Packages](../building-and-submitting-packages.en.html)
