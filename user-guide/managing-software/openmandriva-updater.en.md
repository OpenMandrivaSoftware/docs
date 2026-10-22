---
layout: default
title: OpenMandriva Updater
nav_order: 50
parent: Managing Software
has_toc: true
lang: en
---

# OpenMandriva Updater

*The OpenMandriva Updater* is a lightweight system tray application that keeps your installation current. It checks for updates in the background, notifies you when new packages, or Flatpaks are available, and can install the updates. *OM Installer* is a graphical utility for searching for and installing new software. It runs even on low-memory systems.

## Updater

The updater sits in your system tray as a small icon. When updates are available, the icon changes to indicate the status:

![The tray icon shows an update is needed.](./images/openmandriva-updater-01.png)

Click the tray icon to open the updater window and review pending updates:

![The updater has a simple interface.](./images/openmandriva-updater-02.png)

The updater handles both RPM packages and Flatpaks. Snaps update automatically through the Snap subsystem.

## Installer

*OM Installer* is a graphical tool for searching for and installing RPM, Flatpak, and Snap packages. It provides an alternative to command-line package management when you need to find and install software interactively.

![Search for a package, right-click to mark packages for installation or removal, and click Install Marked to install.](./images/openmandriva-updater-03.png)

To install or remove packages,

1. Open *OM Installer* from the application menu or the updater's tray icon.
1. Search for the package you want by name or keyword.
1. Right-click a package and select *Mark for Installation* or *Mark for Removal*. Packages already installed appear in green.
1. Click *Install Marked* or *Remove Marked* to apply your selections.

Flatpak and Snap packages can be searched in separate categories by clicking the category names in the sidebar.

## Related Topics

- [Using DNF](./index.en.html)
- [OpenMandriva Welcome](../openmandriva-welcome.en.html)
- [First Ten Tasks After Installation](../first-steps.en.html)
