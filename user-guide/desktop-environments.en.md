---
layout: default
title: Desktop Environments
nav_order: 40
parent: User Guide
has_toc: true
lang: en
---

# Desktop Environments

OpenMandriva includes the *KDE Plasma* desktop environment by default. You begin with a complete, working desktop ready for use, and there's no need to change it. You can customize nearly every part of this flexible, modern desktop. 

*GNOME*, *LXQt*, and other desktops are also available for a simpler or lighter experience. Changing the desktop does not change your files, your settings, or your applications. The desktop is the outer layer; the system, your files, and your software stay in place. Once you install a new desktop, switching back requires only choosing again at the login screen.

## Available Desktops

OpenMandriva provides eight desktop environments through task packages. Each task package installs a complete desktop with its core applications and dependencies. Minimal variants include the desktop without extra applications.

### COSMIC

*COSMIC* is a modern desktop environment developed by System76. It features automatic tiling, workspace management, and a clean design built for productivity. COSMIC is built from the ground up with keyboard navigation and customizability in mind.

- **task-cosmic**---the full COSMIC desktop with applications
- **task-cosmic-minimal**---COSMIC without extra applications

![The COSMIC desktop shows a modern tiling window manager with workspace management and a clean panel.](./images/desktop-environments-01.jpg)

### GNOME

GNOME is a modern desktop that prioritizes simplicity and usability. It uses GNOME Shell with an Activities overview and a single top bar, keeping the interface clean and distraction-free.

- **task-gnome**---the full GNOME desktop

![The GNOME desktop shows the GNOME Shell interface with the Activities overview and top bar.](./images/desktop-environments-02.jpg)

### KDE Plasma

KDE Plasma is the default desktop for OpenMandriva. You can customize widgets, panels, and themes, as well as tweak nearly every aspect of the interface. Plasma supports both Wayland and X11 on OpenMandriva.

- **task-plasma**---the full KDE Plasma desktop with applications
- **task-plasma-minimal**---KDE Plasma without extra applications
- **task-plasma-mobile**---KDE Plasma optimized for mobile devices
- **task-plasma-mobile-minimal**---a minimal Plasma mobile interface
- **task-plasma-x11**---KDE Plasma configured for the X11 display server

![The KDE Plasma desktop shows the default panel with widgets, the application launcher, and a clock.](./images/desktop-environments-03.jpg)

### LXDE

*LXDE* is a lightweight desktop with a traditional interface. It is fast and resource-efficient, making it ideal for older computers. LXDE uses GTK+ 2 and provides a familiar desktop metaphor.

- **task-lxde**---the full LXDE desktop

![The LXDE desktop shows a lightweight interface with a traditional panel and application menu.](./images/desktop-environments-04.jpg)

### LXQt

LXQt is a lightweight, Qt-based desktop. It is the successor to LXDE and provides a modern look with traditional desktop elements. LXQt is ideal for users who want a clean, fast desktop with minimal resource usage.

- **task-lxqt**---the full LXQt desktop

![The LXQt desktop shows a clean Qt-based interface with a configurable panel and start menu.](./images/desktop-environments-05.jpg)

### MATE

*MATE* is a traditional desktop environment forked from GNOME 2. It provides a classic desktop layout with a panel, system menu, and file manager. MATE is ideal for users who prefer a familiar, desktop-oriented workflow.

- **task-mate**---the full MATE desktop with applications
- **task-mate-minimal**---a minimal MATE desktop

![The MATE desktop shows a traditional desktop layout with a panel, system menu, and workspace switcher.](./images/desktop-environments-06.jpg)

### SonicDE

*SonicDE* is a community-driven fork of KDE Plasma 6. It focuses on preserving and improving X11 support and init-system independence. SonicDE removes Wayland components and streamlines the Plasma experience for X11-based systems.

- **task-sonicde**---the full SonicDE desktop
- **task-sonicde-minimal**---a minimal SonicDE desktop

![The SonicDE desktop shows a KDE Plasma 6-style interface with traditional panel elements.](./images/desktop-environments-07.jpg)

### Xfce

*Xfce* is a lightweight, modular desktop that emphasizes productivity and speed. It provides a clean interface with a panel, application menu, and desktop icons. Xfce is ideal for users who want a fast, stable desktop without unnecessary visual effects.

- **task-xfce**---the full Xfce desktop
- **task-xfce-minimal**---a minimal Xfce desktop
- **task-xfce-plugins**---additional Xfce panel plugins

![The Xfce desktop shows a lightweight interface with a panel, application menu, and workspace switcher.](./images/desktop-environments-08.jpg)

## Installing a Desktop

Add a new desktop without removing your current one. Use [DNF](managing-software/index.en.html) to install a task package:

```bash
$ sudo dnf install task-plasma
```

Replace `task-plasma` with the package for the desktop you want. For example, `task-gnome` for GNOME or `task-xfce` for Xfce.

## Switching Desktops

After installing a new desktop, select it at the login screen:

1. Log out of your current session.
1. At the login screen, look for a session menu or gear icon.
1. Select your preferred desktop environment from the list.
1. Log in with your password.

## Coexistence and Restrictions

You can install multiple desktops on the same system. However, *Plasma* and *SonicDE* are mutually exclusive---only one of them can be installed at a time. The other desktops can co-exist, but adding more desktops increases the number of packages on your system and the complexity of updates.

{: .tip }
Try a desktop in [live mode](../../getting-started/downloading-openmandriva.en.html) first. Boot from the USB and explore before committing, so you confirm a look you like before changing your system.

## Window Managers

For a lighter, keyboard-driven setup, install a standalone window manager instead of a full desktop environment. These use fewer resources but require more manual configuration than the task-package-based desktops above.

- [Installing i3](desktop-environments/index.en.html)---a tiling window manager for the X11 display server
- [Installing Hyprland](desktop-environments/installing-hyprland.en.html)---a dynamic tiling compositor for the Wayland display server