---
layout: default
title: Building a Go Package
nav_order: 20
parent: Building and Submitting Packages
has_toc: true
lang: en
---
# Building a Go Package

Go projects depend on external modules. Because ABF builds run offline, they cannot fetch modules during a build. Before you build a Go package, you must download the modules your project needs and bundle them with the source. For the rest of the process, follow the [general package workflow](../building-and-submitting-packages.en.html).

## Vendor the Go Modules

Vendoring copies the project's modules into the source tree, so the build does not require network access. Work in the directory that holds your package source.

1. Download the source archive for the package and extract it:

   ```bash
   tar -xf [package-name]-[version].tar.gz
   ```

1. Enter the source directory:

   ```bash
   cd [package-name]-[version]
   ```

1. Pre-download the project's modules into a `vendor` directory:

   ```bash
   go mod vendor
   ```

1. Compress the `vendor` directory into a tarball:

   ```bash
   tar -cJvf [package-name]-[version]-vendor.tar.xz vendor
   ```

The `vendor` tarball is the second source file for the package. Keep it next to your `.spec` file.

## Write the Go Spec File

The spec file points ABF to two source archives: the project source and the `vendor` tarball. Use this template as a starting point:

```spec
Name: [package-name]
Summary: Short description of the project
URL: https://github.com/[user]/[package-name]
Source0: https://github.com/[user]/[package-name]/archive/refs/tags/[package-name]-[version].tar.gz
Source1: [package-name]-[version]-vendor.tar.xz

BuildRequires: golang

%description
Short description of the project.

%prep
%autosetup -p1
tar -zxf %{S:1}

%build
go build -o %{name} ./cmd/%{name}/

%install
install -Dm755 %{name} %{buildroot}/usr/bin/%{name}

%files
%{_bindir}/%{name}
```

`Source0`: the project source archive.

`Source1`: the `vendor` tarball you created.

`BuildRequires: golang`: provides the Go compiler and build tools.

`%autosetup -p1`: unpacks the source archive.

`tar -zxf %{S:1}`: extracts the vendored modules.

`go build -o %{name} ./cmd/%{name}/`: compiles the project. The `-o %{name}` flag names the output binary after the package.

`install -Dm755 %{name} %{buildroot}/usr/bin/%{name}`: installs the binary.

## Build and Submit

Run `abb build` to build the package locally and fix the errors it reports. Submit the package with `abf submit`. The [general package workflow](../building-and-submitting-packages.en.html) covers the remaining steps.

## Related Topics

- [Building and Submitting Packages](../building-and-submitting-packages.en.html)
- [Building a Rust Package](./building-a-rust-package.en.html)
- [Building a Python Package](./building-a-python-package.en.html)
- [Installing Packaging Tools](../preparing-your-system/packaging-tools.en.html)
- [Understanding RPM Spec Files](../understanding-rpm-spec-files.en.html)
- [Preparing Your System](../preparing-your-system.en.html)
