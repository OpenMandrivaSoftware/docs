---
layout: default
title: Partitioning
nav_order: 50
parent: Installing OpenMandriva
has_toc: true
lang: en
---
# Partitioning

Installing OpenMandriva requires you to make decisions about how to organize your disk. The choices you make here affect system performance, data safety, and how easily you recover from problems. Before you reach the partitioning screen in *Calamares*, consider three topics: dual booting with Windows, choosing a file system, and managing swap. The pages that follow cover specific partition layouts and disk encryption in detail.

## Dual Booting with Windows

{: .important }

Dedicate your drive to Linux. Share it with Windows only when you have a specific, unavoidable reason.

Most people who try to dual boot Windows and Linux run into one or more of these problems:

- **Windows overwrites the boot loader.** Updates to Windows, or a recovery routine, can erase the GRUB boot entry for Linux. You then boot straight into Windows, and fixing it requires a live USB plus the `grub-install` command.

- **Fast Startup leaves the disk half-locked.** Windows Fast Startup is a hybrid shutdown that keeps NTFS volumes mounted in a dirty state. Linux refuses to mount a dirty NTFS volume read-write, so your shared partition becomes read-only or inaccessible.

- **Partition fragmentation limits your options.** The default Windows layout is a single large C: drive. Shrinking an active system partition with *GParted* or *Disk Management* is risky and can leave your Windows installation in an unstable state.

- **Updates can break both systems.** A Windows update that touches shared boot files can prevent Linux from booting. A Linux kernel update that changes how GRUB handles the dual-boot entry can prevent Windows from booting.

If you must keep Windows, install each operating system on a separate physical drive. If you have only one drive, create the partitions you need *before* you boot the installer, using GParted from the live session. Back up both systems afterward.

Most users do better with a dedicated drive. A clean, single-boot Linux installation avoids these pitfalls entirely and gives you more flexibility in how you lay out the disk.

## Choosing a File System

Calamares formats your root partition with the file system you choose. OpenMandriva supports *ext4*, *Btrfs*, *XFS*, and *F2FS*. Each has trade-offs that matter for different workloads.

### Comparison Table

| Feature | ext4 | Btrfs | XFS | F2FS |
| --- | --- | --- | --- | --- |
| Snapshots | &mdash; | ✓ via Timeshift/Snapper | &mdash; | &mdash; |
| Transparent compression | &mdash; | ✓ | &mdash; | &mdash; |
| Data checksumming | &mdash; | ✓ | &mdash; | &mdash; |
| Can shrink after creation | ✓ | ✓ | &mdash; | &mdash; |
| Large file throughput | Good | Moderate | Excellent | Good |
| SSD wear reduction | &mdash; | &mdash; | &mdash; | ✓ |
| Maintenance complexity | Low | High | Medium | Medium |

### ext4 — The Safe Default

ext4 is the most widely used Linux file system. It is stable, well tested, and straightforward to maintain. Performance is fast and predictable on everyday workloads. You repair problems with `fsck` if they arise.

ext4 does not support snapshots or transparent compression. If you want rollback capability, pair it with *Timeshift*, which copies the filesystem tree to a backup volume you can restore from a boot-time menu.

### Btrfs — Snapshots and Recovery

Btrfs is a modern, copy-on-write file system that builds in data checksumming, transparent compression, and snapshot support.

Timeshift and *Snapper* automate snapshot creation. A snapshot captures the state of your system at a point in time. If an update breaks something, you boot into an older snapshot and your system is back to working order. Snapshots are cheap because Btrfs only stores the differences between versions.

Btrfs also detects silent data corruption through checksumming, and transparent compression can reduce disk usage on SSDs.

The trade-off is complexity. Write-heavy workloads with repeated file updates can cause fragmentation, and recovering from a corrupted subvolume or a failed balance operation can require expert intervention. If you prefer a set-it-and-forget-it approach, ext4 with Timeshift (using `rsync` mode) gives you snapshots without the file system complexity.

### XFS — Large Files and Throughput

XFS is a high-performance file system optimized for large files and parallel I/O. It delivers excellent throughput on sequential workloads, such as video editing or virtual machine disk images.

XFS cannot be shrunk after creation. You must size the partition correctly the first time, or you must back up, reformat, and restore. It does not support snapshots or data checksumming.

For general desktop use, XFS offers little advantage over ext4. Choose it when you work with large files regularly and want maximum throughput.

### F2FS — Flash Storage

F2FS is the Flash-Friendly File System, designed for solid-state drives, eMMC, and other flash-based storage. It aligns writes with the erase-block size to reduce wear on flash storage and performs well on random write workloads.

The tool chain is less mature than for ext4 or XFS. Filesystem checks and repairs are more limited. It does not support snapshots or checksumming.

If your installation targets an SSD or eMMC device, F2FS is worth considering. For NVMe drives with modern wear-leveling controllers, the difference is negligible and ext4 remains the simpler choice.

## Swap and Hibernation

Swap is disk space that Linux uses as an extension of RAM. It serves two purposes: absorbing memory overflow when RAM fills up, and storing the hibernation image when you suspend-to-disk.

### Swap Partition vs. Swap File

- **Swap partition** — a dedicated partition marked for swap. Calamares can create one automatically when you choose **Erase disk and install**. A partition works with all file systems, including F2FS.
- **Swap file** — a file inside your root partition that Linux treats as swap. More flexible because you can resize it, but Btrfs handles swap files with limitations, and Calamares cannot create encrypted swap files.

### Sizing Swap

The right size depends on whether you need hibernation. General-use swap rarely needs to exceed 8 GB. Hibernation must hold the contents of RAM, so size it to at least your RAM capacity.

| RAM | Swap for general use | Swap for hibernation |
| --- | --- | --- |
| 8 GB | 4 GB | 8&ndash;12 GB |
| 16 GB | 4 GB | 16&ndash;24 GB |
| 32 GB | 4&ndash;8 GB | 32&ndash;48 GB |
| 64 GB+ | 4&ndash;8 GB | Not recommended |

### Hibernation

To use suspend-to-disk (hibernate), you need a swap area at least as large as your RAM. A swap partition is the most reliable choice. When the system hibernates, the kernel writes a compressed image of RAM to swap, then powers off. On the next boot, GRUB reads the image and restores your session.

{: .tip }

If you do not need hibernation, a small 4&ndash;8 GB swap partition is enough for emergency memory overflow. Modern systems with plenty of RAM rarely need swap unless you hibernate.

## Planning Your Layout

With these topics in mind, decide on your partition layout. [Partitioning Schemas](./linux-partitions.en.html) walks through the common approaches and their trade-offs. [Disk Encryption](./encryption.en.html) covers full-disk encryption with Calamares.
