---
layout: default
title: Maintaining Packages
nav_order: 50
parent: Developer Docs
has_toc: true
lang: en
---
# Maintaining Packages

The `packaging-tools` suite from [OpenMandrivaSoftware/packaging-tools](https://github.com/OpenMandrivaSoftware/packaging-tools) automates package maintenance across OpenMandriva's ecosystem. Whether you are bumping versions, fixing build dependencies, or moving packages between repository trees, these scripts handle the repetitive work of updating spec files, committing changes, and triggering ABF builds.

## Main Tools

The scripts live at the top level of the `packaging-tools` repository and are available from your terminal after installation. Each operates on one or more package repositories, typically organized in [build lists](#organizing-package-sets).

### auto-update

`auto-update` checks every package in your local set for upstream version changes. It compares the `Version:` field in each spec file against upstream sources including PyPI, CPAN, GitHub, GitLab, GNOME, and SourceForge. When a newer version exists, the script applies the update, builds locally, and submits to ABF.

You need a GitHub token for full access. Set the `OAUTH_TOKEN` environment variable to a personal access token:

```bash
export OAUTH_TOKEN="your-token-here"
auto-update
```

The tool accepts these options:

- `--dry-run` — check for updates and report without applying them.
- `--downgrade` — allow updates where the upstream version is lower than the current one.

Check only specific packages:

```bash
auto-update firefox thunderbird
```

Coordinated suites like KDE, Qt, and LXQt are excluded automatically. Use `update` with the appropriate build list for those packages instead.

### update

`update` bumps a project to a specific version. It reads a build list to identify the packages in the project, then for each package: clones the repository, updates `Version:` and `Release:` in the spec file, removes obsolete sources from `.abf.yml`, downloads new sources, builds locally with `abb build`, commits, and pushes. After all packages are updated, it triggers a chain build on ABF.

```bash
update PROJECT VERSION
```

Here is how to update KDE Frameworks 6 to version 6.18:

```bash
update kf6 6.18
```

The tool accepts these options:

- `-a` / `--after` — process packages starting after the named one (useful for resuming).
- `-b` / `--beta` — apply a beta tag, for instance `-b 1` for beta1.
- `-l` / `--local` — update and build locally only; skip the ABF chain build.
- `-p` / `--prerelease` — mark the build as a prerelease.

Resume an interrupted update from a specific package:

```bash
update kf6 6.18 kwindowsystem
```

### rebuild

`rebuild` bumps the `Release:` field without changing the version. Use it when a package needs a new build because of a dependency change or compiler update, but the software version has not changed.

```bash
rebuild PROJECT [reason]
```

Use it like this:

```bash
rebuild qt6 "Rebuild for OpenSSL 3.5"
```

### local-rebuild

`local-rebuild` rebuilds packages locally and installs them with `rpm`. It skips ABF entirely, which is useful for testing changes on your machine before submitting.

```bash
local-rebuild PROJECT
```

### fix-builddeps

`fix-builddeps` scans spec files for missing `BuildRequires` declarations. When a spec uses `autoconf`, `automake`, or `make` but does not declare those dependencies, the script adds them automatically.

Scan all packages with `OAUTH_TOKEN` set:

```bash
export OAUTH_TOKEN="your-token-here"
fix-builddeps
```

You can also scan specific packages:

```bash
fix-builddeps firefox gimp krita
```

### addpkg

`addpkg` creates a new package in the OpenMandriva ecosystem. It creates a GitHub repository under the `OpenMandrivaAssociation` organization, creates an ABF project, adds the package to the Cooker and Rolling repositories, and starts an initial build.

Run it from a directory containing your `.spec` file. The available trees are `main`, `unsupported`, `restricted`, and `non-free` (default is `main`).

```bash
addpkg restricted
```

### chrepo

`chrepo` moves a package between repository trees. For instance, when a package has been tested in the `unsupported` tree and is ready for `main`, `chrepo` removes it from `unsupported` and adds it to `main`.

```bash
chrepo [-f FROM] [-t TO] PACKAGENAME
```

Move `mypackage` from `unsupported` to `main`:

```bash
chrepo -f unsupported -t main mypackage
```

### depending-packages

`depending-packages` finds every package that depends on a given package. This is essential when a shared library changes and you must identify affected packages.

```bash
depending-packages PACKAGENAME
```

The tool accepts these options:

- `-k` — exclude packages in the Qt and KDE build lists (since you update those with `update`).
- `-p` — prefix output with `openmandriva/` for use with `abf chain_build`.

Find all packages depending on `libfoo5`:

```bash
depending-packages -p libfoo5
```

## Organizing Package Sets

Build lists are plain-text files that group related packages for coordinated updates. One repository name per line, optionally prefixed with `openmandriva/`. The `update` and `rebuild` scripts read these lists to process packages in order.

Key build lists include

- `kf.buildlist` — KDE Frameworks 5
- `kf6.buildlist` — KDE Frameworks 6
- `qt.buildlist` — Qt 5
- `qt6.buildlist` — Qt 6
- `pd.buildlist` — Plasma Desktop
- `kapps.buildlist` — KDE Applications 5
- `kapps6.buildlist` — KDE Applications 6
- `lxqt.buildlist` — LXQt desktop
- `cosmic.buildlist` — COSMIC desktop
- `maui.buildlist` — Maui Project

## Specialized Tools

`check-completeness` verifies that a build list includes all upstream tarballs. Use it primarily with KDE releases to ensure no components are missing.

`texlive-sync/` contains a Python tool for automated TeX Live module packaging. It fetches the upstream TeX Live database, generates spec files, stores sources on the ABF file store, and can mass-build. The older `package-texlive-module` script in the repository root is legacy.

`mergerepos` merges two package repositories, which is occasionally needed when a preview package becomes the main package. The script is dangerous and should only be used when you understand exactly what it does.

## Best Practices

Run `auto-update --dry-run` first to review planned changes before applying updates. Never run `auto-update` on packages that belong to coordinated build lists; use `update` with the appropriate build list instead. When a shared library changes, run `depending-packages` to identify packages that may need rebuilding. Test changes with `local-rebuild` before pushing to GitHub. Run `fix-builddeps` periodically to catch missing dependencies. Check the [release plan](../community/releases/index.en.html) before migrating packages between Cooker, Rolling, and Rock branches.

## Related Topics

- [Understanding RPM Spec Files](./understanding-rpm-spec-files.en.html)
- [Building and Submitting Packages](./building-and-submitting-packages.en.html)
- [Installing Packaging Tools](./preparing-your-system/packaging-tools.en.html)
- [Repository Policies](../community/releases/repository-policies.en.html)
