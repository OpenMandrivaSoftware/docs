---
layout: default
title: Installing OpenMandriva to a USB Flash Drive
nav_order: 30
parent: Installing OpenMandriva
has_toc: true
lang: en
---
# Installing OpenMandriva to a USB Flash Drive

{: .warning }
> Be careful when identifying your USB drive. Entering the wrong device path could erase your entire hard drive or SSD. Only proceed if you're confident you know which device is your target USB drive.

Install OpenMandriva directly to a USB flash drive to create a portable operating system you can boot on any compatible computer.

## Why Blanching Is Necessary

The Calamares installer identifies USB devices that contain a file system as CD-ROM drives rather than install targets. This prevents installation to most pre-formatted USB flash drives. Before installing, you must "blanch" the USB drive by erasing all content and its partition table, returning it to a completely blank state.

{: .tip }
An "erased" drive still shows partition information to the system. Only a truly blank drive—without any partition table detection—is visible to Calamares as a valid installation target.

## Identifying Your USB Drive

Begin by plugging in the USB flash drive you want to install OpenMandriva to. Identify the device path using `fdisk`:

```bash
$ sudo fdisk -l
```

The output lists all storage devices. Find your USB drive by its size and model. In the example below, a 14.44 GiB USB drive appears as `/dev/sdc`:

```
Disk /dev/sdc: 14.44 GiB, 15496445952 bytes, 30266496 sectors
Disk model: TD USB 3.0      
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 1048576 bytes
Disklabel type: gpt
Disk identifier: B4EE3058-FE04-B24F-AFBF-05E6312D0953

Device        Start      End  Sectors  Size Type
/dev/sdc1      4096   618495   614400  300M EFI System
/dev/sdc2    618496 27301662 26683167 12.7G Linux filesystem
/dev/sdc3  27301663 30266459 2964797  1.4G Linux swap
```

In this example, the USB drive is `/dev/sdc`. Replace `X` in the following command with your drive's letter.

## Blanching the USB Drive

Use the `dd` command to write zeros to the first 2048 kilobytes of the USB drive, effectively erasing all data and partition information:

```bash
$ sudo dd if=/dev/zero of=/dev/sdX bs=1k count=2048
```

For the example above where the USB is `/dev/sdc`:

```bash
$ sudo dd if=/dev/zero of=/dev/sdc bs=1k count=2048
```

Run `fdisk -l` again to verify the drive is now blank:

```
Disk /dev/sdc: 14.44 GiB, 15496445952 bytes, 30266496 sectors
Disk model: TD USB 3.0      
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 1048576 bytes
```

Notice the partition table and device partitions have been removed from the output. The drive is now ready for installation.

## Installing OpenMandriva

With the USB drive properly blanched, start the OpenMandriva installer:

1. Boot from your installation media as described in [Installing OpenMandriva](../installing-openmandriva.en.html).

1. When you reach the partitioning screen in Calamares, select **Erase disk and install OpenMandriva**. Calamares recognizes your blanched USB drive as a valid installation target.

1. Complete the installation process. The installer configures the bootloader to work correctly when booted from the USB drive.

## Verifying the Installation

After installation completes, you can test your portable OpenMandriva installation:

1. Shut down the installation computer.

1. Plug the USB drive into any compatible computer and boot from it.

1. If your computer supports Secure Boot, disable it in BIOS/UEFI settings for GRUB to load properly.

{: .note }
The installation performs best on computers with USB 3.0 ports. USB 2.0 ports work but may result in slower performance.

## Troubleshooting

### "No Installation Target Found"

If the installer doesn't recognize your USB drive as an installation target, verify:

- The drive was properly blanched (no partition table should be detected)
- The drive is large enough (minimum 8 GB recommended)
- Your installation media is set to UEFI mode if your system uses UEFI

### Boot Failures

If the installed system fails to boot on another computer:

- Ensure the target computer's BIOS/UEFI is configured for the same boot mode (UEFI or Legacy)
- Verify Secure Boot is disabled if you're using an unencrypted installation
- Try using a different USB port

## Related Topics

- [Installing OpenMandriva](../installing-openmandriva.en.html)
- [Copying OpenMandriva to a USB Stick](../copying-openmandriva-to-a-usb-stick.en.html)