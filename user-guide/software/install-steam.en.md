---
layout: default
title: Install Steam
nav_order: 40
parent: Managing Software
has_toc: true
lang: en
---

# Install Steam

Steam is a popular digital distribution platform for games. OpenMandriva includes Steam in its repositories---you can install it through OM Welcome or the application menu.

## Install Through OM Welcome

1. Open *OM Welcome*.

1. Navigate to *Applications > Games*.

1. Click *Steam*.

![OM Welcome Games section](./images/install-steam-01.jpg)

![Steam in OM Welcome](./images/install-steam-02.jpg)

![Steam installation prompt](./images/install-steam-03.jpg)

## Install Through the Application Menu

1. Open the *Application Menu*.

1. Navigate to *Games > Steam*.

   ![Steam in application menu](./images/install-steam-04.jpg)

   ![Steam launch screen](./images/install-steam-05.jpg)

   ![Steam setup wizard](./images/install-steam-06.jpg)

   ![Steam installation progress](./images/install-steam-07.jpg)

   ![Steam first run](./images/install-steam-08.jpg)

   ![Steam login screen](./images/install-steam-09.jpg)

   ![Steam main interface](./images/install-steam-10.jpg)

### NVIDIA Graphics Driver

If you use an NVIDIA graphics card, install the 32-bit version of the driver so Steam can run 32-bit games:

```bash
$ sudo dnf clean all; dnf clean all; dnf repolist
$ sudo dnf install --enablerepo=rock-x86_64-non-free nvidia-32bit
```

For older NVIDIA cards, use the legacy driver instead:

```bash
$ sudo dnf install --enablerepo=rock-x86_64-non-free nvidia-legacy-32bit
```

## Related Topics

- [Managing Software](../software.en.html)
- [Using DNF](./using-dnf.en.html)
