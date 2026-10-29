---
layout: default
title: ROME Changelog
nav_order: 50
parent: Releases
has_toc: true
lang: en
---

# ROME Changelog

## Changelog 26.09

Full announcement: [OpenMandriva ROME 26.09 Released](https://www.openmandriva.org/en/news/article/2026-10-01-openmandriva-rome-26-09/)

### KDE

- [Plasma Desktop 6.7.5](https://kde.org/announcements/plasma/6/6.7.5/)
- Frameworks 6.29.0
- [KDE Gear 26.08.1](https://kde.org/announcements/gear/26.08.1/)
- Qt 6.11.2 (and 5.15.19)

### Other Desktops

- GNOME 50.3, Xfce 4.20, LXQt 2.4.0, MATE 1.28 (with an experimental Wayland session)
- In the repositories: hyprland 0.56.2, cosmic 1.7.0, niri 26.04, sway 1.12, i3 4.25.1, labwc 0.20.2, Spectrwm (new)

### Display Subsystem

- [Mesa 26.2.3](http://www.mesa3d.org/)
- Open NVIDIA kernel module now built into the kernel; proprietary driver 610.57.04 in `non-free`

### Core

- [Kernel](https://www.kernel.org/) 7.2.7 (and 7.3.0-rc4) built with clang. GCC compiled versions also available (`kernel-desktop-gcc`)
- [LLVM/clang 23.1.2](http://llvm.org/)
- [gcc 16.2.0](https://gcc.gnu.org/)
- [glibc 2.44](http://www.gnu.org/software/libc/), with support for interchangeable `malloc` implementations
- rpm 6.1.0, with a new optional `%pgo` section in spec files
- grub2 2.16
- ROCm 10.0.0

### Applications

- Helium 0.17.2, new default browser for Plasma and LXQt (replaces ungoogled-chromium)
- Firefox 156.0, Thunderbird 155.0, LibreOffice 26.8.0.3
- Krita 6.0.4 (Qt6), GIMP 3.2.4, Inkscape 1.4.4, Blender 5.2.2, OBS 32.2.2
- WINE 11.18, Proton 11.0+20260808, DXVK 3.0.2, vkd3d 2.0
- Snap support (`sudo dnf install snapd`), alongside Flatpak and AppImage
- Local AI tools: llama-cpp, ollama, whisper-cpp, comfyui and others, on system-wide GGML 0.24.0

## Changelog 25.04

### KDE

- [Plasma Desktop 6.3.4](https://kde.org/announcements/plasma/6/6.3.4) (and 5.27.12)
- [Frameworks 6.13.0](https://kde.org/announcements/frameworks/6/6.13.0) (and 5.116)
- [KDE Applications 25.04.0](https://kde.org/announcements/gear/25.04.0) (and 23.08.5)
- [Qt 6.9.0](https://www.qt.io) (and 5.15.15)

### Display Subsystem

- [Xorg 21.1.16](https://www.x.org/)
- [Wayland 1.23.1](https://wayland.freedesktop.org/releases.html)
- [Mesa 25.0.4](http://www.mesa3d.org/)

### Core

- [Kernel](https://www.kernel.org/) 6.14.2 (and 6.15.0-rc2) built with clang. GCC compiled versions also available
- [systemd 257.5](https://www.freedesktop.org/wiki/Software/systemd/)
- [LLVM/clang 19.1.7](http://llvm.org/)
- binutils 2.44
- [gcc 14.2.1](https://gcc.gnu.org/)
- [glibc 2.41](http://www.gnu.org/software/libc/)
- Java 24

### Installer

- [Calamares 3.3.14](https://calamares.io)

### Key Applications

- LibreOffice Suite 25.2.3 with Qt 6 and Plasma 6 integration
- Falkon 25.04.0
- Chromium 135.0.7049.84 patched with Google spyware disabled and JPEG-XL support re-enabled
- Firefox 137.0.2 patched with spyware disabled
- QMPlay2 25.01.19
- Telegram Desktop 5.13.1
- Krita 5.2.9
- GIMP 3.0.2
- Digikam 8.6.0
- SMPlayer 24.5.0
- VLC 3.0.21
- VirtualBox 7.1.8
- VokoscreenNG 4.5.0
- OBS Studio 31.0.3

### Alternative Desktops

The system repositories also include GNOME 48.1, Mate 1.28, xfce 4.20.1, Cinnamon, icewm, i3, sway, hyprland, hypr, wayfire, budgie and others.

### Flatpak Support

Flatpak support included.

## Related Topics

- [ROME Release Notes](./rome-release-notes.en.html)
- [ROME Errata](./rome-errata.en.html)
- [Getting Support on the Forum](../../user-guide/getting-help/getting-support-on-the-forum.en.html)
