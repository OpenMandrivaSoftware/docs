---
layout: default
title: Getting Started with QA
nav_order: 80
parent: Developer Docs
has_toc: true
lang: en
---
# Getting Started with QA

QA keeps OpenMandriva Lx stable. The team tests the software before it ships, and you can join the bug hunt!

## Set Up Your System

QA testing means working with software no one has finished stabilizing, so back yourself up. Work on a dedicated machine or a virtual machine, or install a separate Rolling system on its own partition. Keep a stable system as a fallback for everyday work.

Make sure you have an account at [ABF](https://abf.openmandriva.org/) and [GitHub](https://github.com/OpenMandrivaAssociation).

Join the QA team on Matrix in <https://matrix.to/#/%21DZknJxSFYPVwIUIcVV%3Amatrix.org?via=matrix.org> and on the [QA Forum](https://forum.openmandriva.org/c/en/qa). The QA room is active with people testing OpenMandriva.

## Set Up the Testing Repositories

Pre-release software arrives through the testing repositories. Packages in the main repository take precedence over anything else, and packages in unsupported or non-free repos are the maintainer's responsibility, not the OpenMandriva team's.

The package workflow is `Cooker → Rolling → Stable repo`. The maintainers build packages in Cooker first, and QA tests them before they move on. This is why QA members keep a Rolling system handy.

Enable the testing repositories with the [Software Repository Selector](../../user-guide/managing-software/software-repository-selector.en.html), or use the command line.

Use this command for the main testing repo only:

```bash
sudo dnf config-manager --enable rolling-testing-[Architecture]
```

Here it is on x86-64:

```bash
sudo dnf config-manager --enable rolling-testing-x86-64
```

To enable every testing repo, use this command:

```bash
sudo dnf config-manager --enable rolling-testing-[Architecture] rolling-testing-[Architecture]-unsupported rolling-testing-[Architecture]-restricted rolling-testing-[Architecture]-non-free
```

Here it is on x86-64:

```bash
sudo dnf config-manager --enable rolling-testing-x86-64 rolling-testing-x86-64-unsupported rolling-testing-x86-64-restricted rolling-testing-x86-64-non-free
```

Replace `[Architecture]` with your architecture. To disable a repository, swap `--enable` for `--disable`.

## Test Packages with Kahinah

Once your system is ready, vote on the packages. Use [Kahinah](https://kahinah.tsn.sh/) to decide which packages move to the stable repository, and log in with your GitHub account.

Browse the waiting packages in *Recent Builds*. Vote with a thumbs up or a thumbs down, and tell the team why. A package needs three *Accept* votes to move forward, unless anyone marked it *Reject*; a rejection gets discussed before the package goes any further. A package that stays stuck in Kahinah with no votes for more than seven days can advance on QA inaction.

## Test New Releases

Testing new Alpha, Beta, and RC ISOs gets planned before each release. Find what to test and when in the [release QA guide](./getting-started-with-qa/release-qa-checklist.en.html).

## Triage New Bugs

Once someone has [reported a bug](../user-guide/getting-help/how-to-report-a-bug.en.html), triage puts it in front of the right person. That process is still coming together, so check the [issue tracker](https://github.com/OpenMandrivaAssociation/distribution/issues) for where help is most needed.

{: .important }
Testing repositories by definition contain software that could have bugs. Enable them only when you are actively testing and disable them again when you are done.
