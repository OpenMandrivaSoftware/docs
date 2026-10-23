---
layout: default
title: Using Cooker
nav_order: 10
parent: Developer Docs
has_toc: true
lang: en
---
# Using Cooker

Cooker is the development branch of OpenMandriva Lx. It reflects the current progress of work across all lines. Packages build in Cooker first, then move through the release plan to Rolling and eventually to a stable release. Package updates can break your system if you apply them at the wrong time, so always check the Matrix channel before updating.

## What Cooker Needs

The OpenMandriva Lx distribution exists through two major fields of technical contribution:

- Creation and maintenance of the tools, configuration, and art special to the distribution, such as the installer, the configuration center, and themes.
- Consistent packaging of thousands of programs and libraries so they are available to users in a simple, unified way.

Guidelines and rules for both areas are documented in the [Repository Policies](../community/releases/repository-policies.en.html).

## Get Cooker

Download the latest Cooker snapshot ISO files from the official [OpenMandriva Cooker](https://www.openmandriva.org/info-cooker/) page. Choose the ISO for your architecture.

{: .warning }

Package updates in Cooker can break your system at any time. Always check the `[code]#openmandriva-cooker:matrix.org` Matrix channel before applying updates. Use Cooker only in a test environment.

## Run Cooker in a Virtual Machine

Because package updates can break your system at any time, run Cooker in a virtual machine or on a separate partition rather than installing it alongside your everyday system.

[Preparing Your System](./preparing-your-system.en.html) guides you through installing Virt Manager and creating a Cooker VM.

## Related Topics

- [Preparing Your System](./preparing-your-system.en.html)
- [Building and Submitting Packages](./building-and-submitting-packages.en.html)
- [Repository Policies](../community/releases/repository-policies.en.html)
