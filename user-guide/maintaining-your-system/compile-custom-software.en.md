---
layout: default
title: Compile Custom Software
nav_order: 40
parent: Maintaining Your System
has_toc: true
lang: en
---

# Compile Custom Software

OpenMandriva uses *clang* as its default compiler, a unique feature of the distribution. Since OpenMandriva 5.0, clang compiles the kernel and kernel modules. *GCC* remains available for compatibility with software that specifically requires it; compile new software with clang by default.

{: .warning }

GCC remains available for compatibility but is not used for kernel or kernel module compilation. Use clang by default; switch to GCC only when software specifically requires it.

## Before You Compile

Building from source takes more time and maintenance than installing from repositories, so check for an existing package first.

1. Check whether the software already exists in the repositories. Search using *DNF*, *DnfDrake*, or *OM Installer* before building from source.

1. If the package is missing, you can request it through the forum or GitHub.

## Install Development Tools

Development tool packages provide the compilers, headers, and libraries needed to build software from source.

1. Install the basic development tool sets from OM Welcome:

   ![The OM Welcome development tools page shows available tool sets for installation.](./images/compile-custom-software-01.png)

1. Or install them from the command line:

   ```bash
   sudo dnf install task-devel task-c-devel task-c++-devel
   ```

## Compile a Program

Build scripts default to GCC, but you can direct them to use clang by passing compiler variables:

```bash
make CC=clang CXX=clang++ LD=ld.lld AR=llvm-ar NM=llvm-nm OBJCOPY=llvm-objcopy OBJDUMP=llvm-objdump STRIP=llvm-strip
```

## Package Your Software

Distribute your software through the official repositories by joining the packaging team. See [How to Build and Submit Packages](../../dev/how-to-build-and-submit-packages.en.html) for instructions.

## Related Topics

- [Maintaining Your System](../maintaining-your-system.en.html)
- [How to Build and Submit Packages](../../dev/how-to-build-and-submit-packages.en.html)
