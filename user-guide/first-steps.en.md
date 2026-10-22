---
layout: default
title: First Ten Tasks After Installation
nav_order: 10
parent: User Guide
has_toc: true
lang: en
---
# First Ten Tasks After Installation

You have installed OpenMandriva. Before you settle in, complete these ten tasks to secure your data, install the software you need, and make the system feel like yours.

## 1. Update the System

Updates deliver security patches, bug fixes, and the latest software versions. Update first, before you install anything else.

```bash
sudo dnf dsync --refresh --allowerasing
```

Reboot when prompted, especially if the kernel was updated.

## 2. Explore OM Welcome

*OM Welcome* is the first screen you see on your desktop at each boot. It is a configuration hub---not just a greeting---that introduces you to OpenMandriva, its features, and its tools. You can disable it from starting automatically at any time.

1. Click through each screen to learn what OpenMandriva offers.
2. Use the *Configure* screen to quickly access system, hardware, software, and desktop tools.
3. Use the *Applications* screen to install commonly used software by category.
4. Use the *Repositories* screen to review and manage your software sources.

For full details, see [OpenMandriva Welcome](managing-software/openmandriva-welcome.en.html).

## 3. Manage Software Repositories

Repositories control which software and updates you receive. Set them up before installing multimedia codecs or additional software.

1. Open the *Software Repository Selector*.
2. Enable the repositories you need:
   - **main/release**---core packages, always enable.
   - **extra**---community packages.
   - **restricted**---patented codecs where legally allowed.
   - **non-free**---proprietary drivers and applications.
3. Refresh the cache:
```bash
sudo dnf clean all
sudo dnf repolist
```

## 4. Install Multimedia Codecs

OpenMandriva includes only open-source codecs by default.

1. Open the *Software Repository Selector*.
2. Check the **Restricted** repository.
3. Install codecs:
```bash
sudo dnf install gstreamer1.0-plugins-ugly gstreamer1.0-libav
```

For DVD playback, also install `lib64dvdcss` from the Restricted repository.

## 5. Set Up Timeshift

*Timeshift* creates automatic system snapshots so you can roll back after a failed update or broken driver.

1. Install Timeshift:
```bash
sudo dnf install timeshift
```

2. Open Timeshift from the application menu and run the wizard.
3. Choose `rsync` mode for ext4 or XFS, or Btrfs mode if your root partition uses Btrfs.
4. Set a daily schedule and keep at least 7 days of snapshots.

## 6. Add a Printer

1. Open **System Settings → Printers**.
2. Click *Add Printer*.
3. Select your printer or enter its network address.
4. Choose the driver and apply.

For unsupported printers, check the [OpenPrinting database](https://www.openprinting.org/).

## 7. Install Additional Software

*Discover* is the default graphical package manager. Use it for everyday installs, or *DNF* for command-line control.

1. Open Discover from the application menu.
2. Search for the application you want.
3. Click *Install*.

For command-line installs:

```bash
sudo dnf install [package-name]
```

Popular choices include *LibreOffice*, *Firefox*, and *VLC*.

## 8. Configure Automatic Backups

Snapshots protect your system, but back up your personal files separately. *BorgBackup* deduplicates data for efficient daily backups. *Vorta* adds a graphical interface.

1. Choose a destination: an external drive, a network share, or cloud storage.
2. Install BorgBackup and Vorta:
```bash
sudo dnf install borgbackup vorta
```

3. Open Vorta and create a new backup repository.
4. Set the folders to back up and the backup schedule.

## 9. Customize the Desktop

1. Open **System Settings**.
2. Change the wallpaper under *Workspace*.
3. Adjust themes and fonts under *Appearance*.
4. Right-click the desktop to add widgets or rearrange panels.

## 10. Join the Community

Stay connected with other users and contributors.

- Visit the [forums](https://forum.openmandriva.org) for guides and troubleshooting.
- Join the Matrix chat for real-time help.
- Follow [openmandriva.org](https://openmandriva.org) for news and releases.

## Related Topics

- [Managing Software](managing-software.en.html)
- [Desktop Environments](desktop-environments.en.html)
- [Network Configuration](network.en.html)
- [Using DNF](managing-software/index.en.html)
- [Software Repository Selector](managing-software/software-repository-selector.en.html)
- [OpenMandriva Welcome](managing-software/openmandriva-welcome.en.html)
