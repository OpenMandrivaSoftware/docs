---
layout: default
title: Understanding RPM Spec Files
nav_order: 30
parent: Developer Docs
has_toc: true
lang: en
---
# Understanding RPM Spec Files

An RPM package is defined by a *specification file* (`.spec`) that describes how to build a piece of software. Spec files range from simple to complex depending on what you are building. The RPM packaging guide and Red Hat's packaging blog cover the format in depth:

- [RPM Packaging Guide](https://rpm-packaging-guide.github.io)
- [Create your first RPM](https://www.redhat.com/en/blog/create-rpm-package)

## Creating a Spec File

Use the appropriate `v*` tool from `packaging-tools` to generate a template for your package type. You can find the available tools in [Installing Packaging Tools](./preparing-your-system/packaging-tools.en.html).

As you learn to write spec files, start with an existing `.spec` file from another RPM-based distribution. Because OpenMandriva is its own distribution and not descended from any others, the `spec` file must be modified to work.

When you run a `v*` tool, the tool creates the `.spec` file in `~/abf/[package-name]`. Work from that directory throughout the build process.

## What a Spec File Contains

A `v*` tool creates a template with most values pre-filled. A basic spec file looks like this:

```
Name:       mypackage
Version:    1.0.0
Release:    1
Summary:    A short description
License:    MIT
Source0:    https://example.com/mypackage/mypackage-1.0.0.tar.xz

BuildSystem: autotools

%description
A longer description of what the package does.
```

The top fields describe the package: `Name`, `Version`, `Release`, `Summary`, `License`, and source files.

The sections tell the build system what to do during each phase:

`%prep`: unpacks and prepares the source code.

`%build`: compiles the software.

`%install`: copies built files into a temporary install directory (typically runs `make install`).

`%check`: runs the test suite (for example, `make check`).

`%files`: lists every file the package installs.

`%changelog`: records changes to the package.

The `BuildSystem:` directive tells the build system how to compile your software. For example, `BuildSystem: autotools` makes the build invoke `./configure` and `make`.

## Related Topics

- [Installing Packaging Tools](./preparing-your-system/packaging-tools.en.html)
- [Building and Submitting Packages](./building-and-submitting-packages.en.html)
