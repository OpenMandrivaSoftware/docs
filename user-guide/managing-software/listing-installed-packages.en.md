---
layout: default
title: Listing Installed Packages
nav_order: 70
parent: Managing Software
has_toc: true
lang: en
---

# Listing Installed Packages

Check which packages are included in your OpenMandriva installation---for example, to compare a live USB with your installed system or to audit what ships in the ISO.

## Generate a Sorted Package List

In a terminal, run:

```bash
rpm -qa | sort > pkglist-sort.txt
```

This creates a text file named `pkglist-sort.txt` in your home directory, listing all installed packages sorted alphabetically.

![A sorted package list shows all installed packages alphabetically in a text file.](./images/listing-installed-packages-01.jpg)

{: .note }
> This trick works on installed systems too---not just in live or ISO mode. You can run the command any time you need a package list.

## List Packages by Installation Date

To sort the list by installation date instead of alphabetical order, run this command:

```bash
rpm -qa --last > pkglist-last.txt
```

## Related Topics

- [Using DNF](./index.en.html)
- [Maintaining Your System](../maintaining-your-system.en.html)
