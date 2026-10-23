---
layout: default
title: Preparing Your System
nav_order: 20
parent: Developer Docs
has_toc: true
lang: en
---
# Preparing Your System

Before you build and submit your first package, prepare an isolated environment. Cooker---OpenMandriva's development branch---changes quickly, and package updates can break your system at any time. Always check the `[code]#openmandriva-cooker:matrix.org` Matrix channel before applying updates. Running Cooker on your daily system puts your working desktop at risk.

Preparing your system takes three steps:

1. [Installing and Using Virt Manager](./preparing-your-system/index.en.html)---set up the virtualization platform that runs your Cooker virtual machine.
1. [Creating a Cooker VM](./preparing-your-system/creating-cooker-vm.en.html)---download a Cooker ISO and install it in a virtual machine.
1. [Installing Packaging Tools](./preparing-your-system/packaging-tools.en.html)---install the `packaging-tools` package and learn the `v*` template utilities.

Complete all three before you start writing spec files.
