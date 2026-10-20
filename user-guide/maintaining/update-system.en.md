---
layout: default
title: Update Your System
nav_order: 10
parent: Maintaining Your System
has_toc: true
lang: en
---

# Update Your System

OpenMandriva's package manager (*DNF*) handles all system updates. Unlike some distributions, you should **not** use *Discover* for system upgrades---use one of the methods below instead.

## Update from the Command Line

1. Open *Konsole* and refresh the package lists:

   ```bash
   $ sudo dnf clean all ; dnf clean all ; dnf repolist
   ```

1. Sync your system to the latest packages:

   ```bash
   $ sudo dnf distro-sync --refresh --allowerasing
   ```

## Update Using the Graphical Menu

Alternatively, you can update using a graphical tool:

![Update menu](./images/update-system-01.png)

## Update Using Task Manager

Or use the task manager interface:

![Task manager update](./images/update-system-02.jpg)

## Update Using DnfDrake

Or use *DnfDrake*---see [DnfDrake Overview](../software/dnfdrake.en.html) for details:

![DnfDrake update](./images/update-system-03.png)

## Related Topics

- [Maintaining Your System](./index.en.html)
- [Switch Update Channels](./update-channel.en.html)
