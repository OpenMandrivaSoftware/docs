---
layout: default
title: Using Cooker
nav_order: 10
parent: Developer Docs
has_toc: true
lang: en
---
# Using Cooker

Cooker is the development branch of OpenMandriva Lx. It reflects the current progress of work across all lines and is considered a moving, unstable target. Packages build in Cooker first, then move through the release plan to Rolling and eventually to a stable release.

## What Cooker Needs

The OpenMandriva Lx distribution exists through two major fields of technical contribution:

- Creation and maintenance of the tools, configuration, and art special to the distribution, such as the installer, the configuration center, and themes.
- Consistent packaging of thousands of programs and libraries so they are available to users in a simple, unified way.

Guidelines and rules for both areas are documented in the [Repository Policies](../community/releases/repository-policies.en.html).

## Get Cooker

Download the latest Cooker snapshot ISO files from the official [OpenMandriva Cooker](https://www.openmandriva.org/info-cooker/) page. Choose the ISO for your architecture.

{: .warning }

OpenMandriva cannot provide support for Cooker systems due to its unstable nature. Use it only in a test environment.

## Run Cooker in a Virtual Machine

Because Cooker is unstable and breaks frequently, never install it on your daily driver. Instead, run it in a virtual machine or on a separate partition. Installing Cooker alongside your everyday system can leave you with an unusable desktop when a package update fails.

[Preparing Your System](./preparing-your-system.en.html) guides you through installing Virt Manager and creating a Cooker VM.

## Related Topics

- [Preparing Your System](./preparing-your-system.en.html)
- [Building and Submitting Packages](./building-and-submitting-packages.en.html)
- [Repository Policies](../community/releases/repository-policies.en.html)
