---
layout: default
title: Listing Installed Packages
nav_order: 10
parent: Tips and Tricks
page_id: user-guide.managing-software.tips-and-tricks.listing-installed-packages
parent_id: user-guide.managing-software.tips-and-tricks
lang: en
source_lang: en
permalink: /user-guide/managing-software/tips-and-tricks/listing-installed-packages/
redirect_from:
- /user-guide/managing-software/tips-and-tricks/listing-installed-packages.en.html
has_toc: true
---
# Listing Installed Packages

Check which packages are included in your OpenMandriva installation, for example, to compare a live USB with your installed system or to audit what ships in the ISO.

## Generate a Sorted Package List

In a terminal, run this command:

```bash
$ rpm -qa | sort > pkglist-sort.txt
```

This creates a text file named `pkglist-sort.txt` in your home directory, listing all installed packages sorted alphabetically.

![A sorted package list shows all installed packages alphabetically in a text file.](../images/listing-installed-packages-01.jpg)

{: .note }
This trick works on installed systems too---not only in live or ISO mode. Run the command any time you need a package list.

## List Packages by Installation Date

To sort the list by installation date instead of alphabetical order, run this command:

```bash
$ rpm -qa --last > pkglist-last.txt
```

## Related Topics

- [List the Latest Updates](/user-guide/managing-software/tips-and-tricks/list-the-latest-updates/)
- [Create an Install Command from a Package List](/user-guide/managing-software/tips-and-tricks/create-an-install-command-from-a-package-list/)
- [List All Packages in the ISO](/user-guide/managing-software/tips-and-tricks/list-all-packages-in-the-iso/)
- [Using DNF](/user-guide/managing-software/using-dnf/)
- [Maintaining Your System](/user-guide/maintaining-your-system/)
