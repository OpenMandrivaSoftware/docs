---
layout: default
title: Fix a Broken Bootloader
nav_order: 10
parent: Troubleshooting
has_toc: true
lang: en
---

# Fix a Broken Bootloader

OpenMandriva uses GRUB2 as its bootloader. If GRUB stops working---for example, after a disk change or a failed update---repair it with a few commands.

## Regenerate the GRUB Configuration

Refresh the boot menu after a system change or failed update to detect installed operating systems:

```bash
$ sudo grub2-mkconfig -o /boot/grub2/grub.cfg
```

In most cases, the simpler command works:

```bash
$ sudo update-grub2
```

## Install GRUB to a Drive

Write the bootloader to the drive you want to boot from---typically needed when the bootloader is damaged, missing, or moved to a different drive:

```bash
$ sudo grub2-install /dev/[drive]
```

Replace `[drive]` with your drive name---for example `sda` or `nvme0n1`. List your drives to identify the correct drive name:

```bash
$ sudo fdisk -l
```

## Boot Without Your Hard Drive

If you cannot access your system, boot from an external rescue tool:

- [SystemRescue](https://www.system-rescue.org/)---a comprehensive, actively maintained toolkit with GRUB, filesystem, and partition repair utilities.
- [Boot-Repair-Disk](https://sourceforge.net/projects/boot-repair-cd/)---focuses on automated boot repair with a recommended repair option.
- [Super Grub2 Disk](https://www.supergrubdisk.org/)---detects and boots operating systems without modifying your system.

## Additional Information

The `grub2-mkconfig` and `update-grub2` commands use the `os-prober` utility to detect other operating systems. Run it independently to verify detected systems:

```bash
$ sudo os-prober
```

## Related Topics

- [Connect to the Internet in Recovery Mode](./connect-to-the-internet-in-recovery-mode.en.html)
- [Maintaining Your System](../maintaining-your-system.en.html)
