---
layout: default
title: Installing and Using Virt Manager
nav_order: 10
parent: Preparing Your System
has_toc: true
lang: en
---
# Installing and Using Virt Manager

*Virt Manager* (virt-manager) is a desktop application that provides a graphical interface for managing virtual machines through *libvirt*. You can use it to create and run virtual machines for testing different operating systems, software configurations, or unstable packages---all safely isolated from your main system.

## Install Virt Manager

1. Install the `virt-manager` package along with `iptables` for network access:

   ```bash
   sudo dnf install virt-manager iptables
   ```

1. Add your user account to the `qemu` and `libvirt` groups so you can manage virtual machines without root privileges:

   ```bash
   sudo usermod -a -G qemu [your-user]
   sudo usermod -a -G libvirt [your-user]
   ```

   Replace `[your-user]` with your actual username.

Newer versions of `libvirt` rely on TPM for encryption, which OpenMandriva does not support. Until OpenMandriva patches the Virt Manager packages, you must fix the secrets encryption manually. It takes some typing, but thankfully, only a few steps: 

1. Make sure the secrets directory exists and has the right permissions: 

   ```bash
   sudo mkdir -p /var/lib/libvirt/secrets
   sudo chmod 700 /var/lib/libvirt/secrets

   ```

1. Create the key manually: 

   ```bash

    sudo sh -c 'umask 0077; dd if=/dev/urandom status=none bs=32 count=1 | \
      systemd-creds encrypt --with-key=host --name=secrets-encryption-key \
      - /var/lib/libvirt/secrets/secrets-encryption-key'
   ```

1. Patch the service yourself, so `libvirt` doesn't try using TPM again. Edit the service:  

   ```bash 
      sudo systemctl edit virt-secret-init-encryption.service
   ```

1. Add this to the service file. It's the same command you used to create the key manually: 

   ``` 
    [Service]
    ExecStart=
    ExecStart=/usr/bin/sh -c 'umask 0077 && (dd if=/dev/urandom status=none bs=32 count=1 | systemd-creds encrypt --with-key=host --name=secrets-encryption-key - /var/lib/libvirt/secrets/secrets-encryption-key)'
   ```

1. Finally, register the changes with systemd: 

   ```bash 
    sudo systemctl daemon-reload
   ```

1. Since the group changes in the previous step require a re-login, reboot your system now:

   ```bash
   sudo systemctl reboot
   ```

When you reboot, `libvirtd.service` should already be running by default. 

## Configure Storage Pools

Virt Manager stores virtual machine disk images and ISO files in *storage pools*---pre-defined directories that you register with the application. You need at least two storage pools: one for downloaded ISOs and one for virtual machine disk images.

The default storage pool points to `/var/lib/libvirt/images`, which is not a good place for personal VM data. Set up two pools in your home directory instead.

1. Launch Virt Manager. The main window shows *QEMU/KVM*. If it complains that `libvirtd` is not running, start the service:

   ```bash
   sudo systemctl enable --now libvirtd.service
   ```

2. Double-click *QEMU/KVM* to connect. The label changes to *QEMU/KVM* once connected.

3. Click the *Create a new virtual machine* button in the toolbar.

   ![The virt-manager toolbar shows the Create a virtual machine button.](./images/virt-manager-01.png)

4. Choose *Local install media* and click *Forward*.

5. Under *Choose ISO or CDROM install media*, click *Browse*.

   This opens the storage volume manager, where you create your storage pools for the first time. You only do this once; future VMs reuse the pools you create here.

   ![The storage volume manager dialog lists available directories and pools.](./images/virt-manager-02.png)

   By default, only the `var/lib/libvirt/images` directory appears. You will not use this. Instead, create two folders in your home directory:

   - One for downloaded ISOs---for example, `/home/[your-user]/Downloads/Linux`.
   - One for VM disk images---for example, `/home/[your-user]/VMs`.

6. Click the *+* button in the bottom-left corner to create a new storage pool.

7. In the dialog that appears, enter a name for your ISO pool---for example, `ISOs`. Click *Browse*, navigate to the ISO directory you created, and click *Finish*.

   ![The Create a new storage pool dialog prompts for a pool name and path.](./images/virt-manager-03.png)

8. Repeat the same process to create a second pool for your VM disk images---for example, name it `VMs` and point it to `/home/[your-user]/VMs`.

   You have now configured Virt Manager to use your chosen directories for all future virtual machines. You will not need to repeat these steps.

## Next Steps

With Virt Manager installed and configured, you are ready to create your first virtual machine. See [Creating a Cooker VM](./creating-cooker-vm.en.html) to set up a development environment for OpenMandriva's Cooker branch.

## Related Topics

- [Creating a Cooker VM](./creating-cooker-vm.en.html)
- [Preparing Your System](../preparing-your-system.en.html)
- [Using Cooker](../using-cooker.en.html)
