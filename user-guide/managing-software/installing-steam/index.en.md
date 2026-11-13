---
layout: default
title: Installing Steam
nav_order: 60
parent: Managing Software
page_id: user-guide.managing-software.installing-steam
parent_id: user-guide.managing-software
lang: en
source_lang: en
permalink: /user-guide/managing-software/installing-steam/
redirect_from:
- /user-guide/managing-software/installing-steam.en.html
has_toc: true
---
# Installing Steam

Steam is a popular digital distribution platform for games. OpenMandriva includes Steam in its repositories---you can install it through OM Welcome or the application menu.

## Install Through OM Welcome

1. Open *OM Welcome*.

1. Navigate to *Applications > Games*.

1. Click *Steam*.

![OM Welcome Games section](../images/install-steam-01.jpg)

![Steam in OM Welcome](../images/install-steam-02.jpg)

![Steam installation prompt](../images/install-steam-03.jpg)

### NVIDIA Graphics Driver

If you use an NVIDIA graphics card, install the 32-bit version of the driver so Steam can run 32-bit games. Make sure you have enabled the *non-free* repository in the [Software Repository Selector](/user-guide/managing-software/software-repository-selector/). 

```bash
$ sudo dnf install nvidia-32bit
```

For older NVIDIA cards, use the legacy driver instead:

```bash
$ sudo dnf install nvidia-legacy-32bit
```

## Related Topics

- [Managing Software](/user-guide/managing-software/)
- [Using DNF](/user-guide/managing-software/using-dnf/)
