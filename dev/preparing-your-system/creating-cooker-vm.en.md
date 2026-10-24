---
layout: default
title: Creating a Cooker VM
nav_order: 20
parent: Preparing Your System
has_toc: true
lang: en
---
# Creating a Cooker VM

Now that Virt Manager is installed and configured, create a virtual machine running OpenMandriva Cooker. This gives you a safe, isolated environment for building and testing packages without affecting your daily system.

If you have not yet installed Virt Manager or configured storage pools, follow [Installing and Using Virt Manager](./index.en.html) first.

## Download a Cooker ISO

Cooker snapshots are published as ISO images. Download the latest build for your architecture from the official [OpenMandriva Cooker](https://www.openmandriva.org/info-cooker/) page.

## Create the VM

1. In Virt Manager, click *Create a new virtual machine* in the toolbar.

   ![The virt-manager toolbar shows the Create a virtual machine button.](./images/cooker-vm-01.png)

1. Choose *Local install media*, then click *Forward*.

1. Click *Browse*, navigate to your ISO storage pool, select the Cooker ISO you downloaded, and click *Choose Volume*. If the ISO doesn't appear, click the *Refresh* icon. 

   ![The storage volume dialog shows the Cooker ISO selected from the ISOs pool.](./images/cooker-vm-02.png)

1. Virt Manager cannot auto-detect OpenMandriva. De-select *Automatically detect from the installation media / source*, type *Generic*, and select *Generic Linux 2024*. Click *Forward*.

1. Choose the amount of memory and CPUs to dedicate to the VM. The defaults of 4 GB and 2 CPUs are sufficient for package building. Click *Forward*.

1. Click *Select or create custom storage*, then click *Manage...*.

1. In the storage volume dialog, select your *VMs* storage pool.

1. Click the *+* button next to *Volumes* to create a new disk image.

1. Enter a name for the disk image, for example, `cooker`.

1. Choose the disk size. A minimum of 50 GB is recommended for a development environment. Click *Finish*.

   ![The disk image creation dialog asks for a name and size.](./images/cooker-vm-03.png)

1. Confirm the new disk image is selected, then click *Choose Volume*.

1. Click *Forward*.

1. Enter a name for the VM, for example, `Cooker`. **Check** *Customize configuration before install*, then click *Finish*.

   ![The virtual machine configuration screen shows the VM name and the customize option.](./images/cooker-vm-04.png)

1. In the configuration editor, locate the *Firmware* drop-down at the bottom. The default is BIOS; change it to *UEFI*, and then click *Apply*. 

   ![The VM configuration editor shows the firmware selection drop-down, set to UEFI.](./images/cooker-vm-05.png)

1. Click *Begin Installation*. The VM boots from the Cooker ISO. Proceed with the [installation](../../getting-started/installing-openmandriva.en.html) as you would for any OpenMandriva release.

After installation, double-click the VM in the Virt Manager window and click its *Play* button to launch it.

## Share Files with the VM

You can use *virtiofs* to share a directory between your host system and the Cooker VM. Files you place in the shared directory on your host appear inside the VM, and vice versa. This is useful for moving package sources, build artifacts, or configuration files without manual copying.

Before you begin, shut down the VM if it is running.

1. On your host system, create the shared directory inside `~/VMs`:

   ```bash
   mkdir -p ~/VMs/vmshare
   ```

1. In Virt Manager, open the VM's details window. Click *Show virtual machine details* (or right-click the VM and choose *Open*).

1. Enable *shared memory* in the VM's processor settings. Click the *Processor* entry in the hardware list and check *All CPUs are hot-pluggable*, then check *Enable shared memory*.

1. Click *Add Hardware*, then select *Filesystem* from the device list.

1. Configure the filesystem device:

   - Set the **source** to the absolute path of `~/VMs/vmshare`, for example, `/home/[your-user]/VMs/vmshare`.
   - Set the **tag** (name) to `hostshare`.

   The driver defaults to *virtiofs* when you select Filesystem, which is the correct choice.

1. Click *Finish*.

1. Click *Apply* to save the configuration.

1. Start the VM and log in.

1. Create a mount point and mount the shared directory:

   ```bash
   sudo mkdir -p /mnt/hostshare
   sudo mount -t virtiofs hostshare /mnt/hostshare
   ```

1. To mount the share automatically on every boot, add this line to the VM's `/etc/fstab`:

    ```
    hostshare  /mnt/hostshare  virtiofs  defaults  0  0
    ```

Files you place in `~/VMs/vmshare` on your host now appear in `/mnt/hostshare` inside the VM. When you build RPMs on your host system, you can copy them here to test installing them in the VM. If you decide to build RPMs in the VM, you can also share then with the host system this way. 

## Related Topics

- [Installing and Using Virt Manager](./index.en.html)
- [Preparing Your System](../preparing-your-system.en.html)
- [Using Cooker](../using-cooker.en.html)
- [Installing OpenMandriva](../../getting-started/installing-openmandriva.en.html)
