---
layout: default
title: Copying OpenMandriva to a USB Stick
nav_order: 20
parent: Getting Started
has_toc: true
lang: en
---
# Copying OpenMandriva to a USB Stick

The ISO file you downloaded in the [previous step](./downloading-openmandriva.en.html) can't be copied directly to a USB stick for installation. Instead, the whole USB stick must be reserved for the contents of the ISO, so you need to copy it to the USB block by block. Make sure you have a USB stick that's 8GB or larger. 

If you're on Windows, there are programs you can do that for you. If you're already on a different Linux, you already have everything you need. 

## Making an Installation USB on Windows 

1. Download Balena Etcher from this site: <https://etcher.balena.io>. 

1. Click the Etcher executable from your browser's download notification. 

1. Etcher launches. Follow the [Etcher documentation](https://etcher-docs.balena.io/) for help with Etcher. 

## Making an Installation USB on Linux 

Since Balena Etcher is also available for Linux, you can use it on Linux to create your bootable USB. You don't, however, have to; if you don't want to install anything, you can create your bootable installer right from the CLI. 

1. Insert your USB stick, but don't mount/open it. 

1. Open a terminal and type `lsblk`. A list appears, showing you all the devices on your machine: 

   ```bash
    NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
    sda           8:0    1  58.2G  0 disk 
    ├─sda1        8:1    1  58.2G  0 part 
    └─sda2        8:2    1    32M  0 part 
    zram0       253:0    0  15.6G  0 disk [SWAP]
    zram1       253:1    0     0B  0 disk 
    zram2       253:2    0     2G  0 disk /var/tmp
    nvme0n1     259:0    0   1.9T  0 disk 
    ├─nvme0n1p1 259:1    0   300M  0 part /boot/efi
    ├─nvme0n1p2 259:2    0   1.9T  0 part /var/log
    │                                     /var/cache
    │                                     /home
    │                                     /boot
    │                                     /
    └─nvme0n1p3 259:3    0  12.7G  0 part [SWAP]
   ```

1. Find your USB drive; usually it's in the form of `sdX`, where `X` is a letter. In the case above, it's `sda`. 

1. Navigate to where you downloaded your ISO; by default this is your Downloads folder. 

1. Type the command below: 

   ```bash
    dd bs=4M if=[path to openmandriva iso file] of=/dev/[usb device] status=progress oflag=sync
   ```

   For example, if you're in your Downloads directory, the OpenMandriva ISO's file name is `OpenMandrivaLx.rolling-snapshot.20260927.4760-plasma6wayland.znver1.iso`, and your USB is identified as `sda`, you'd type this: 

   ```bash
    dd bs=4M if=OpenMandrivaLx.rolling-snapshot.20260927.4760-plasma6wayland.znver1.iso of=/dev/sda status=progress oflag=sync
   ```

   Hit Enter to execute the command. 

It takes some time, but eventually the ISO is written to your USB stick. When it's done, you're ready to install! 
