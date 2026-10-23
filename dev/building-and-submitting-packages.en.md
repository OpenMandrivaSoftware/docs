---
layout: default
title: Building and Submitting Packages
nav_order: 40
parent: Developer Docs
has_toc: true
lang: en
---
# Building and Submitting Packages

The build system is *ABF* (Automated Build Farm). You submit packages to ABF, and it builds them for every supported architecture. Your changes compile first in Cooker, the development branch, and are tested before moving through the release plan.

## What ABF Does

ABF runs your package through every target architecture, checks the build, and publishes the result. Submitting a package with `abf submit` creates a build job. Builds can take a while, so ABF queues jobs and runs them in order.

## The Basic Workflow

The workflow compiles your package across all target architectures and submits it to ABF for testing and review.

1. Write the spec file and package files on your machine.
2. Build locally with `abb build` to catch problems early.
3. Submit the package with `abf submit`.
4. Watch the build in the ABF project page. Fix failures, edit the spec, and submit again.

{: .note }

Build locally before submitting. It is faster to fix a local failure than a queued one, and you control your own build environment.

## Building Your Package Locally

When your spec file is ready, save it and return to your terminal. From the `~/abf/[package-name]` directory, run:

```bash
abb build
```

Several subdirectories are created:

`BUILD`: where the source is unpacked and compiled.

`RPMS`: contains the finished binary RPM.

`SRPMS`: contains the source RPM.

A log file is also produced. If the build fails, use the log to identify the problem. If a required build dependency is missing, the error message tells you which packages to install. The source code for your package is downloaded automatically.

When the build succeeds, your RPM is in the `RPMS` directory and your source RPM is in the `SRPMS` directory. Install the RPM and verify the software works.

## Submitting Your Package

Experiment locally as much as you need---there is no limit on local builds. Submitting packages to ABF requires accounts on both the [ABF system](https://abf.openmandriva.org) and [GitHub](https://github.com/OpenMandrivaAssociation).

{: .note }

You must request account verification. Due to past spam issues, the verification email never arrives. Join the `[code]#openmandriva-cooker:matrix.org` channel on Matrix and ask a team member to verify your account.

1. If your package already exists in OpenMandriva (for example, you are bumping the version), fork the repository to your GitHub account and clone your fork. If the package does not exist yet, create a new Git repository on GitHub, then clone it to your machine.

2. Make your package build locally. By the end of this step you have a local RPM you can install and the downloaded source code that you upload to ABF in a later step.

3. Register for an account on [ABF](https://abf.openmandriva.org) and have it verified by a team member in the Cooker Matrix channel.

4. Upload the source code to [File Store](https://file-store.openmandriva.org). ABF displays a hash for the uploaded file.

5. Copy the hash. In the same folder as your `.spec` file, create a file named `.abf.yml`.

6. In `.abf.yml`, add the source file name and its hash:

   ```yaml
   sources:
     [source-code-file.tar.xz]: [hash-number]
   ```

7. Commit only the `.spec` and `.abf.yml` files to the repository and push to your GitHub account.

8. Log in to [ABF](https://abf.openmandriva.org).

9. In the left-hand menu, select *Projects*, then *New Project*.

10. Under *Project Name*, type the name of your GitHub repository (lowercase, matching the software name). Set *Owner* to *Myself*.

11. Under *Github organization*, type your GitHub username.

12. Check *Project is a package*.

13. Under *Maintainer of Project*, your ABF username should already be populated.

14. Click *Save*. The project now appears in your list of projects on ABF.

15. In the project list, click *New Build*.

16. Under *Build for Platform*, select *main* under *Cooker*.

17. Under *Architecture*, select *x86_64*.

18. If your personal repository appears under *Extra Repositories*, click the red *X* to remove it.

19. *Use cached chroot* and *Use extra tests* are checked by default---leave them.

20. Click *Start Build*.

21. When the x86_64 build succeeds, start another build for the remaining architectures: *aarch64* and *znver1*.

22. If all builds succeed, send a pull request on GitHub.

23. If the build is for a new package, notify the OpenMandriva developers in the Cooker Matrix channel. A team member creates the official OpenMandriva repository.

24. Fork or clone the new OM repository, re-commit your `.spec` and `.abf.yml` files, then send another pull request.

## Using the Command Line

Prefer the command line? Submit packages with the `abf` tool instead of the web interface.

When your local build works, run:

```bash
abf submit [path-to-spec].spec
```

A submission form opens so you can add a summary and choose the target branch (usually *Cooker*). If the build succeeds on ABF, maintainers review your package.

To build only this package on ABF, run:

```bash
abb build
abf submit
abf addpkg [name] [repository]
```

You need ABF access to push the package to a repository, so start that request early.

## Building for Release

A Cooker build is not enough. Packages move through the [release plan](../community/releases/index.en.html): Cooker first, then the rolling release, then the stable release. QA verifies each package before it leaves Cooker. Do not edit the release repositories directly.

## Updating Packages to a Newer Version

1. Update the `Version:` field in the spec file, commit, and run `abb build` to check if it still builds.

2. If the build breaks---a dependency changed, a path changed, and so on---fix the spec and run `abb build` again. Repeat until the build succeeds.

3. When the new version builds, run `abf submit` and update the package as you would when submitting it for the first time.

## Installing Your Submitted Package

When your package is merged, it lands in Cooker---not in ROME or Rock right away. Because Cooker is unstable, install your package from the Cooker repository using a virtual machine or a separate partition.

{: .note }

Do *not* add Cooker repositories to your system. Doing so breaks ROME or Rock.

To upgrade an existing package:

```bash
sudo dnf upgrade --enablerepo=[repo-name] [package-name]
```

To install a new package:

```bash
sudo dnf install --enablerepo=[repo-name] [package-name]
```

For example, to install an upgraded `syncthing`:

```bash
sudo dnf upgrade --enablerepo=cooker-x86_64 syncthing
```

Or to install a new `vifm`:

```bash
sudo dnf install --enablerepo=cooker-x86_64-extra vifm
```

The [RPM packaging guide](https://rpm-packaging-guide.github.io) and the [packaging-tools repository](https://github.com/OpenMandrivaSoftware/openmandriva-packaging-tools) have more examples.

## Related Topics

- [Understanding RPM Spec Files](./understanding-rpm-spec-files.en.html)
- [Installing Packaging Tools](./preparing-your-system/packaging-tools.en.html)
- [Using Cooker](./using-cooker.en.html)
- [Maintaining Packages](./maintaining-packages.en.html)
