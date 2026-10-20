---
layout: default
title: Partitioning Schemas
nav_order: 10
parent: Partitioning
has_toc: true
lang: en
---
# Partitioning Schemas

The partitioning layout you choose determines how your disk is divided and what stays separate from the rest. Each approach carries trade-offs between simplicity, data safety, and maintenance. The three most common layouts in *Calamares* are described here, along with guidance on choosing the right one for your needs.

## One Partition for Everything

The simplest layout puts everything—kernel, system files, and your personal data—on a single root (`/`) partition. Calamares creates this automatically when you select **Erase disk and install**.

- **Installation is automatic.** Calamares sizes the partition to fill the disk, creates a swap partition if you enable it, and sets up the EFI partition if your system uses UEFI.
- **No planning required.** You do not decide how much space to reserve for what.
- **Reinstallation wipes everything.** If you need to reinstall OpenMandriva, your personal files in `/home` are gone unless you backed them up separately.
- **System updates carry a small risk.** A broken kernel or driver can affect your personal files because they live on the same partition.

This layout suits users who want a clean start, reinstall frequently, or keep their data on a separate drive or cloud storage. It is the default choice and the easiest to get right.

## A Separate /home Partition

A separate `/home` partition stores your personal files, settings, and documents apart from the system files. You keep it across operating system reinstallations.

- **Your data survives reinstallation.** When you reinstall OpenMandriva, you format only the root partition. Your `/home` partition stays intact, and your files, browser profiles, and application settings come back exactly as you left them.
- **You can encrypt `/home` independently.** If full-disk encryption feels heavy, you can leave root unencrypted and protect only `/home`.
- **You must plan the size upfront.** If you allocate too much to `/`, `/home` runs out of space; if you allocate too much to `/home`, the system partition fills up. Resizing requires a live USB and care.
- **Snapshots become more complex.** *Timeshift* and *Btrfs* snapshots operate on the root partition. Your personal data is outside that safety net unless you set up separate backups.

This layout suits users who reinstall their operating system occasionally, who want to keep personal data safe from system mistakes, or who dual boot and share a data partition between operating systems.

## Separate Partitions for System Directories

Some users create additional partitions for `/boot`, `/var`, `/tmp`, or other directories. Each partition isolates that directory's data from the root partition.

- **Isolation improves stability.** A runaway log in `/var` can fill the partition but not crash the rest of the system. A full `/tmp` from a misbehaving application does not lock up your desktop.
- **Fine-grained encryption.** You can encrypt sensitive directories (like `/var/log`) while leaving others plain.
- **Better fit on small disks.** You can put a modest root partition on a fast SSD and a large `/var` or `/home` on a slow, spacious hard drive.
- **Management overhead.** More partitions mean more things to size correctly, more mount points in `/etc/fstab`, and more complexity when moving the system to a new disk.
- **Not all directories benefit.** `/usr` and `/etc` are tightly coupled to the system and rarely need separation. Separating `/boot` is only necessary when you encrypt the root partition (see [Disk Encryption](./encryption.en.html)).

This layout suits advanced users, servers, and systems where specific directories grow large or need protection. It is overkill for a typical desktop installation.

## Comparison

| Layout | Setup difficulty | Data safety on reinstall | Ongoing maintenance | Best for |
| --- | --- | --- | --- | --- |
| Single partition | Lowest | None | None | Beginners, frequent reinstalls |
| Separate /home | Low | High | Occasional resizing | Most desktop users |
| Multiple partitions | High | Very high | Regular | Servers, advanced users |

## Calamares Partitioning Options

Calamares offers three automated choices at the partitioning screen:

- **Erase disk and install** — erases everything and lays out a standard layout (root, swap, and EFI partition if needed).
- **Format a partition and install** — formats one existing partition and installs into it.
- **Install alongside** — shrinks an existing partition and creates space for OpenMandriva.

Each automated option supports the single-partition layout by default. To create a separate `/home` partition or add custom partitions, select **Manual partitioning**. There you click each partition, choose a file system, and assign a mount point (`/`, `/home`, `/boot`, and so on). Check the **Encrypt** box on any partition you want to protect with LUKS (see [Disk Encryption](./encryption.en.html)).

## Manual Partitioning Workflow

To build the partition layout described above---a separate `/`, `/home`, and optional swap---follow these steps in the Calamares manual partitioning screen.

{: .note }

This guide applies to all versions of OpenMandriva, including Cooker and ROME.

### Select Manual Partitioning

To control your partition layout, select *Manual Partitioning*.

![Manual partitioning option](./images/linux-partitions-01.png)

Accepting the default *Erase disk* option creates only `/boot/efi` and `/` partitions. The installer no longer creates a swap partition by default, since most modern systems do not need one.

![Manual partition screen](./images/linux-partitions-02.png)

### Create the Partition Table

1. Create a partition table. For EFI or UEFI boot, use `GPT`. For legacy boot, you can use either `MBR` or `GPT`---if you are unsure, choose `GPT`.

1. If your system has multiple drives or SSDs, they must all use the same partition table type---all `GPT` or all `MBR`.

   ![Partition table creation](./images/linux-partitions-03.png)

### Add Partitions in Order

The only requirement is that `/boot/efi` comes first; the remaining partitions can be in any order.

1. Create the `/boot/efi` partition---typically 300 MB, formatted as FAT16 or FAT32 (the partitioner labels it `esp`).

1. Create the `/` (root) partition---this is where the operating system installs.

1. Create the `/home` partition---this stores your personal data separately from the system.

1. Create the swap partition---used as overflow memory.

1. Select *Create* for each partition and follow the dialog steps.

   ![Create partition dialog](./images/linux-partitions-04.png)

1. The completed layout should look like this.

   ![Completed partition layout](./images/linux-partitions-05.png)

When satisfied, select *Next* to begin installation.

![EFI partition dialog](./images/linux-partitions-06.png)

### Swap Partition Considerations

Your swap partition will probably never be used. Only a small minority of users need swap---those running very old computers with limited RAM or performing intense mathematical or scientific calculations. Most users should have at least 4 GB of RAM. If your computer is short on memory, consider upgrading it.

## Recommendations

- If this is your first Linux installation, let Calamares create a single root partition. You can reorganize later.
- If you reinstall occasionally or want to protect personal data, create a separate `/home` partition during installation. This is the most common recommendation for desktop users.
- If you run a server or need fine-grained control over disk layout, design your partition scheme in *GParted* (from the live session) before starting Calamares, then assign mount points in the manual partitioning screen.

{: .tip }

You can resize or move partitions later with GParted, but doing so on a mounted system is risky. Plan your layout before you start the installer.

## Related Topics

- [Partitioning](./index.en.html)
- [Disk Encryption](./encryption.en.html)
- [Installing OpenMandriva](../../installing-openmandriva.en.html)
