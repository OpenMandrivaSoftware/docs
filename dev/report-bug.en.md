---
layout: default
title: How to Report a Bug
nav_order: 70
parent: Developer Docs
has_toc: true
lang: en
---
# How to Report a Bug

A clear bug report helps developers find and fix problems fast. Follow these practices.

## Where to report bugs

Use the [Issue Tracker](https://github.com/OpenMandrivaAssociation/distribution/issues) for bugs. It is the best place, even if you also reported the bug on Matrix or the forum. A GitHub account is required.

- Click **New issue**, then **Bug report > Get started** for a common bug.
- Choose *Enhancement request*, *Package request*, or *Package update* for non-bug items.

## Good report practices

- Check if a similar issue is already reported. If it is, add a short note confirming it, like "Confirming in OM Lx 4.3 as of 11 March 2022 fully updated."
- **One bug, one report.** File a separate report for each issue, and put everything about one issue into a single report.
- Ask for help on the [forum](https://forum.openmandriva.org/), not in the issue tracker. If you agree something is a bug, report it there.
- Write in English. A clear report in non-perfect English beats a perfect report in your native language.
- Use a clear title that describes what you were doing. Always include the OpenMandriva version and flavor.

## Include useful details

- **Provide console output.** If a program fails, launch it from a terminal. Include the full output in a plain text file, not a screenshot from a phone.
  - Prefix commands with `LC_ALL=C` to force English output: `LC_ALL=C dnf install <package>`.
  - Attach logs. The system journal is the best log and is accessible with `journalctl`. Other logs live in `/var/log`, such as `dnf.log` and `Xorg.0.log`.
- Include the `omv-bug-report.log` file if you can. The [om-bug-report tool](https://github.com/OpenMandrivaSoftware/om-bug-report) gathers most of this for you.
- Try the latest updates first, so you do not spend time on a problem a recent fix already solved.

## My program does not start

1. Open a terminal in your desktop session. In KDE Plasma open Konsole; in LXQt open the LXQt Terminal.
2. Launch the program from the command line. If you do not know the command, find its binary in the package manager; for example, typing `dolphin` opens the Dolphin file manager.
3. Type the first few letters and press <kbd>Tab</kbd> to use auto-completion.
4. If the program crashes, capture the error output. Save it to a text file.

## My graphical desktop does not start

If the screen stays black, switch to a virtual terminal with <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>F2</kbd> (or <kbd>F3</kbd>–<kbd>F6</kbd>). Log in there and let developers know which graphics hardware you are using:

```bash
lspci -nnk | grep -EiA3 'vga|3d|display'
```
