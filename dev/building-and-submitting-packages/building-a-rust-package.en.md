---
layout: default
title: Building a Rust Package
nav_order: 10
parent: Building and Submitting Packages
has_toc: true
lang: en
---
# Building a Rust Package

Rust projects depend on many small libraries, called *crates*, that ship on [crates.io](https://crates.io). Because ABF builds run offline, they cannot fetch crates during a build. Before you build a Rust package, you must download every crate your project needs and bundle them with the source. For the rest of the process, follow the [general package workflow](../building-and-submitting-packages.en.html).

## Vendor the Rust Crates

Vendoring copies the project's crates into the source tree, so the build does not require network access. Work in the directory that holds your package source.

1. Download the source archive for the package and extract it:

   ```bash
   tar -xf [package-name]-[version].tar.gz
   ```

1. Enter the source directory:

   ```bash
   cd [package-name]-[version]
   ```

1. Pre-download the project's crates into a `vendor` directory:

   ```bash
   cargo vendor
   ```

1. Compress the `vendor` directory into a tarball:

   ```bash
   tar -cJvf [package-name]-[version]-vendor.tar.xz vendor
   ```

The `vendor` tarball is the second source file for the package. Keep it next to your `.spec` file.

## Write the Rust Spec File

The spec file points ABF to two source archives: the project source and the `vendor` tarball. Use this template as a starting point:

```spec
Name: [package-name]
Summary: Short description of the project
URL: https://github.com/[user]/[package-name]
Source0: https://github.com/[user]/[package-name]/archive/refs/tags/[package-name]-[version].tar.gz
Source1: [package-name]-[version]-vendor.tar.xz

BuildRequires: rust-packaging

%description
Short description of the project.

%prep
%autosetup -p1
tar -zxf %{SOURCE1}
%cargo_prep -v vendor

%build
cargo build --frozen --release

%install
install -Dpm 0755 -t target/release/%{name} %{buildroot}%{_bindir}

%files
%{_bindir}/%{name}
```

`Source0` points to the project source archive.

`Source1` points to the `vendor` tarball you created.

`BuildRequires: cargo` provides the Rust build tools and the `%cargo_prep` macro.

`%autosetup -p1` unpacks the source archive.

`%cargo_prep -v vendor` tells `cargo` to use the vendored crates.

`cargo build --frozen --release` compiles the project without network access. The `--frozen` flag makes `cargo` refuse to download anything.

## Point `cargo` to the Vendored Sources

`%cargo_prep -v vendor` works for most projects. If it fails, configure `cargo` directly with a `.cargo/config.toml` file. Remove the `%cargo_prep -v vendor` line from your `%prep` section, and add these commands after `%autosetup` unpacks the source:

```bash
mkdir -p .cargo
cat > .cargo/config.toml << EOF
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF
```

The `[source.crates-io]` block replaces the normal crates.io source with the vendored one. The `[source.vendored-sources]` block names the directory that holds the crates.

## Vendor Multiple Rust Projects

Some packages bundle more than one Rust project. Vendor each project's crates and give each project a `.cargo/config.toml` file that points to the shared `vendor` directory.

{: .tip }
Each sub-project must reference the shared `vendor` directory with a relative path that climbs back to it, such as `../../vendor`.

1. Vendor the second project. The `-s` flag tells `cargo` to include another project's `Cargo.toml` in the vendoring process:

   ```bash
   cargo vendor -s other/project/Cargo.toml
   ```

1. Add a `.cargo/config.toml` file to each project, using the same structure shown above. For the main project, set `directory = "vendor"`. For a sub-project, set `directory = "../../vendor"` so it finds the shared crates.

## Build and Submit

Run `abb build` to build the package locally and fix the errors it reports. Submit the package with `abf submit`. The [general package workflow](../building-and-submitting-packages.en.html) covers the remaining steps.

## Related Topics

- [Building and Submitting Packages](../building-and-submitting-packages.en.html)
- [Building a Python Package](./building-a-python-package.en.html)
- [Building a Go Package](./building-a-go-package.en.html)
- [Installing Packaging Tools](../preparing-your-system/packaging-tools.en.html)
- [Understanding RPM Spec Files](../understanding-rpm-spec-files.en.html)
- [Preparing Your System](../preparing-your-system.en.html)
