---
layout: default
title: Software Repository Selector
nav_order: 20
parent: Managing Software
has_toc: true
lang: en
---
# Software Repository Selector

The Software Repository Selector (*om-repo-picker*) configures OpenMandriva to use specific releases, architectures, and repositories. Open it from the application menu (search for *OpenMandriva Repo Selector*) or from the OM Welcome panel. Changing repositories usually switches between releases.

## The Four Media Sources

The Software Repository Selector manages four types of repositories that OpenMandriva uses. Each type serves a different purpose:

- **Main** contains core packages maintained by the OpenMandriva Lx team. This includes everything in the install images plus other commonly used applications. *main/release* should always be enabled. Leave *main/testing* disabled unless you need bleeding-edge packages.

- **Extra** contains community-maintained packages. The core team does not maintain these, so some work well and some do not. You can use whatever works for your needs.

- **Restricted** contains libraries that OpenMandriva cannot install by default for legal reasons such as patents. Availability varies by country. If these packages are prohibited in your region, leave them disabled.

- **Non-Free** contains applications and drivers that do not meet the definition of Free Software. OpenMandriva cannot fix problems caused by these packages, because no source code is available.

You can also enable third-party repositories that OpenMandriva does not host.

## Refreshing Repository Data

After changing repositories, save your changes. Then refresh your local repository cache by running:

```bash
dnf clean all
dnf repolist
```

You see your refreshed repository list and confirm the repositories you enabled.

## Related Topics

- [Managing Software](../software.en.html)
- [Using DNF](./using-dnf.en.html)