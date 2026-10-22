---
layout: default
title: Connect to the Internet in Recovery Mode
nav_order: 20
parent: Troubleshooting
has_toc: true
lang: en
---

# Connect to the Internet in Recovery Mode

Sometimes you must boot into console or recovery mode for routine maintenance or system repair. In these modes, Wi-Fi may not work automatically; connect using the command line.

{: .note }

Your internet must have worked before something went wrong. If networking was never configured, these commands will not help.

## Boot Into Console or Recovery Mode

At the GRUB menu, change the boot target to access a text console or recovery environment:

1. At the GRUB boot menu, press `E` to edit the boot entry.

   ![The GRUB boot menu shows the cursor on the boot entry with the E key highlighted.](./images/connect-to-the-internet-in-recovery-mode-01.jpg)

1. Find the line starting with `linux` and append `3` to boot into console mode.

   ![The boot entry editor shows the linux line with a 3 being appended.](./images/connect-to-the-internet-in-recovery-mode-02.jpg)

1. Alternatively, select *Advanced options* and then *Recovery mode*.

   ![The Advanced options menu shows Recovery mode as a selectable entry.](./images/connect-to-the-internet-in-recovery-mode-03.jpg)

## Connect via Wi-Fi

Use the `nmcli` command to manage network connections when the graphical interface is unavailable.

1. List available network devices:

   ```bash
   $ nmcli dev status
   ```

   This shows network devices such as `wifi`, `wifi-p2p`, and `ethernet`. Identify your Wi-Fi device name, for example `wlp4s0`.

1. Connect to a Wi-Fi network:

   ```bash
   $ nmcli --ask dev con wlp4s0
   ```

   Replace `wlp4s0` with your device name. The `--ask` flag prompts you for the Wi-Fi password.

1. Verify the connection:

   ```bash
   $ nmcli dev status
   ```

   The device should show as `connected`.

## Connect via Ethernet

If you use an ethernet cable, the connection usually activates automatically:

```bash
$ nmcli dev status
```

If your ethernet device, such as `elp4s0`, shows as disconnected, connect it:

```bash
$ nmcli dev con elp4s0
```

The `--ask` option is not needed for ethernet, since the system already has permission.

## Related Topics

- [Fix a Broken Bootloader](./index.en.html)
- [Maintaining Your System](../maintaining-your-system.en.html)
