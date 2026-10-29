---
layout: default
title: Setting Up a Mirror
nav_order: 25
parent: OpenMandriva Community
has_toc: true
lang: en
---
# Mirroring

OpenMandriva mirrors let you download packages and install images quickly. A flat mirror topology keeps them honest: every mirror syncs directly from the origin (ABF), so no lagging mirror is propagated to others, and each mirror can be as fresh as the source.

## For end users

You rarely need to pick a mirror yourself. Point your tools at **`mirror.openmandriva.org`** (Mirrorbits): it redirects to the nearest healthy mirror and falls back to ABF if a file is missing. For a live, per-mirror reliability ranking, see the [Mirror status](https://mirror.openmandriva.org/status) page.

A plain text file on our repositories shows which mirror you will be redirected to:

- Immediate redirection: http://mirror.openmandriva.org/release_current/README.txt
- Visual list of mirrors: http://mirror.openmandriva.org/release_current/README.txt?mirrorlist

## Looking for a mirror

- **Mirmon** (the mirrors manager) shows which mirrors are up to date: https://mirmon.openmandriva.org/
- **Mirrorbits** (the nearby-mirror redirector) shows where mirrors are distributed around the world: https://mirror.openmandriva.org/?mirrorstats

## Setting up a mirror

If you want to support the project by running a mirror, sync directly from our origin (ABF distribution) so your mirror stays as fresh as the source:

```bash
rsync -av rsync://abf-downloads.openmandriva.org/openmandriva/ /local/path/
```

{: .important }
Do not forget the `TIME.txt` file — Mirmon and Mirrorbits need it to work correctly. You also need at least **600 GB** of free disk space.

## The primary mirror

Our T0 mirror, ABF, is where packages are compiled and distributed. It holds more than any other mirror: source packages, debug packages, old release packages, personal repositories, and more. Its content can be explored at <http://abf.openmandriva.org>.

Mirrorbits always redirects to ABF if a file does not exist on any mirror.

## Related Topics

- [Release Codenames](./releases/release-codenames.en.html)
- [Repository Policies](./releases/repository-policies.en.html)
