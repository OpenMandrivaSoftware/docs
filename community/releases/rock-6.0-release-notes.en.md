---
layout: default
title: OpenMandriva Lx 6.0 Release Notes
nav_order: 60
parent: Releases
has_toc: true
lang: en
---

# OpenMandriva Lx 6.0 Release Notes

The OpenMandriva teams announce the availability of **OpenMandriva Lx 6.0 Rock** edition. *(Codename: Vanadium)*

## Available Media

This release is available as a live media USB flash drive (memory stick), downloadable in ISO format. These are available on the [downloads](https://www.openmandriva.org/release-picking) page. USB flash drive installation is usually noticeably fast. Speed depends on many factors. Live media means you can run OpenMandriva Lx straight from a memory stick and try it before installing. You can also install the system to hard disk either from the running live image or from the boot manager.

**Available ISO files:**

- *x86_64 KDE Plasma desktop* — full featured (includes the most common used functionalities, multimedia and office software).
- *znver1 KDE Plasma desktop* — for AMD CPUs newer than 2017 (Ryzen, ThreadRipper, EPYC). This version outperforms the generic (x86_64) one by taking advantage of new features in those processors. Install znver1 only on the listed processors; do not install on any other hardware.

## System Requirements

OpenMandriva 6.0 requires at least 2048 MB of memory and at least 10 GB of hard drive space (see the errata for known issues with partitioning). 20 GB recommended for a Plasma desktop full installation.

**Graphics Hardware:** The KDE Plasma Desktop requires a 3D graphics card that supports OpenGL 2.0 or above. AMD, Intel, Adreno or VC4 graphics chips are recommended.

## Internet Connection

Calamares Installer checks if an Internet connection is available, but OpenMandriva 6.0 installs fine even without. Install as you normally do and proceed to use your new system. Updating requires being temporarily connected to the internet, or downloading the packages elsewhere and transferring them to the installed system. You can also use the system and not update for as long as you see fit.

## Virtual Machines

At this time, the only virtualization software that OpenMandriva 6.0 ISOs are tested on is qemu and VirtualBox. The same hardware requirements apply when running in virtual machines. For VirtualBox, use at least 2048 MB of memory or OpenMandriva 6.0 fails to boot. Install to a fresh virtual machine in VirtualBox, as installing to an existing one may occasionally fail.

The most recent install images may need the VMSVGA graphics controller set to display correctly and properly boot in VirtualBox.

## Calamares Installer

Calamares is an installer framework. By design it is very customizable to satisfy a wide variety of needs and use cases. It aims to be easy, usable, beautiful, pragmatic, inclusive and distribution-agnostic. Calamares includes an advanced partitioning feature, with support for both manual and automated partitioning operations. It is the first installer with an automated "Replace Partition" option, which makes it easy to reuse a partition over and over for distribution testing. Many Linux distros use Calamares installer and each has its own implementation and standards. You may notice some small differences but this is not a bug.

## Partitioning

At this time, partitioning LVM and Raid setups with Calamares installer is not supported.

The following applies to all partitioning of all installations on hardware: If you have a UEFI/EFI computer and your BIOS offers a choice when you boot installation media, for example:

`USB some Flash Drive`

`UEFI USB some Flash Drive`

You must choose the UEFI option and boot that. Some computers with more spartan FIRMWARE or BIOS may offer only the one option and almost always it is the correct one. If on a notebook you do not see the above choice, no worries. If you enable multiple storage drives, you must use the same partition table type for all of them. They must all be GPT or all MBR for everything to work properly. On UEFI computers in multi-boot situations with multiple storage drives, if you already have an existing `/boot/efi` partition, use it. The partitioner does not create another `/boot/efi` with proper flags and installation results in error with no bootloader installed. Do not format; set the mount point to `/boot/efi` and select the `boot` flag. You can have many different boot loaders for different operating systems in the same `/boot/efi` partition. Switching boot loaders is done in FIRMWARE or BIOS settings.

## File System Type

In the Calamares installer for OpenMandriva 6.0, the file system list includes all file systems the operating system recognizes for a host of reasons. This does not mean you should use anything in the list for your root (`/`) partition. `ext4` is the official recommendation for root, `fat32` is the recommendation for `boot/efi`.

`btrfs`, `f2fs` and `xfs` are working in recent tests but are much less often tested. Feedback is relied upon for this. `btrfs` is not a good choice for multi-boot scenarios based on recent testing.

**Other file system types in the list are not recommended.**

No official recommendation is made at this time for storage partitions or for a separate `/home` partition. Users who use separate storage partitions or a separate `/home` partition know what they are doing. For `/home`, use `ext4` (recommended) or whatever is used for the root partition.

## Changing Partition Type

Calamares cannot convert one partition type to another and preserve partition data. Calamares does not support reading or creating ZFS due to licensing.

{: .warning }
> If you run Calamares to change an existing partition type, you must first delete the partition and recreate it as the type that you wish.

## NVME SSDs

NVME SSDs are normally recognized by the OpenMandriva 6.0 Live ISO. If for some reason they are not, there are workarounds under "Troubleshooting" in the ISO Grub2 Menu that may work: (PCIE ASPM=OFF) and (NVME APST=OFF). This works for most hardware. This issue is very hardware specific. See the errata for more information.

## Installer and EFI Support

This release of OpenMandriva 6.0 supports booting and installation with and without UEFI.

*Note that secure boot is NOT supported.*
*Note that it is NOT recommended to mix MBR and GPT partitions.*

To perform an EFI installation on an existing MBR disk, convert the disk partition table to the newer GPT partitioning scheme. Use the gdisk tool. A typical invocation uses `gdisk /dev/sda`: the existing partition table is converted in memory to the GPT scheme. Warnings are issued about potential data loss; the disk is not altered until you write the partition table by pressing `w`. Back up any important data.

There may be occasions where the conversion cannot be performed, usually due to insufficient space at the beginning or end of the disk to write the partition table. Delete or resize a partition to create the needed space; gparted is helpful in these circumstances.

Create a `/boot/efi` partition to contain the boot equipment. Create it while running the Calamares installer. When the installer reaches the partitioning stage, remove the `/` (root) partition and create a small (300 MB) fat32 partition at the start of the drive. Name the partition `/boot/efi` and set the `boot` flag. If diskspace is critical, use a smaller partition, but set it as fat32 in Calamares or the installation fails. If you fail to observe these steps, the boot loader installation fails. Partition the disk in the normal way afterward.

Share experiences on the forums so this aspect of the installation can be improved.

If you are installing beside Windows 8, 8.1, 10 or similar EFI booted OS, back up any important data as a precaution. Testing has been limited with this configuration, but successful installations have been performed with no issues. Feedback in this area is welcome.

## Booting from USB

You can boot this release from a USB storage device. To create the live/installation media:

- Use the isowriter tool available from the repos:

  `sudo dnf --refresh install om-imagewriter`

  At least 4 GB of flash drive capacity is recommended. Persistent storage is not necessary. Note that this erases everything on your USB!

{: .warning }
> **Windows users**: If you use other USB-writing tools such as [Rufus](https://rufus.ie/en), select the `dd` mode. Otherwise, the tool truncates the volume name and breaks the boot process. Balena Etcher is reported as working fine to transfer OpenMandriva ISO images to USB storage devices.

- Via `dd`:

  ```bash
  sudo dd if=[iso_name] of=[usb_drive] bs=4M conv=fdatasync status=progress
  ```

  Replace `[iso_name]` with the path to the ISO and `[usb_drive]` with the device node of the USB drive, for example `/dev/sdb`.

- SUSE Studio ImageWriter and Balena Etcher have also been tested and work to transfer ISO images to USB storage devices.

- Ventoy is not fully supported. Under some circumstances it may or may not work. Use one of the suggested methods above. See [OpenMandriva Lx 6.0 Errata](./rock-6.0-errata.en.html) for Ventoy workarounds.

## Installing from USB

After creating your USB drive, turn off the computer, plug it into the USB port, and restart.

{: .warning }
> You may have to disconnect/unplug any secondary monitors to reach the login screen.

If your computer supports starting from USB, choose the device from which to boot. Interrupt the normal startup process and access the BIOS menu by pressing the key mentioned in the message after the computer starts. Usually the correct key is `Esc`, `Del`, `F12`, `F10`, `F9`, `F8`, or similar. If uncertain, do an internet search for what your hardware requires.

When you see the menu, select the entry matching your USB drive. You see entries along the lines of:

`USB some Flash Drive`

`UEFI USB some Flash Drive`

If you have a UEFI/EFI computer, select the one mentioning "UEFI" and boot that. Otherwise, the Calamares installer presents only legacy BIOS options for installation.

## Booting from DVD

Booting from DVD is deprecated, but OpenMandriva 6.0 ISOs boot from DVD using Legacy or UEFI boot. If you encounter difficulties, [these workarounds](https://forum.openmandriva.org/t/4377) should enable you to boot from DVD. In testing, booting OpenMandriva 6.0 from DVD took 5-6 minutes. This may take longer on some hardware. Using a DVD is slower than using a USB flash drive.

## About Repositories

Use the [Software Repository Selector](../../user-guide/managing-software/software-repository-selector.en.html) (also known as *om-repo-picker*) to select additional repositories for more package availability.

{: .warning }
> **Do not mix repositories from different release versions or update channels.** For example, do not use Cooker repositories on a Rock system. If you use Rock, use Rock repositories only. This is explained in more detail in [Release Plan and Repositories](../../community/releases/index.en.html). If you mix different release/update channel repositories and break your computer, the solution is a fresh install. Do not do this again after the fresh install.

## How to Install and Remove Packages

While graphical tools (Discover, dnfdragora, etc.) are useful to find available extra software, install and remove packages from the command line:

```bash
sudo dnf --refresh install [package_name]
```

Remove a package:

```bash
sudo dnf remove [package_name]
```

Install or remove a string of packages:

```bash
sudo dnf --refresh install [package_name_1] [package_name_2] [package_name_3] [package_name_4]
```

More about package management with dnf [here](https://dnf.readthedocs.io/en/latest/command_ref.html).

## Recommended Update Procedure

The recommended, long-proven way to update is using the command line. Copy and paste this command:

```bash
sudo dnf clean all ; sudo dnf dsync --allowerasing
```

You can also upgrade your system using "System Update" in the menu panel of new installs, or in the *Application Menu > System > System Update*.

If you have a problem with the `dsync` upgrade, use this command:

```bash
sudo dnf clean all ; sudo dnf dsync --allowerasing 2>&1 | tee dsync.log.txt
```

This creates the log `dsync.log.txt` to attach to a forum post or bug report. If you use this command multiple times, the file gets overwritten each time. Rename the file each time if you need multiple transaction logs, for example `dsync1.log.txt`, `dsync2.log.txt`, and so on.

*Note:* `dsync` is an alias for `distro-sync`. Fedora users may be used to `dnf up`, but OpenMandriva is different. For Rock releases, use `dnf up` or `dnf dsync`.

## Default Sound Server Switched to Pipewire

[*Pipewire*](https://pipewire.org/) has become the default sound server in the current system release together with WirePlumber, replacing PulseAudio. However, PulseAudio is still in the repository and you can return to it at any time. Use this command:

```bash
sudo dnf rm pipewire-pulse ; sudo dnf in pulseaudio-server
```

## Clang Compiled Kernel

The standard kernel for OpenMandriva 6.0 is clang compiled. The `kernel-desktop-gcc` and `kernel-server-gcc` versions are available in the rare instance they are needed.

## Nvidia Graphics Hardware

See the [OpenMandriva Lx 6.0 Errata](./rock-6.0-errata.en.html) for NVIDIA graphics information.

## Related Topics

- [OpenMandriva Lx 6.0 Errata](./rock-6.0-errata.en.html)
- [OpenMandriva Lx 6.0 Changelog](./rock-6.0-changelog.en.html)
- [Using DNF](../../user-guide/index.en.html)
- [Getting Support on the Forum](../../user-guide/getting-help/getting-support-on-the-forum.en.html)
