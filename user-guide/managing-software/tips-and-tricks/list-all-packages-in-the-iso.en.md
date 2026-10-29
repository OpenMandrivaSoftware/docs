---
layout: default
title: List All Packages in the ISO
nav_order: 40
parent: Tips and Tricks
has_toc: true
lang: en
---

# List All Packages in the ISO

When booted from a Live ISO, you can generate a complete list of all packages included in the image. This is useful for comparing what ships in the ISO with what is installed on your system.

## List All Packages Alphabetically

Open a terminal and run this command:

```bash
$ rpm -qa | sort > pkglist-sort.txt
```

This creates a text file named `pkglist-sort.txt` in your home directory, listing all installed packages sorted alphabetically.

![A terminal window shows the sorted package list saved to a text file in the home directory.](./images/list-all-packages-in-the-iso-01.jpg)

This trick works in both Live ISO mode and on an installed system. You can run the command any time you need a package list.

## List Packages by Installation Date

To sort the list by installation date instead of alphabetical order, run this command:

```bash
$ rpm -qa --last > pkglist-last.txt
```

## Related Topics

- [Listing Installed Packages](./index.en.html)
- [List the Latest Updates](./list-the-latest-updates.en.html)
- [Using DNF](../index.en.html)
