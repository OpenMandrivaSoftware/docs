---
layout: default
title: Fix a Broken Bootloader
nav_order: 10
parent: Troubleshooting
has_toc: true
lang: en
---

# Fix a Broken Bootloader

OpenMandriva uses GRUB2 as its bootloader. If GRUB stops working, for example, after a disk change or a failed update, repair it using one of the approaches below, depending on your situation.

If your bootloader is broken, you can fix it in one of four ways:

1. If you cannot boot at all, repair GRUB from a Live session using an OpenMandriva ISO.
2. If you can still access your system, regenerate the GRUB configuration manually.
3. If your bootloader is damaged, missing, or moved to another drive, install GRUB to a specific drive.
4. If you have access to another computer, use external rescue tools.

## Repair GRUB from a Live Session

{: .note }
This procedure repairs the bootloader on an installed OpenMandriva system. If your system has a different boot problem, see [Boot Without Your Hard Drive](#boot-without-your-hard-drive) below for rescue tools.

{: .tip }
This procedure is written for less technical users. After each command, press Enter to execute it.

When you cannot boot into your system, repair GRUB2 from an OpenMandriva Live ISO. The following steps mount your installed system and run repair commands inside it.

1. Boot from an OpenMandriva Live ISO.

2. Open *Konsole* and run `su -` to become root. No password is required in the Live environment.

   ![A terminal window shows the root prompt after running su - in the Live environment](./images/fix-a-broken-bootloader-01.jpg)

3. Identify your disk and root partition device name:

   ```bash
   # fdisk -l
   ```

   The disk name appears as something like `Disk /dev/sda` or, for an NVMe SSD, `Disk /dev/nvme0n1`. The root partition device name is listed under "Device" and includes a number, such as `/dev/sda1` or `/dev/nvme0n1p4`.

   ![The output of fdisk -l lists the disk name and partition device names](./images/fix-a-broken-bootloader-02.jpg)

4. Mount your root partition to `/mnt`:

   ```bash
   # mount [partition device name] /mnt
   ```

   For example,

   ```bash
   # mount /dev/sda2 /mnt
   ```

   Or, for an NVMe SSD:

   ```bash
   # mount /dev/nvme1n1p4 /mnt
   ```

   ![The mount command mounts the root partition to /mnt](./images/fix-a-broken-bootloader-03.jpg)

5. Bind-mount the system directories so they are available inside the chroot:

   ```bash
   # for i in /proc /sys /sys/firmware/efi/efivars /run /dev /dev/pts; do mount --bind $i /mnt$i; done
   ```

   ![The bind-mount command makes system directories available inside the chroot](./images/fix-a-broken-bootloader-04.jpg)

6. Enter your installed system with `chroot`:

   ```bash
   # chroot /mnt
   ```

   When the chroot succeeds, the shell prompt changes from something like `[root@omv-1602 ~]#` to `[root@omv-1602 /]#`.

   ![The chroot command changes the root to the installed system](./images/fix-a-broken-bootloader-05.jpg)

7. For UEFI boot systems, mount the EFI partition inside the chroot:

   ```bash
   # mount /boot/efi
   ```

   Skip this step for BIOS boot systems.

   ![The mount /boot/efi command mounts the EFI system partition for UEFI boot](./images/fix-a-broken-bootloader-06.jpg)

8. Update the GRUB2 menu:

   ```bash
   # update-grub2
   ```

   ![The update-grub2 command regenerates the GRUB2 configuration](./images/fix-a-broken-bootloader-07.jpg)

9. Install the GRUB2 bootloader to your drive:

   ```bash
   # grub2-install /dev/[drive]
   ```

   Replace `[drive]` with the disk you want to boot from. For example,

   ```bash
   # grub2-install /dev/sda
   ```

   Or, for an NVMe SSD:

   ```bash
   # grub2-install /dev/nvme1n1
   ```

   ![The grub2-install command writes the bootloader to the disk](./images/fix-a-broken-bootloader-08.jpg)

10. Exit the chroot:

    ```bash
    # exit
    ```

    ![The exit command returns from the chroot environment](./images/fix-a-broken-bootloader-09.jpg)

11. Unmount the partitions. Use the up-arrow key to recall the mount command from step 4, then change `mount` to `umount`:

    ```bash
    # umount -l [partition device name] /mnt
    ```

    For example,

    ```bash
    # umount -l /dev/nvme1n1p4 /mnt
    ```

    ![The umount command unmounts the previously mounted partitions](./images/fix-a-broken-bootloader-10.jpg)

12. Reboot the system.

After rebooting, your system should boot normally. If it still does not boot, try one of the rescue tools in [Boot Without Your Hard Drive](#boot-without-your-hard-drive).

## Regenerate the GRUB Configuration

When you can still access your system, refresh the boot menu after a system change or failed update to detect installed operating systems:

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

Replace `[drive]` with your drive name, for example `sda` or `nvme0n1`. List your drives to identify the correct drive name:

```bash
$ sudo fdisk -l
```

## Boot Without Your Hard Drive

If you have access to another computer from which to make another ISO, several external rescue tools are available:

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
