---
layout: default
title: Repository Policies
nav_order: 70
parent: Releases
has_toc: true
lang: en
---
# Repository Policies

The team maintains the four repositories and their update flow. You do not need to know the internals, but it helps to understand the rules.

## Cooker

Cooker is an experimental branch that can break. You can do many things here, including updating to a beta or git snapshot. Before making a big change — switching a major system component, a lot of rebuilds, dropping a widely used package, changing something likely to break other people's hardware — coordinate it. Bring it up at a Tech Committee meeting, open a pull request and wait for others, or ask on the Cooker channel and wait for replies. Cooker is usually open but freezes at times to consolidate.

## ROME

ROME must stay usable at all times. Anything sent to ROME must build in Cooker first. The team sends packages to `rolling/testing`, not the release repository; QA moves them to release after testing. ROME normally uses released versions, not betas, unless upstream is in a "release forever" cycle. ROME freezes briefly before new releases so each release is a good snapshot.

## Release

Release must stay usable at all times. Anything sent there must build in Cooker and ROME testing first. ROME must stay usable at all times, so QA gate every move from testing.

## End of the line

Once a package reaches its update channel, the team marks it complete and moves on to the next. Do not spam maintainers asking when something will be released or updated — they work in their free time. If you would like to help, read how to [create, maintain, and update packages](../../dev/how-to-build-and-submit-packages.en.html) and [join the QA team](../../dev/getting-started-with-qa.en.html).
