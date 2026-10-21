---
layout: default
title: List Recent Updates
nav_order: 30
parent: Maintaining Your System
has_toc: true
lang: en
---

# List Recent Updates

When troubleshooting a malfunctioning system, it helps to know which packages were recently installed or updated. This guide shows you how to generate a list of packages sorted by installation date.

## Generate a Complete List

Run the main command to see all installed packages sorted by date, most recent first:

```bash
rpm -qa --last
```

This outputs a list like:

```
korganizer-17.12.2-1-omv2015.0.x86_64         Thu 15 Mar 2018 05:27:48 PM CET
incidenceeditor-17.12.2-1-omv2015.0.x86_64    Thu 15 Mar 2018 05:27:48 PM CET
spectacle-17.12.2-1-omv2015.0.x86_64          Thu 15 Mar 2018 05:27:45 PM CET
```

> **Note:** The list can be very long and some rows may scroll off screen. Save the output to a text file for easier reading.
{: .note }

## Save the List to a File

To save the list to a text file in your home directory:

```bash
rpm -qa --last > rpmlast.txt
```

Use a descriptive filename---including a date---to avoid overwriting previous lists:

```bash
rpm -qa --last > rpmlast_20180315.txt
```

## Export to CSV Format

To import the list into a spreadsheet such as *LibreOffice Calc*, save as CSV:

```bash
rpm -qa --last > rpmlast_20180315.csv
```

## Filter by Date

Narrow the list by piping through `grep`. For example, to see only March updates:

```bash
rpm -qa --last | grep Mar
```

Or to see packages updated on a specific day:

```bash
rpm -qa --last | grep "Thu 15 Mar"
```

## Related Topics

- [Maintaining Your System](../maintaining-your-system.en.html)
- [Update Your System](./index.en.html)
