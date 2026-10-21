---
layout: default
title: DnfDrake Overview
nav_order: 30
parent: Managing Software
has_toc: true
lang: en
---

# DnfDrake Overview

*DnfDrake* is a graphical frontend for DNF that adds system-level features not available in *Discover*, including system-wide upgrades and package history. It also opens the Software Repository Selector.

## Install DnfDrake

Install DnfDrake from the Application Menu or via the command line:

```bash
$ sudo dnf install dnfdrake
```

![DnfDrake install screen](https://forum.openmandriva.org/uploads/default/optimized/2X/1/18e27d874170593396f1172330c092289db3e782_2_690x431.jpeg)

## Start DnfDrake

You can launch DnfDrake from two locations:

![DnfDrake start options](https://forum.openmandriva.org/uploads/default/optimized/2X/8/8a4d5e99378b22695d860d62ca5d2814aa0b54b9_2_690x431.jpeg)

- From the *Application Menu*.
- From *OM Control Center*.

## First Start

On first launch, package lists are loaded and cached locally. The first start takes longer than subsequent ones because it performs an initial sync.

![First start loading](https://forum.openmandriva.org/uploads/default/optimized/2X/a/a771eb3429a7bc1c8e74c8e68cf217434d8a85df_2_690x431.jpeg)

### Extra Options

Rolling and ROME users should select *Distro Update* so that the *Update SYS* button changes to *Distro Sync*---this runs the correct command for a full system upgrade. Rock users can leave the default.

![Distro sync options](https://forum.openmandriva.org/uploads/default/optimized/2X/1/1ffb7f4b9d5cb038b8591d93e0cafec81c5fc931_2_690x431.jpeg)

Toggling the other options reveals additional buttons for the current session.

### Distro Sync

The Distro Sync view handles full system upgrades.

### Configure Options

You can save a custom command for quick access---useful for commands you use frequently.

### Software Repository Selector

DnfDrake provides a shortcut to the Software Repository Selector (`om-repo-picker`). When you close it, the repository list refreshes automatically.

## Features

- **Search**---find packages by name or description.
- **Install**---install individual packages or downloaded RPM files.
- **Remove**---uninstall packages you no longer need.
- **VersionLock**---lock a package to its current version to prevent updates.
- **History**---view the DNF transaction history.
- **Command field**---run any DNF command directly.

## Related Topics

- [Using DNF](./index.en.html)
- [Software Repository Selector](./software-repository-selector.en.html)
- [Managing Software](../managing-software.en.html)
