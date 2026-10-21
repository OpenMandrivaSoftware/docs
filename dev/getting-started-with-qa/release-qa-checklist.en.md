---
layout: default
title: Release QA Checklist
nav_order: 20
parent: Getting Started with QA
has_toc: true
lang: en
---

# Release QA Checklist

Before each release, QA tests Alpha, Beta, and RC ISO images to catch problems early. This checklist covers the essential areas to verify during ISO testing.

## ISO Installation

1. Boot from a USB stick created with `dd if="openmandriva iso" of="/dev/sd*" bs=4M`.
1. Verify that the graphical and text installers function as specified.
1. Confirm the installer works in different languages---no missing translations.
1. Test alternative keyboard layouts.

## General Installation Properties

1. No installation action should appear off-screen at any resolution---all *OK* and *Apply* buttons must be visible.
1. Users should be able to return to previous steps. If a step is irreversible---such as partition formatting---warn before proceeding.

## Hardware and Boot

1. The release must install on all designated hardware platforms.
1. The boot splash displays correctly---no image displacement.
1. The boot manager detects other OS installations and updates when a new kernel is installed.
1. The boot menu shows these entries:
   - OpenMandriva Linux
   - Failsafe boot (single user root terminal)
   - Rescue system

## Graphical Login and Desktop

1. The login manager displays all users (excluding system users).
1. The last logged-in user is pre-selected; on a fresh install, the first user alphabetically.
1. The keyboard cursor starts in the password field.
1. USB devices mount cleanly for ext2, ext3, ext4, FAT32, and NTFS filesystems.
1. The window manager starts without errors.
1. Visible indicators appear for plugged-in USB devices.

## Services

1. Samba, CUPS, SSH, NFS, and FTP servers start without errors.
1. The auto-update system functions when internet access is available.
1. The OpenMandriva Control Center (`om-cc`) opens and works correctly.
1. The Software Repository Selector (`om-repo-picker`) is fully operational.
1. The packaging system and repositories are operational, including auto-update.

## Core Applications

### System
- Plasma Desktop
- KDE configuration apps
- Sound server (network sound functional)
- Akonadi server
- File indexing
- Konsole

### Office
- LibreOffice
- Okular

### Internet
- Falkon
- Firefox
- Chromium
- Browser plugins
- PDF support
- Java
- KMail
- Mozilla Thunderbird
- IRC Client

### File Management
- Dolphin (network access works)
- Midnight Commander

### File Editors
- KWrite
- Kate

### Development
- KDevelop
- Eclipse

### Graphics
- Gwenview
- Krita
- DigiKam

### CLI Core Applications
- `mc`, `vim`, `ed`, `vi`, `nano`, `emacs`, `bash`, `sh`, `binutils`, `man`, `less`, `netstat`, `bind`, `dhclient`, `m4`, `bison`, `grep`, `awk`, `sed`, `make`, `autoconf`, `libtool`, `pkgconfig`, `scons`, `rpm`, `perl`, `python`

## Release Approval Criteria

1. All core applications listed above must open, process, close, and save files where appropriate---with no outstanding security issues.
1. No bugs that seriously compromise system functionality for core packages. Bugs in supplementary packages are tolerated unless they affect the running OS.
1. Installing a different kernel from the repositories must work---the boot manager updates automatically and shows the new kernel.
1. Network connectivity must work---both wired and wireless.
1. Printing must work from all applications that support it.
1. The Software Repository Selector must be fully operational.
1. The packaging system and repositories must be operational, including auto-update.
1. ISO files must be properly named and dated.

## Test Planning

The QA team produces a detailed [checklist on GitHub](https://github.com/OpenMandrivaAssociation/distribution/wiki/QA-Checklist-for-QA-and-testers) for each ISO, listing detected bugs alongside typical use cases:

1. Does the ISO burn to a USB stick?
1. Does the GRUB/boot screen appear?
1. Do GRUB/boot options work?
1. Does the ISO boot to multi-user.target?
1. Does the ISO boot to graphical.target?
1. Does autologin for the live user work?
1. Does the default desktop appear after autologin?
1. Is the desktop usable---menu, file manager, web browser?
1. Does the ISO boot in VirtualBox?
1. Does the ISO install in VirtualBox?

## Related Topics

- [Getting Started with QA](../getting-started-with-qa.en.html)
- [Bug Report Tool](./index.en.html)
- [How to Report a Bug](../report-bug.en.html)
