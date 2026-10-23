---
layout: default
title: Getting Started with QA
nav_order: 80
parent: Developer Docs
has_toc: true
lang: en
---
# Getting Started with QA

QA keeps OpenMandriva Lx stable. The team tests the software before it ships, and you can join.

## Set up your system

QA testing means working with software no one has finished stabilizing, so back yourself up. Work on a dedicated machine or a virtual machine, or install a separate Rolling system on its own partition. Keep a stable system as a fallback for everyday work.

Make sure you have an account at [ABF](https://abf.openmandriva.org/) and [GitHub](https://github.com/OpenMandrivaAssociation).

Join the QA team on Matrix in `[code]#openmandriva-cooker:matrix.org` and on the [QA Forum](https://forum.openmandriva.org/c/en/qa). QA works in the same room as the developers, so mind your netiquette. If you can, attend the weekly Technical Committee meetings.

## Set up the testing repositories

Pre-release software arrives through the testing repositories. Packages in the main repository take precedence over anything else, and packages in unsupported or non-free repos are the maintainer's responsibility, not the OpenMandriva team's.

The package workflow is `Cooker → Rolling → Stable repo`. The maintainers build packages in Cooker first, and QA tests them before they move on. This is why QA members keep a Rolling system handy.

Enable the testing repositories with the [Software Repository Selector](../../user-guide/managing-software/software-repository-selector.en.html), or from the command line:

For the main testing repo only:

```bash
sudo dnf config-manager --enable rolling-testing-$ARCH
```

To enable every testing repo:

```bash
sudo dnf config-manager --enable rolling-testing-$ARCH rolling-testing-$ARCH-unsupported rolling-testing-$ARCH-restricted rolling-testing-$ARCH-non-free
```

Replace `$ARCH` with your architecture. To disable a repository, swap `--enable` for `--disable`.

## Test packages with Kahinah

Once your system is ready, vote on the packages. Use [Kahinah](https://kahinah.tsn.sh/) to decide which packages move to the stable repository, and log in with your GitHub account.

Browse the waiting packages in *Recent Builds*. Vote with a thumbs up or a thumbs down, and tell the team why. A package needs three *Accept* votes to move forward, unless anyone marked it *Reject*; a rejection gets discussed before the package goes any further. A package that stays stuck in Kahinah with no votes for more than seven days can advance on QA inaction.

## Test new releases

Testing new Alpha, Beta, and RC ISOs gets planned before each release. Find what to test and when in the [release QA guide](./getting-started-with-qa/release-qa-checklist.en.html).

## Triage new bugs

Once someone has [reported a bug](./how-to-report-a-bug.en.html), triage puts it in front of the right person. That process is still coming together, so check the [issue tracker](https://github.com/OpenMandrivaAssociation/distribution/issues) for where help is most needed.

{:.important}

Testing repositories hold unready software. Enable them only when you are actively testing, and disable them again when you are done.
