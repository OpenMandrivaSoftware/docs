---
layout: default
title: Installing Hyprland
nav_order: 20
parent: Desktop Environments
has_toc: true
lang: en
---

# Installing Hyprland

*Hyprland* is a dynamic tiling Wayland compositor that combines the efficiency of tiling with modern visual effects. It supports window animations, rounded corners, custom layouts, and multi-monitor setups---all while remaining lightweight. Unlike i3, which runs on the X11 display server, Hyprland runs natively on Wayland.

{: .note }
*Main* is the only repository needed on both *Rock* 6.0 and *ROME*.

## Update Your System

Refresh repository metadata and upgrade existing packages before installing Hyprland:

```bash
$ sudo dnf clean all
$ sudo dnf distro-sync --refresh --allowerasing
```

## Install Hyprland and Supporting Tools

Install the compositor and core utilities:

```bash
$ sudo dnf install hyprland waybar wofi hyprlock hyprpolkitagent
```

| Package | Purpose |
| --- | --- |
| `hyprland` | The Wayland compositor |
| `waybar` | Highly customizable status bar |
| `wofi` | Application launcher for Wayland |
| `hyprlock` | GPU-accelerated screen locker |

{: .tip }
For screenshot and screen-recording tools: `sudo dnf install grim slurp swappy`

## Launch Hyprland

Hyprland provides a session file for display managers. Select Hyprland at the login screen:

1. Log out of your current session.
1. At the login screen, click the session menu or gear icon.
1. Select Hyprland from the list of available sessions.
1. Enter your password to log in.

{: .tip }
To start Hyprland without a display manager, switch to a virtual console (`Ctrl`+`Alt`+`F2`) and run this command:

```bash
$ Hyprland
```

## First-Time Configuration

On the first launch, Hyprland generates a default configuration at `~/.config/hypr/hyprland.conf`. By default, the `Super` key (the Windows key) serves as the modifier. Common default key bindings:

- `Super`+`Return`: opens a terminal
- `Super`+`D`: opens the wofi application launcher
- `Super`+`Q`: closes the focused window
- `Super`+`Shift`+`Q`: ends the Hyprland session

Customize any setting by editing the configuration file:

```bash
$ nano ~/.config/hypr/hyprland.conf
```

{: .tip }
The [Hyprland wiki](https://wiki.hypr.land/) has extensive documentation on configuring key bindings, animations, workspaces, and monitors.

## Related Topics

- [Desktop Environments](../desktop-environments.en.html)
- [Using DNF](../managing-software/index.en.html)
- [Software Repository Selector](../managing-software/software-repository-selector.en.html)