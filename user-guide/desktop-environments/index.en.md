---
layout: default
title: Installing i3
nav_order: 10
parent: Desktop Environments
has_toc: true
lang: en
---

# Installing i3

*i3* is a tiling window manager for the X11 display server. Instead of stacking windows on top of each other, i3 arranges them in a grid that you control with keyboard shortcuts. It uses minimal resources and starts quickly, making it ideal for older hardware and users who prefer keyboard-driven workflows.

Unlike the full desktop environments described in [Desktop Environments](../desktop-environments.en.html), i3 does not include a file manager, panel, or notification daemon. You start with a bare window manager and add only the components you need.

{: .note }
*Rock* 6.0 stores `i3-wm` in the *Extra* repository. On *ROME*, it is in *Main*.

## Enable the Extra Repository (Rock Only)

On Rock, `i3-wm` is not in the default Main repository. Run this command to enable Extra:

```bash
$ sudo dnf config-manager --enable rock-x86_64-extra rock-updates-x86_64-extra
```

znver1 users replace `x86_64` with `znver1` in the repository names.

On ROME, skip this step. `i3-wm` is available from Main.

{: .tip }
You can also manage repositories with the [Software Repository Selector](../managing-software/software-repository-selector.en.html).

## Update Your System

Refresh repository metadata and upgrade existing packages before installing i3:

```bash
$ sudo dnf clean all
$ sudo dnf distro-sync --refresh --allowerasing
```

## Install i3 and Supporting Tools

Install the window manager and essential components:

```bash
$ sudo dnf install i3-wm i3lock dmenu xterm
```

| Package | Purpose |
| --- | --- |
| `i3-wm` | The i3 tiling window manager |
| `i3lock` | Screen locker |
| `dmenu` | Application launcher used by i3's default configuration |
| `xterm` | Terminal emulator used by i3's default configuration |

{: .tip }
To add a status bar that displays system information, install `i3status`. This package is in the Extra repository, so ensure Extra is enabled as described above.

## Launch i3

i3 ships with a session file for display managers. Select i3 at the login screen:

1. Log out of your current session.
1. At the login screen, click the session menu or gear icon.
1. Select i3 from the list of available sessions.
1. Enter your password to log in.

{: .tip }
To start i3 without a display manager, create an X init file instead:

```bash
$ echo "exec i3" > ~/.xinitrc
$ startx
```

On the first launch, i3 offers to generate a default configuration at `~/.config/i3/config`. Accept the offer, then customize key bindings and appearance as needed.

{: .tip }
i3 coexists with other desktop environments. You can keep *Plasma* or *GNOME* installed and switch between them at the login screen. To remove Plasma entirely after switching to i3, run `sudo dnf remove plasma-desktop`.

## Related Topics

- [Desktop Environments](../desktop-environments.en.html)
- [Using DNF](../managing-software/index.en.html)
- [Software Repository Selector](../managing-software/software-repository-selector.en.html)