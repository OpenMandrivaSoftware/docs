---
layout: default
title: Fix a Broken Bootloader
nav_order: 10
parent: Troubleshooting
has_toc: true
lang: en
---

# Fix a Broken Bootloader

OpenMandriva uses GRUB2 as its bootloader. If GRUB stops working---for example, after a disk change or a failed update---you can repair it with a few commands.

## Regenerate the GRUB Configuration

Probe your system and write a comprehensive GRUB menu:

```bash
$ sudo grub2-mkconfig -o /boot/grub2/grub.cfg
```

In most cases, the simpler command works:

```bash
$ sudo update-grub2
```

## Install GRUB to a Drive

Install the bootloader to the drive you want to boot from, replacing `[drive]` with your drive name---for example `sda` or `nvme0n1`:

```bash
$ sudo grub2-install /dev/[drive]
```

To identify your drives, list them with:

```bash
$ sudo fdisk -l
```

## Boot Without Your Hard Drive

If you cannot access your system, boot from external tools:

- [Super Grub2 Disk](https://sourceforge.net/p/supergrub2/)---try this first to boot without reinstalling.
- [Rescatux](https://sourceforge.net/p/rescatux/)---a rescue distribution.

## Additional Information

The `grub2-mkconfig` and `update-grub2` commands use the `os-prober` utility to detect other operating systems. You can run it independently:

```bash
$ sudo os-prober
```

## Related Topics

- [Connect to the Internet in Recovery Mode](./connect-to-the-internet-in-recovery-mode.en.html)
- [Maintaining Your System](../maintaining-your-system.en.html)
