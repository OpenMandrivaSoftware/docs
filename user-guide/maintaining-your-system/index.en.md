---
layout: default
title: Update Your System
nav_order: 10
parent: Maintaining Your System
has_toc: true
lang: en
---

# Update Your System

*DNF* manages all system updates on OpenMandriva. Don't use *Discover* for system upgrades; use one of the methods below instead.

## Update from the Command Line

Use the command line when you need full control over the update process or when no graphical environment is available.

1. Open *Konsole* and refresh the package lists:

   ```bash
   $ sudo dnf clean all ; dnf clean all ; dnf repolist
   ```

1. Sync your system to the latest packages:

   ```bash
   $ sudo dnf distro-sync --refresh --allowerasing
   ```

## Update Using the Graphical Menu

Check for and install updates through the desktop's graphical update menu.

![The graphical update menu shows available system updates.](./images/index-01.png)

## Update Using Task Manager

Monitor and manage background update tasks through the Task Manager.

![The Task Manager window displays running update tasks.](./images/index-02.jpg)

## Update Using DnfDrake

Use *DnfDrake* for a graphical interface to *DNF*. See [DnfDrake Overview](../managing-software/dnfdrake-overview.en.html) for details.

![DnfDrake displays available updates for review.](./images/index-03.png)

## Update Using the OpenMandriva Updater

Use the *OpenMandriva Updater* for automatic background checks and desktop notifications. See [OpenMandriva Updater](../managing-software/openmandriva-updater.en.html) for details.

![The OpenMandriva Updater window shows pending updates.](./images/index-04.png)

## Related Topics

- [Maintaining Your System](../maintaining-your-system.en.html)
- [DnfDrake Overview](../managing-software/dnfdrake-overview.en.html)
- [OpenMandriva Updater](../managing-software/openmandriva-updater.en.html)
- [Switch Update Channels](./switch-update-channels.en.html)
