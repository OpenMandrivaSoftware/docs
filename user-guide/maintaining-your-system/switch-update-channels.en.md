---
layout: default
title: Switch Update Channels
nav_order: 20
parent: Maintaining Your System
has_toc: true
lang: en
---

# Switch Update Channels

OpenMandriva offers two main release branches: *Rock* (stable) and *ROME* (rolling). Switch from Rock to ROME, or vice versa, by updating your repository channel and running a system upgrade.

{: .note }

ROME requires comfort with the command line and basic *DNF* commands. Read [Release Plan and Repositories](../../community/releases/index.en.html) before switching.

## Switch from Rock to ROME

Update your repository channels from the stable *Rock* branch to the rolling *ROME* branch.

1. Open *Software Repository Selector* (`om-repo-picker`) from the application menu, or open it from OM Welcome.

   ![The Software Repository Selector window opens with update channel options.](./images/switch-update-channels-01.jpg)

1. In OM Welcome, select the OpenMandriva repo-picker.

   ![OM Welcome highlights the repo-picker option for launching the selector.](./images/switch-update-channels-02.jpg)

1. Navigate to the *Update channel* section.

   ![The Update channel section displays available channel options.](./images/switch-update-channels-03.jpg)

1. Select *Rolling* from the dropdown menu, confirm with *OK*, and enter your root password when prompted.

   ![The dropdown menu presents Rock and Rolling as update channel choices.](./images/switch-update-channels-04.jpg)

   This changes your repositories from Rock to Rolling. The window may disappear briefly; wait for the process to finish.

1. Run a system upgrade to apply the changes:

   ```bash
   $ sudo dnf clean all ; dnf clean all ; dnf repolist
   $ sudo dnf --allowerasing distro-sync
   ```

## Switch from ROME to Rock

Reverting to Rock requires a fresh installation. Back up your data first, then install the latest Rock ISO.

## Related Topics

- [Maintaining Your System](../maintaining-your-system.en.html)
- [Update Your System](./index.en.html)
