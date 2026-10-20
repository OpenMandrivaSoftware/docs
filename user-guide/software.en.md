---
layout: default
title: Managing Software
nav_order: 30
parent: User Guide
has_toc: true
lang: en
---
# Managing Software

You install and remove software with a package manager. OpenMandriva ships several of them, and you can use whichever you like. All of them reach the same repositories, so whichever you pick they all see the same list of available packages.

## Graphical Package Managers

These package managers provide graphical interfaces for searching, installing, and managing software.

- *Discover* is the default, built into KDE Plasma. It finds and removes most applications. Use it for applications, not for system updates.

- *DNFDragora* is a classic OpenMandriva GUI for finding, installing, and removing packages.

- *DnfDrake* adds system-level features Discover does not, such as system-wide upgrades and package history. It also opens the Software Repository Selector.

- *OM Updater* is a small, fast system updater that sits in your tray, notifies you of updates, and installs them when you select it. It comes with an equally small and fast OM Installer for installing packages graphically. 

The only graphical package manager installed by default is Discover, because it ships with the KDE Plasma desktop. This means by default, you must remember to run updates periodically, because currently you can't update OpenMandriva with Discover. All three of the above package managers include a tray utility to notify you of updates. 

## Command Line Package Manager

For advanced control over software installation and management, use the command-line tools. *DNF* is the fastest and most powerful way to manage software. Almost everything you can do in a GUI you can do in a terminal. See [Using DNF](./using-dnf.en.html).

## Repository Selector and Other Sources

OpenMandriva provides tools for managing different software sources.

- *Software Repository Selector* (`om-repo-picker`) picks which release, architecture, and repositories your system uses. See [Software Repository Selector](./repositories-tldr.en.html).

- *Flatpak* applications are packaged separately from the system repositories.

## What OpenMandriva Does Not Provide

OpenMandriva does not ship software from third-party sources that sit outside its repositories. You can still run some of these:

- *AppImage* files are self-contained executables that need no installation.

- Compiling software from source and installing binary packages from other sources both work, but they need care and are your responsibility.
