---
layout: default
title: Managing Software
nav_order: 30
parent: User Guide
has_toc: true
lang: en
---
# Managing Software

You install and remove software with a package manager. OpenMandriva ships several; use whichever you prefer. They all reach the same repositories, so whichever you pick sees the same list of available packages.

## Graphical Package Managers

These package managers provide graphical interfaces for searching, installing, and managing software.

- *Discover* is the default, built into KDE Plasma. Use it to find and remove applications, not for system updates.

- *DNFDragora* is a classic OpenMandriva GUI for finding, installing, and removing packages.

- *DnfDrake* adds system-level features that Discover does not, such as system-wide upgrades and package history. It also opens the Software Repository Selector. See [DNFDrake Overview](./managing-software/dnfdrake-overview.en.html).

- *OM Updater* is a small, fast system updater that sits in your tray, notifies you of updates, and installs them when you select it. It also includes a small, fast OM Installer for installing packages graphically. See [OpenMandriva Updater](./managing-software/openmandriva-updater.en.html).

Discover is the only graphical package manager installed by default, because it ships with the KDE Plasma desktop. This means you must remember to run updates periodically, because you cannot update OpenMandriva with Discover. All three of the above package managers include a tray utility to notify you of updates.

## Command-Line Package Manager

For advanced control over software installation and management, use the command-line tools. *DNF* is the fastest and most powerful way to manage software. Almost everything you can do in a GUI, you can do in a terminal. See [Using DNF](./managing-software/index.en.html).

## Repository Selector and Other Sources

OpenMandriva provides tools for managing different software sources.

- *Software Repository Selector* (`om-repo-picker`) picks which release, architecture, and repositories your system uses. See [Software Repository Selector](./managing-software/software-repository-selector.en.html).

- *Flatpak* applications are packaged separately from the system repositories.

## What OpenMandriva Does Not Provide

OpenMandriva does not ship software from sources outside its own repositories. You can still run some of these:

- *AppImage* files are self-contained executables that need no installation.

- Both compiling software from source and installing binary packages from other sources work, but they require care and are your responsibility.
