---
layout: default
title: Fix Incorrect Time in Dual Boot
nav_order: 30
parent: Troubleshooting
has_toc: true
lang: en
---

# Fix Incorrect Time in Dual Boot

If you dual-boot OpenMandriva with Windows and the system clock shows the wrong time, the cause is almost always a mismatch in how the hardware clock (RTC) is stored. Windows stores RTC in local time, while Linux expects UTC.

## Diagnose the Problem

Check your time configuration to determine whether the hardware clock is set to local time or UTC:

```bash
$ timedatectl
```

Inspect the last line of the output:

- If `RTC in local TZ: yes`, your clock is set correctly. The problem is elsewhere.
- If `RTC in local TZ: no`, this is the most common cause. Set the clock to local time.

## Set the Clock to Local Time

Set the hardware clock to local time to match Windows:

```bash
$ sudo timedatectl set-local-rtc 1 --adjust-system-clock
```

The command prompts for your root password.

## Verify the Fix

Run `timedatectl` again to confirm the change:

```bash
$ timedatectl
```

The last line should now show `RTC in local TZ: yes`.

{: .warning }

A warning about the system being configured to read the RTC in local time is expected and appears every time you run `timedatectl`. You can safely ignore it.

## Definitions

**RTC**: Real Time Clock, also called the hardware clock or `hwclock`.

**TZ**: Time Zone.

## Related Topics

- [Connect to the Internet in Recovery Mode](./connect-to-the-internet-in-recovery-mode.en.html)
- [Maintaining Your System](../maintaining-your-system.en.html)
