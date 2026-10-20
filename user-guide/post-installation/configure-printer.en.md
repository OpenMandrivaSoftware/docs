---
layout: default
title: Configure a Printer
nav_order: 30
parent: Post Installation Configuration
has_toc: true
lang: en
---

# Configure a Printer

Printers are often auto-configured when turned on, but sometimes the correct driver is not installed or the printer does not set up automatically. This guide walks you through configuring a printer manually.

## Check for Auto-Configuration

1. Turn your printer on.

1. Check whether the printer was automatically configured and whether the correct driver was installed. If both are true, you are ready to print.

1. If the printer was not configured, turn it off before proceeding.

## Remove Existing Printer Entry

1. Open *Printer Settings*:

   ```
   kcmshell6 kcm_printer_manager
   ```

   > **Note:** On Plasma 5, use `kcmshell5` instead of `kcmshell6`.
   {: .note }

1. Remove the printer entry if one exists.

## Install the Driver Package

If the correct driver was not installed by default, install the matching package for your printer brand:

- `task-printing-canon` --- Canon
- `task-printing-epson` --- Epson
- `task-printing-hp` --- HP
- `task-printing-lexmark` --- Lexmark
- `task-printing-okidata` --- OKI
- `brlaser` --- Brother
- `task-printing-misc` --- Other brands

For example, to install the OKI driver:

```bash
$ sudo dnf install task-printing-okidata
```

## Reconfigure the Printer

1. Turn the printer back on.

1. The system should automatically configure the printer. If it does not, reboot and check again.

If the printer still does not work, seek help on the [OpenMandriva Forum](https://forum.openmandriva.org/c/support/17).

## Related Topics

- [Post Installation Configuration](./index.en.html)
- [Set Your User Avatar](./set-user-avatar.en.html)
