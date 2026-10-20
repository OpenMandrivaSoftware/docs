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

## 2. Install Multimedia Codecs

OpenMandriva includes only open-source codecs by default. To play MP3, H.264, or DVDs, enable the Restricted repository.

1. Open the *Software Repository Selector*.
2. Check the **Restricted** or **Non-Free** repository.
3. Install codecs:
```bash
sudo dnf install gstreamer1.0-plugins-ugly gstreamer1.0-libav
```

For DVD playback, also install `lib64dvdcss` from the Restricted repository.

## 3. Set Up Timeshift

*Timeshift* creates automatic system snapshots so you can roll back after a failed update or broken driver.

1. Install Timeshift:
```bash
sudo dnf install timeshift
```

2. Open Timeshift from the application menu and run the wizard.
3. Choose `rsync` mode for ext4 or XFS, or Btrfs mode if your root partition uses Btrfs.
4. Set a daily schedule and keep at least 7 days of snapshots.

## 4. Add a Printer

1. Open **System Settings → Printers**.
2. Click *Add Printer*.
3. Select your printer or enter its network address.
4. Choose the driver and apply.

For unsupported printers, check the [OpenPrinting database](https://www.openprinting.org/).

## 5. Install Additional Software

*Discover* is the default graphical package manager. Use it for everyday installs, or *DNF* for command-line control.

1. Open Discover from the application menu.
2. Search for the application you want.
3. Click *Install*.

For command-line installs:

```bash
sudo dnf install [package-name]
```

Popular choices include *LibreOffice*, *Firefox*, and *VLC*.

## 6. Import Browser Data

Bring your bookmarks, passwords, and history from your previous browser.

1. Open your web browser.
2. Go to *Settings → Import Data from Another Browser*.
3. Select the source browser and the data you want.
4. Click *Import*.

## 7. Configure Automatic Backups

Snapshots protect your system, but back up your personal files separately. *BorgBackup* deduplicates data for efficient daily backups. *Vorta* adds a graphical interface.

1. Choose a destination: an external drive, a network share, or cloud storage.
2. Install BorgBackup and Vorta:
```bash
sudo dnf install borgbackup vorta
```

3. Open Vorta and create a new backup repository.
4. Set the folders to back up and the backup schedule.

## 8. Customize the Desktop

1. Open **System Settings**.
2. Change the wallpaper under *Workspace*.
3. Adjust themes and fonts under *Appearance*.
4. Right-click the desktop to add widgets or rearrange panels.

## 9. Manage Software Repositories

Repositories control which software and updates you receive.

1. Open the Software Repository Selector.
2. Enable the repositories you need:
   - **main/release** — core packages, always enable.
   - **extra** — community packages.
   - **restricted** — patented codecs where legally allowed.
   - **non-free** — proprietary drivers and applications.
3. Refresh the cache:
```bash
sudo dnf clean all
sudo dnf repolist
```

## 10. Join the Community

Stay connected with other users and contributors.

- Visit the [forums](https://forum.openmandriva.org) for guides and troubleshooting.
- Join the Matrix chat for real-time help.
- Follow [openmandriva.org](https://openmandriva.org) for news and releases.

## Related Topics

- [Managing Software](../software.en.html)
- [Desktop Environments](../desktop.en.html)
- [Network Configuration](../network.en.html)
- [Using DNF](software/using-dnf.en.html)
- [Software Repository Selector](software/repositories-tldr.en.html)
