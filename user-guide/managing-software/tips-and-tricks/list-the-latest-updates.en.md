---
layout: default
title: List the Latest Updates
nav_order: 20
parent: Tips and Tricks
has_toc: true
lang: en
---

# List the Latest Updates

When updates cause problems, a list of recently installed packages helps you find the source. The `rpm` command with the `--last` flag lists packages sorted by installation date, with the most recent first.

## Generate a Date-Sorted Package List

Run this command in a terminal:

```bash
$ rpm -qa --last
```

The output appears like this:

```
korganizer-17.12.2-1-omv2015.0.x86_64         Thu 15 Mar 2018 05:27:48 PM CET
incidenceeditor-17.12.2-1-omv2015.0.x86_64    Thu 15 Mar 2018 05:27:48 PM CET
lib64vdpau-drivers-17.3.6-1-omv2015.0.x86_64  Thu 15 Mar 2018 05:27:47 PM CET
lib64korganizer_core5-17.12.2-1-omv2015.0.x86_64 Thu 15 Mar 2018 05:27:47 PM CET
spectacle-17.12.2-1-omv2015.0.x86_64          Thu 15 Mar 2018 05:27:45 PM CET
locales-en-2.27-9-omv2015.0.x86_64            Thu 15 Mar 2018 05:27:45 PM CET
kdf-17.12.2-1-omv2015.0.x86_64                Thu 15 Mar 2018 05:27:44 PM CET
task-plasma-5.10.5-4-omv2015.0.x86_64         Thu 15 Mar 2018 05:27:43 PM CET
okular-tiff-17.12.2-1-omv2015.0.x86_64        Thu 15 Mar 2018 05:27:43 PM CET
```

{: .note }
The list may be very long. To see every entry at once or to attach it to a bug report, save it to a file.

## Save the List to a Text File

Save the output to a text file in your home directory:

```bash
$ rpm -qa --last > rpmlast.txt
```

To avoid overwriting a previous file, use a date-stamped filename:

```bash
$ rpm -qa --last > rpmlast_20180315.txt
```

## Save the List as CSV

You can also save the output in CSV (Comma Separated Value) format for easy import into a spreadsheet like *LibreOffice Calc*:

```bash
$ rpm -qa --last > rpmlast_20180315.csv
```

## Filter by Date

Narrow down the list by date. To show only updates from March, filter for month abbreviations:

```bash
$ rpm -qa --last | grep Mar
```

To filter to a specific day, quote the date string to handle spaces:

```bash
$ rpm -qa --last | grep "Thu 15 Mar"
```

## Related Topics

- [Listing Installed Packages](./index.en.html)
- [Create an Install Command from a Package List](./create-an-install-command-from-a-package-list.en.html)
- [Using DNF](../index.en.html)
