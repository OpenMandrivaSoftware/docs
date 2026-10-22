---
layout: default
title: List Recent Updates
nav_order: 30
parent: Maintaining Your System
has_toc: true
lang: en
---

# List Recent Updates

When troubleshooting a malfunctioning system, identify which packages were recently installed or updated. Generate a list of packages sorted by installation date.

## Generate a Complete List

View all installed packages sorted by date, most recent first:

```bash
rpm -qa --last
```

Here is a sample of the output:

```
korganizer-17.12.2-1-omv2015.0.x86_64         Thu 15 Mar 2018 05:27:48 PM CET
incidenceeditor-17.12.2-1-omv2015.0.x86_64    Thu 15 Mar 2018 05:27:48 PM CET
spectacle-17.12.2-1-omv2015.0.x86_64          Thu 15 Mar 2018 05:27:45 PM CET
```

{: .note }

The list can be lengthy, and some rows may scroll off screen. Save the output to a text file for easier reading.

## Save the List to a File

Save the list to a text file in your home directory:

```bash
rpm -qa --last > rpmlast.txt
```

Include a date in the filename to avoid overwriting previous lists:

```bash
rpm -qa --last > rpmlast_20180315.txt
```

## Export to CSV Format

Save the list as CSV for import into a spreadsheet such as *LibreOffice Calc*:

```bash
rpm -qa --last > rpmlast_20180315.csv
```

## Filter by Date

Narrow the list by piping through `grep`. See only March updates:

```bash
rpm -qa --last | grep Mar
```

See packages updated on a specific day:

```bash
rpm -qa --last | grep "Thu 15 Mar"
```

## Related Topics

- [Maintaining Your System](../maintaining-your-system.en.html)
- [Update Your System](./index.en.html)
