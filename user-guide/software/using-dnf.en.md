---
layout: default
title: Using DNF
nav_order: 10
parent: Managing Software
has_toc: true
lang: en
---
# Using DNF

DNF is the command-line software manager. It handles installing, removing, and updating packages and repositories. Everything you can do in a graphical package manager you can also do with DNF, often faster.

For the full list of commands, read the [DNF5 reference](https://dnf5.readthedocs.io/en/latest/index.html). DNF has two major versions with slightly different commands: [DNF4](https://dnf.readthedocs.io/en/latest/command_ref.html) and [DNF5](https://dnf5.readthedocs.io/en/latest/).

## Common commands

Run each command as an administrator with `sudo`:

- Install a package:  `dnf --refresh install <package-name>`
- Remove a package:  `dnf remove <package-name>`
- Search for a package:  `dnf search <package-name>` (partial names work)
- Clean caches and metadata:  `dnf clean all`
- Update your Rock system:  `dnf --refresh upgrade`
- Update a ROME system:  `dnf --refresh distro-sync`

## Other common commands

- `check-update` checks for updates without downloading or installing.
- `downgrade` reverts a package to its previous version.
- `info` shows what a package is and its version.
- `reinstall` reinstalls the currently installed package.
- `repolist` lists the enabled repositories.

## Abbreviations

DNF accepts short versions of commands:

| Abbreviation | Full command |
| --- | --- |
| `dnf in` | `dnf install` |
| `dnf up` | `dnf upgrade` |
| `dnf rm` | `dnf remove` |
| `dnf dsync` | `dnf distro-sync` |

## Options

| Option | What it does |
| --- | --- |
| `--allowerasing` | Erases installed packages to resolve conflicts. Do not use unless you know what you are doing. |
| `--best` | Uses the newest available package versions, even when dependencies would normally block an update. |
| `--disable` / `--enablerepo=<code>repo_id</code>` | Turn a repository on or off. Often used together with `config-manager`. |
| `--nobest` | Ignores the newest-version rule. |
| `--downloadonly` | Downloads packages without installing them. |
| `--exclude=<code>package_name</code>` | Skips this package during an operation. |
| `-y, --assumeyes` | Answers "yes" to all prompts automatically. |

## Using DNF

```bash
dnf --help
man dnf4
```

Reading the help message takes about one minute; the man page takes a few minutes.

The man page for DNF4 and the [DNF5 command reference](https://dnf5.readthedocs.io/en/latest/ref_cli.html) both list these commands and options in detail.

## Related Topics

- [Managing Software](../software.en.html)
- [Software Repository Selector](./repositories-tldr.en.html)
