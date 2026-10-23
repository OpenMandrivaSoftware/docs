---
layout: default
title: Bug Report Tool
nav_order: 10
parent: Getting Started with QA
has_toc: true
lang: en
---

# Bug Report Tool

The `om-bug-report` tool collects system information to help diagnose problems. Run it and attach the generated report file to any bug report you file.

## Open the Bug Report Tool

1. Open *OM Welcome*.

1. Navigate to *OM Features > Bug report tool*.

The tool opens a window and begins gathering information from your system.

## Information Collected

The tool collects the following data:

- Configuration files in `/etc/*`
- Kernel configuration from `/proc` entries
- GRUB configuration (the boot program)
- `lspcidrake` output (PCI device listing)
- `lsusb` output (USB device listing)
- `dmidecode` output (hardware information from BIOS)
- `systemctl --failed` output (services that failed to start)
- `journalctl -b` output (current boot log)
- `rpm -qa` output (list of installed packages)
- GCC version

After collecting the information, the tool creates a file named `omdv-bug-report` in your home directory.

> **Important:** Attach this file to any bug report you file. It speeds up diagnosis by giving developers the system details they need.
{: .important }

## Related Topics

- [Getting Started with QA](../getting-started-with-qa.en.html)
- [How to Report a Bug](../how-to-report-a-bug.en.html)
- [How to Report Bugs Effectively](./report-bugs-effectively.en.html)
