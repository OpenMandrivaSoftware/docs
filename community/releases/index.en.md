---
layout: default
title: Release Plan and Repositories
nav_order: 60
parent: Releases
has_toc: true
lang: en
---
# Release Plan and Repositories

An OpenMandriva release is a set of software packages put together to form an operating system. Each release is also called an *update channel*. There are four update channels: Cooker, ROME, Rock, and Release.

{: .warning }
Do not mix update channels on one system; doing so causes package conflicts.

## The Update Channels

The workflow runs in one direction:

```text
Cooker → ROME → Release
```

**Cooker** is the development branch where the development team builds the distribution and its packages. Cooker is always changing and can break at any time. It is not for people who do not enjoy solving complex computer problems.

**ROME** is the rolling release. It holds the newest packages that the team considers ready, so it is up to date but should still work as a daily system. ROME users should be comfortable with the command line.

**Rock** is the stable release. Rock points to the latest stable release, so Rock updates in place as OpenMandriva Lx releases new stable versions. Rock is designed for people who want a system that does not change.

**Release** is the most stable and least changing channel. Package updates here are mostly bug fixes and security patches, and each version eventually reaches end of life.

{: .important }
Rock, ROME, and Cooker are the only downloadable and installable releases. To use the Release channel, which only receives security patches and bug fixes, select it in the Software Repository Selector. When a Release reaches end of life, it receives no further updates.

Rock upgrades annually, ROME monthly, and Cooker daily.

## Repositories

A repository is a server of package files. You reach repositories with a package manager such as DNF, DNFDragora, or Discover. Each of the four update channels has its own repositories, and they are not interchangeable.

Each repository has four media sources:

| Media source | What it holds |
| --- | --- |
| `main` | Packages the OpenMandriva Lx team maintains; the bulk of what you need. Keep `main/release` enabled. |
| `extra` | Community-maintained packages. Some work well, some do not. |
| `restricted` | Libraries not enabled by default for legal reasons. |
| `non-free` | Software that does not meet the definition of Free Software. OpenMandriva cannot fix problems caused here. |

Use the [Software Repository Selector](../../user-guide/managing-software/software-repository-selector.en.html) to set which channel and media sources your system uses.
