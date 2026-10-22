---
layout: default
title: Software Repository Selector
nav_order: 10
parent: Managing Software
has_toc: true
lang: en
---
# Software Repository Selector

Use the Software Repository Selector (*om-repo-picker*) to choose which releases, architectures, and repositories OpenMandriva uses. Open it from the application menu (search for *OpenMandriva Repo Selector*) or from the OM Welcome panel. Changing repositories usually switches between releases.

Open the selector from the Application Menu by searching for *OpenMandriva Repo Selector*:

![The Application Menu search shows Software Repository Selector in the results.](./images/software-repository-selector-01.jpg)

Or open it from the OM Welcome panel:

![The OM Welcome panel shows the option to open the repository selector.](./images/software-repository-selector-02.jpg)

## The Four Media Sources

The Software Repository Selector manages four types of repositories that OpenMandriva uses. Each type serves a different purpose:

- **Main** contains core packages maintained by the OpenMandriva Lx team. This includes everything in the install images plus other commonly used applications. Always enable *main/release*. Leave *main/testing* disabled unless you need bleeding-edge packages.

![The repository selector shows the Main repository with release and testing channels.](./images/software-repository-selector-03.jpg)

![A warning dialog appears when attempting to enable the testing repository on a stable release.](./images/software-repository-selector-04.jpg)

- **Extra** contains community-maintained packages. The core team does not maintain these, so some work well and some do not. You can use whatever works for your needs.

![The repository selector shows the Extra repository channel.](./images/software-repository-selector-05.jpg)

- **Restricted** contains libraries that OpenMandriva cannot install by default for legal reasons such as patents. Availability varies by country. If these packages are prohibited in your region, leave them disabled.

![The repository selector shows the Restricted repository channel.](./images/software-repository-selector-06.jpg)

- **Non-Free** contains applications and drivers that do not meet the definition of Free Software. OpenMandriva cannot fix problems caused by these packages, because no source code is available.

![The repository selector shows the Non-Free repository channel.](./images/software-repository-selector-07.jpg)

You can also enable third-party repositories that OpenMandriva does not host.

![The repository selector shows options for adding third-party repositories.](./images/software-repository-selector-08.jpg)

## Refreshing Repository Data

After changing repositories, save your changes.

1. Run `dnf clean all` to clear all cached package metadata.
1. Run `dnf repolist` to list your enabled repositories.

Verify that the repositories you enabled appear in the output.

## Related Topics

- [Managing Software](../managing-software.en.html)
- [Using DNF](./index.en.html)