---
layout: default
title: Build System
nav_order: 10
parent: Developer Docs
has_toc: true
lang: en
---
# Build System

The build system is *ABF* (Automated Build Farm). You submit packages to ABF, and it builds them for every architecture. This is where your changes first compile and the team tests them before they move through the release plan.

## What ABF Does

ABF runs your package through every target architecture, checks the build, and publishes the result. Submitting a package with `abf submit` creates a build job. The build can take a while, so ABF queues jobs and runs them in order.

## The Basic Workflow

This workflow compiles your package across all target architectures and submits it to ABF for testing and review.

1. Write the spec file and package files on your machine.
2. Build locally with `abb build` to catch problems early. See [How to Build and Submit Packages](../how-to-build-and-submit-packages.en.html).
3. Submit the package with `abf submit`.
4. Watch the build in the ABF project page. Fix failures, edit the spec, and submit again.

The [packaging guide](../how-to-build-and-submit-packages.en.html) walks you through each step.

## Submitting a Package

After you submit a package, it becomes an ABF project. The build log shows the exact failure. Most early-build problems are small: a missing dependency, a wrong path, a file the package forgot to install. The log tells you which.

{: .note }

Build locally before submitting. It is faster to fix a local failure than a queued one, and you control your own build.

## Building for Release

A Cooker build is not enough. Packages move through the [release plan](../community/releases/index.en.html)-—-Cooker, then the rolling release, then the stable release. QA verifies each package before it leaves Cooker. Do not edit the release repositories directly.

## Related Topics

- [How to report a bug](../report-bug.en.html)
- [Getting started with QA](../getting-started-with-qa.en.html)
