---
layout: default
title: OpenMandriva Lx 6.0 Errata
nav_order: 70
parent: Releases
has_toc: true
lang: en
---

# OpenMandriva Lx 6.0 Errata — Known Issues

{: .note }
> As with any release, there are still issues and bugs that may not have been resolved. This page documents those that may cause inconvenience and, where possible, details how they may be worked around.

Please read the [OpenMandriva Lx 6.0 Release Notes](./rock-6.0-release-notes.en.html) as well.

## Known Issues and Workarounds

### Steam

The game launcher *Steam* is available in the `non-free` repositories of OpenMandriva. It is known to crash on the first start, complaining about `steamwebhelper` not responding.

Since Steam is not Open Source, the code cannot be fixed. A workaround exists: kill the hung `steamwebhelper` process (reboot if you do not know how) and start Steam again.

The second and all subsequent launches work.

### NVIDIA Graphics Cards

Community members have made NVIDIA proprietary drivers available. The `nvidia` driver contains the latest production driver. You can install the driver from the OpenMandriva Welcome module.

Keep in mind that the people who make these packages available are volunteering their time and knowledge. There may be a lag between a new kernel and the relevant NVIDIA package builds.

{: .warning }
> These packages are kernel specific. At this time, they do not install if a newer kernel version is installed on the system than the kernel version this software is built for.
>
> More information is available [here](https://forum.openmandriva.org/t/about-nvidia-proprietary-driver-software/4770) and [here](https://forum.openmandriva.org/t/installing-nvidia-proprietary-drivers-in-rome/4742).

**Known issues (all NVIDIA packages):**

1. The code is closed source. Nothing wrong with the code can be fixed; NVIDIA handles that.
2. Plymouth boot splash may not work.
3. Virtual terminals may not work.
4. Kscreenlocker may not work.
5. If you use `kernel-rc-desktop`, install `nvidia-kmod-rc-desktop`. For `kernel-rc-server`, install `nvidia-kmod-rc-server`.

If you have a graphics performance issue with NVIDIA proprietary drivers, contact the [nVidia developers linux forum](https://forums.developer.nvidia.com/c/gpu-graphics/linux/148). OpenMandriva can only deal with issues related to packaging of this third-party software and whether it does or does not install.

6. Probably also related to NVIDIA graphics cards:

{: .warning }
> You may have to disconnect/unplug any secondary monitors to reach the login screen.

See also [#2072](https://github.com/sddm/sddm/issues/)

### How to Install X11 on a Plasma 6 Wayland System

For Plasma 6 users:

```bash
sudo dnf in task-plasma6-x11 --refresh
```

This gives an option to compare X11 to Wayland. Problems with Wayland in Plasma 6 are known. Use this to determine whether an issue is related to Wayland. This is essential for support requests in the OM Forum and bug reports. Also useful if Wayland does not work.

### How to Install Wayland on a Plasma 6 X11 System

For Plasma 6 users:

```bash
sudo dnf in task-plasma6-wayland --refresh
```

This gives an option to compare Wayland to X11.

### NVME SSDs

NVME SSDs are normally recognized by the OpenMandriva Live ISO. If for some reason they are not, there are workarounds under "Troubleshooting" in the ISO Grub2 Menu that may work: (PCIE ASPM=OFF) and (NVME APST=OFF). This works for most hardware. This issue is very hardware specific.

This problem is caused by buggy firmware in NVMe devices. If the device maker provides a firmware update, check if that fixes it without disabling ASPM.

ASPM (Active State Power Management) can reduce the power consumption of NVMe devices — disabling it is not recommended unless needed.

On an installed system, add the workaround to `/etc/default/grub` and run `update-grub2` to make it global. Use the one that worked on the Live ISO.

If (PCIE ASPM=OFF) worked, add:

`pcie=aspm=off`

to the lines:

`GRUB_DECLINE_LINUX_DEFAULT`

`GRUB_DECLINE_LINUX_RECOVERY`

in `/etc/default/grub` and then run:

```bash
sudo update-grub2
```

If (NVME APST=OFF) worked, add instead:

`nvme_core.default_ps_max_latency_us=0`

Ask questions about anything you do not understand on the [forum](https://forum.openmandriva.org/).

### Installing from Ventoy

**This issue should be fixed at the time of writing.**

Previous workaround if needed:

1. Copy the desired OpenMandriva `.iso` file to the Ventoy partition on the Ventoy flash drive. Boot that.
2. Open Konsole (terminal) and `cd /run/initramfs/omdv/LiveOS`
3. Type `ls` and check that `squashfs.img` is present
4. Leave Konsole open in that directory
5. Open the Calamares installer and install the new system

As long as that directory is open and `ls` shows `squashfs.img` is present, the desired OMLx system can be installed booted from the Ventoy flash drive.

If that does not work, try this:

1. Open Konsole (terminal), `cd` to `/run/initramfs/omdv/LiveOS`, then:

   ```bash
   cp squashfs.img /live
   ```

   Perform this step immediately after booting the Live ISO, or the folder `/run/initramfs/omdv/LiveOS` disappears or is not recognized. After `cp`, that folder disappears, so next:

2. ```bash
   sudo mkdir /run/initramfs/omdv/LiveOS
   ```
3. ```bash
   sudo cp /live/squashfs.img /run/initramfs/omdv/LiveOS
   ```
4. Verify:

   ```bash
   ls -la /run/initramfs/omdv/LiveOS
   ```

   ```
   total 2867796
   drwxr-xr-x 2 root root         60 Oct 19 20:30 .
   drwxr-xr-x 3 root root         60 Oct 19 20:29 ..
   -r--r-- 1 root root 2936623104 Oct 19 20:30 squashfs.img
   ```

5. Install OpenMandriva

### GEOIP

The installer's automatic GEOIP setting may not set the timezone correctly (it guesses the location based on the IP address). If the timezone is detected incorrectly, select the correct timezone manually.

### How to Configure a Printer

Turn the printer on and check if it is automatically configured. Verify that the right driver was installed. If the printer was auto-configured and the correct driver is installed, you are all set.

If it was not, turn off the printer. Open *System Settings > Hardware > Printers* or run `kcmshell6 kcm_printer_manager` from terminal (Konsole):

```bash
kcmshell6 kcm_printer_manager
```

If using Plasma 5, use `kcmshell5` instead of `kcmshell6`, and remove the printer in the UI dialog. If the correct driver was not installed by default, add a software package. Determine what software (if any) to add for the printer. In OpenMandriva, this is most likely a `task-printing` package specific to the printer brand. The packages are:

- `task-printing-canon`
- `task-printing-epson`
- `task-printing-hp`
- `task-printing-lexmark`
- `task-printing-okidata`
- `task-printing-misc`

Install the package that matches the printer brand, or the misc package if none match. For example:

```bash
sudo dnf install task-printing-okidata
```

Turn the printer on again and it should then automatically configure itself (a reboot may be needed for auto-config to work). Configure with *System Settings > Hardware > Printers* or run from terminal (Konsole):

```bash
kcmshell6 kcm_printer_manager
```

An alternative method to set up a printer in OpenMandriva is to use CUPS (https://localhost:631/ in a browser). For some hardware this may work better.

If help is needed, seek it [here](https://forum.openmandriva.org/c/en/support).

*Note:* For USB-connected printer issues, remove the `usbmuxd` and `ipp-usb` packages. Removing `ipp-usb` means the "driverless" driver is not usable.

### Discover New Software

To explore additional repositories' packages, enable them with the [Software Repository Selector](../../user-guide/managing-software/software-repository-selector.en.html) and refresh the cache. Use the `--refresh` option:

```bash
sudo dnf --refresh install [package_name]
```

Or use `dnf clean all`:

```bash
sudo dnf clean all ; sudo dnf install [package_name]
```

### Graphics Controller in VirtualBox 7.0.x

The most recent OMLx install images may need the VMSVGA controller to boot successfully in VirtualBox 7.0.x.

### Sound in VirtualBox 7.0.x

Some users report choppy or stuttering sound in the OM VirtualBox 7.0.x package. This issue seems related to the user's hardware. Developers are aware and actively looking for a solution. Remember that sound in VirtualBox is an emulation and the process is subject to periodic issues. Using VirtualBox for multimedia likely has periodic problems.

### Multiboot

In the real world, multiboot works well most of the time. When problems occur, the solution is sometimes a workaround rather than a fix. These are realities of multiboot.

OpenMandriva QA cannot test the bootloader with every file system type on every Linux distro, or even on the "Top 10" Linux distros. Whether multi-booting with Windows or other Linux distros, user reports are relied upon to know what works and what does not.

One known problem: OpenMandriva grub2 does not create boot entries for openSUSE systems that use the btrfs file system. OpenMandriva grub2 does work with openSUSE systems that use the ext4 file system.

This happens because openSUSE uses custom syntax for the btrfs patches for the openSUSE os-prober and grub2 packages, which is not compatible with OMLx code. It is not known whether OMLx bootloader works with openSUSE with other file system types such as XFS or F2FS. Switch boot-loaders in UEFI firmware settings or BIOS to the openSUSE bootloader as a workaround.

As users report multiboot issues, fixes are applied where possible. Issues that cannot be fixed are reported in Errata for OpenMandriva releases.

### Pipewire Sound Server

Some users may experience issues with the new Pipewire sound server. Switch to the older PulseAudio sound server by opening Konsole and running:

```bash
sudo dnf remove pipewire-pulse ; sudo dnf install pulseaudio-server
```

### Zypper

The `zypper-needs-restarting` package conflicts with `dnf-utils` if installed. Remove `dnf-utils` as a workaround.

### Bluetooth

For Bluetooth devices, enable the systemd bluetooth service. Open Konsole and run:

```bash
sudo systemctl enable --now bluetooth
```

### System Settings

Some modules in System Settings may not display correctly on the first launch. They display correctly at the next login.

## Related Topics

- [OpenMandriva Lx 6.0 Release Notes](./rock-6.0-release-notes.en.html)
- [OpenMandriva Lx 6.0 Changelog](./rock-6.0-changelog.en.html)
- [Getting Support on the Forum](../../user-guide/getting-help/getting-support-on-the-forum.en.html)
