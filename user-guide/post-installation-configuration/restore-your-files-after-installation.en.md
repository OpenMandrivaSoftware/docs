---
layout: default
title: Restore Your Files After Installation
nav_order: 20
parent: Post Installation Configuration
has_toc: true
lang: en
---

# Restore Your Files After Installation

You have installed OpenMandriva. Before you settle in, copy your personal files---documents, photos, browser bookmarks, and other data---from your old system into your new Linux environment. Understanding how Linux names and organizes these folders helps you place everything in the right spot.

## What the Home Directory Is

In Linux, your personal files live in a directory called the *home directory*, located at `/home/[username]/`. This is the equivalent of `C:\Users\[username]` on Windows or `/Users/[username]` on macOS. Everything inside your home directory belongs to you---you do not need administrator privileges to read, move, or delete files there.

Most applications store their settings in your home directory too, so copying your old home directory to the new one restores not just your files but your preferences as well.

## Default Directories

Linux uses a standard set of directories inside your home folder, defined by the *Freedesktop specification*. Each serves a specific purpose and uses the same name on Windows and macOS, so files copied from a backup land in a familiar location.

| Directory | Purpose | Windows | macOS |
| --- | --- | --- | --- |
| `~/Desktop` | Files you want to see on your desktop | Desktop | Desktop |
| `~/Documents` | Documents, spreadsheets, presentations | Documents | Documents |
| `~/Downloads` | Files saved from web browsers and email | Downloads | Downloads |
| `~/Music` | Audio files and music libraries | Music | Music |
| `~/Pictures` | Photos and images | Pictures | Pictures |
| `~/Videos` | Video files and recordings | Videos | Movies |
| `~/Templates` | Template files for new documents | Templates | No direct equivalent |
| `~/Public` | Files shared with other users on the same machine | Public | Public |

The `~` character is shorthand for your home directory, so `~/Documents` expands to `/home/[username]/Documents`.

## Restoring Your Files

The directories above use standard names that match Windows and macOS. You can copy files directly from a backup or old drive into the corresponding folder.

1. Connect your backup drive or old hard disk to your computer.
2. Open the *File Manager* (Dolphin on KDE Plasma).
3. Navigate to your old files. On a Windows drive, look in `Users\[username]`. On a macOS drive, look in `Users/[username]`.
4. Drag and drop files into the matching directory in your home folder. For example, copy documents from the old `Documents` folder into `~/Documents`.
5. For applications that store data in hidden folders---like browser profiles---copy the `.config` directory from your old home folder to your new one. Hidden folders begin with a dot, so enable *Show Hidden Files* in the file manager.

{: .note }

Hidden files and directories (starting with a dot) store application settings. These often matter more than visible files---copy your browser profile, IDE settings, and other dotfiles if you want your applications to look and behave the same after restoration.

## Related Topics

- [Set Your User Avatar](./index.en.html)
- [Configure a Printer](./configure-a-printer.en.html)
- [Post Installation Configuration](../post-installation-configuration.en.html)
