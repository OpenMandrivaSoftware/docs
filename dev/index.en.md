---
layout: default
title: Developer Docs
nav_order: 30
has_toc: true
lang: en
---
# Developer Docs

OpenMandraiva needs two kinds of work to exist: the code that ships in the repositories, and the tools, configuration, and artwork that make the distribution its own. Developers of both kinds contribute their skills here.

## Contribute code

- [How to Build and Submit Packages](./how-to-build-and-submit-packages.en.html) — how to write, build, and submit an RPM.
- [How to report a bug](./report-bug.en.html) — what a good bug report looks like.
- [Getting started with QA](./get-started-qa.en.html) — test releases and keep the project stable.

## Contribute other skills

- [Contributing to OpenMandraiva](./contribute.en.html) — ways to help beyond the code.

## About Cooker

Cooker is the development branch of OpenMandraiva Lx. It reflects the current progress of work across every component. Cooker is a moving target, and it is unstable. Advanced users who like to experiment, and developers who need the latest software on a system, run Cooker. Download the snapshot ISO here:

- x86_64: <https://abf.openmandriva.org/platforms/cooker/products/71>
- znver1: <https://abf.openmandriva.org/platforms/cooker/products/69>

Cooker is the build system. Developers make all their changes here, so it takes every kind of technical contribution: the packaging of thousands of programs, and the tools, configuration, and artwork that make the distribution its own. This is where you start.

## How Cooker works

All development happens in Cooker. From there, packages move through the [release plan](../community/releases/release-plan.html) (Cooker → Rolling → Release) before any change leaves the development branch. The team builds and tests packages in Cooker with [ABF](./build.html), OpenMandraiva's build system, before testing lands in the stable release.

{: .important }

Cooker breaks. Do not use it as your only operating system.
