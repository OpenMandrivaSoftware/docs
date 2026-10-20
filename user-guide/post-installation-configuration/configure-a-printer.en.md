---
layout: default
title: Configure a Printer
nav_order: 30
parent: Set Your User Avatar
has_toc: true
lang: en
---

# Configure a Printer

Printers connected via USB are often auto-configured when turned on. Network printers can be auto-discovered, but you must kick off that discovery in the printer configuration tool.

## Install the Driver Package

Some printer manufacturers require an extra driver package that is not installed by default. If your printer requires one, [install](../managing-software.en.html) the matching package for your printer brand before configuring the printer:

- `task-printing-canon`---Canon
- `task-printing-epson`---Epson
- `task-printing-hp`---HP
- `task-printing-lexmark`---Lexmark
- `task-printing-okidata`---OKI
- `brlaser`---Brother
- `task-printing-misc`---Other brands

For example, to install the OKI driver:

```bash
sudo dnf install task-printing-okidata
```

## Check for Auto-Configuration

1. Turn your printer on and make sure it is connected---via USB cable or on your Wi-Fi or wired network.

1. Open *System Settings → Printers* and check whether your printer appears in the list.

1. If the printer appears and a test page prints successfully, you are ready. If not, proceed to add it manually.

## Remove an Existing Entry

If a broken or duplicate printer entry exists, remove it before adding a fresh configuration.

1. Open *System Settings → Printers*.
2. Right-click the problematic printer and select *Remove*.

## Using the Add Printer Wizard

When the printer is powered on and connected, the Add Printer wizard detects it automatically---whether via USB or the local network.

1. Open *System Settings → Printers*.
2. Click *Add...* in the group of buttons above the list.
3. If your printer appears in the list, select it.
1. If the driver is not automatically selected click *Manual Driver Search*. This brings up all the installed drivers for your manufacturer's printers. 
4. Select the driver for your printer model.
5. Click *OK* to finish.

{: .note }

If you cannot find your printer model in the drivers list, you may have to download the driver from the manufacturer's website. Make sure you download the RPM version of the driver and follow the manufacturer's instructions carefully. 

## Add a Printer Manually

If the printer does not appear in the Add Printer wizard, click *Show Manual Options* to enter the printer address manually. Choose the protocol that matches your printer.

1. Open *System Settings → Printers*.
2. Click *Add...*.
3. Click *Show Manual Options*.
4. Select a protocol from the list and enter the required fields:

   | Protocol | Address format | Fields |
   |---|---|---|
   | Manual Config | `ipp://[printer]:[port]/[queue]` | Address |
   | IPP (ipps) | `ipps://[printer]:[port]/[queue]` | Address |
   | IPP | `ipp://[printer]:[port]/[queue]` | Address |
   | IPP (https) | `https://[printer]:[port]/[queue]` | Address |
   | AppSocket/HP JetDirect | `socket://[printer]:[port]/[queue]` | Address |
   | LPD/LPR Host or Printer | `lpd://` | Address, Queue |
   | Windows Printer via SAMBA | `smb://[printer]:[port]/[queue]` | Address, User name, Password |

1. Enter the printer address in the field(s) provided.
2. Click *Continue with Address* (or *Save Printer...* for SAMBA).
3. Select the PPD file for your printer model, or choose from the list of detected drivers.
4. Click *OK* to finish.

## Verify and Test

1. Open *System Settings → Printers*.
2. Click *Print Test Page* from your printer's context menu.

If the printer still does not work, check that the printer is powered on, its network is reachable, and the correct driver is selected. For further help, visit the [OpenMandriva Forum](https://forum.openmandriva.org/c/support/17).

## Related Topics

- [Managing Software](../managing-software.en.html)
- [Post Installation Configuration](../../post-installation-configuration.en.html)
- [Set Your User Avatar](./index.en.html)
