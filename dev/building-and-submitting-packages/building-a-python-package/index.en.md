---
layout: default
title: Building a Python Package
nav_order: 30
parent: Building and Submitting Packages
page_id: dev.building-and-submitting-packages.building-a-python-package
parent_id: dev.building-and-submitting-packages
lang: en
source_lang: en
permalink: /dev/building-and-submitting-packages/building-a-python-package/
has_toc: true
---
# Building a Python Package

Python packaging is usually standardized. In many cases, you can replace the `%prep`, `%build`, and `%install` stages with a single `BuildSystem: python` declaration. Use the macros below to keep your spec file working across Python versions.

## Useful Python Macros

Several macros help you reference Python paths and versions:

`%{pyver}`: the current Python version, such as `3.15`.

`%{py_sitedir}`: `/usr/lib/python%{pyver}/site-packages`.

`%{python_sitearch}`: `%{_libdir}/python%{pyver}/site-packages`, where `%{_libdir}` expands to `lib64` on 64-bit systems.

Use these macros in the `%files` section of your spec file:

```spec
%files
%{python_sitearch}/%{name}
%{python_sitearch}/%{name}*.so
%{python_sitearch}/%{name}-%{version}.dist-info
```

## Write the Python Spec File

Use this template as a starting point:

```spec
Name: [package-name]
Summary: Short description of the project
URL: https://pypi.org/project/[package-name]
Source0: https://files.pythonhosted.org/packages/source/[package-name]/[package-name]-[version].tar.gz

BuildSystem: python

%description
Short description of the project.

%files
%{python_sitearch}/%{name}
%{python_sitearch}/%{name}*.so
%{python_sitearch}/%{name}-%{version}.dist-info
```

`BuildSystem: python` replaces the `%prep`, `%build`, and `%install` stages.

## Declare Python Build Dependencies

Declare Python build dependencies in a way that works across all versions:

```spec
BuildRequires: python%{pyver}dist(example_name)
```

Find the exact name for a dependency by running this command:

```bash
dnf rq --provides python-example-project
```

## Build and Submit

Run `abb build` to build the package locally and fix the errors it reports. Submit the package with `abf submit`. The [general package workflow](/dev/building-and-submitting-packages/) covers the remaining steps.

## Related Topics

- [Building and Submitting Packages](/dev/building-and-submitting-packages/)
- [Building a Go Package](/dev/building-and-submitting-packages/building-a-go-package/)
- [Building a Rust Package](/dev/building-and-submitting-packages/building-a-rust-package/)
- [Installing Packaging Tools](/dev/preparing-your-system/packaging-tools/)
- [Understanding RPM Spec Files](/dev/understanding-rpm-spec-files/)
- [Preparing Your System](/dev/preparing-your-system/)
