---
layout: default
title: Report Bugs Effectively
nav_order: 30
parent: Bug Report Tool
has_toc: true
lang: en
---

# Report Bugs Effectively

A good bug report lets a developer see your problem happen on their own machine. This guide explains how to write reports that get results.

## Give Details, Not Vague Statements

When you say "It doesn't work," you give the developer nothing to investigate. Since the software works for them, either you are doing something differently or your environment differs. Provide all the information you can---more is almost always better than less.

Check existing bug lists before reporting. If the bug is already known, adding details helps more than duplicating the report.

## Let the Developer Reproduce It

To fix a bug, the developer needs to see it fail on their own machine. Give step-by-step instructions they can follow exactly:

- For graphical programs: which buttons you pressed and in what order.
- For command-line programs: the exact command you typed.
- Wherever possible, include a verbatim transcript of the session---your commands and the computer's output.

If the program reads a file, include a copy. If it talks to a network service, describe the service and software.

## Describe What Happened

If the developer runs your steps but nothing goes wrong, you have not given enough information. Describe everything you observed---what appeared on screen, what you expected to see, and how they differ.

Note every error message, especially any numbers in them. Numbers often contain clues the programmer can read even when the text description is vague.

## Do Not Try Random Fixes

When something goes wrong, stop and take note of the current state. Do not try reinstalling software, running cleanup tools, or making other changes---each action can destroy the evidence the developer needs.

If you do get the system working again, try to reproduce the bug a second time. Developers fix reproducible bugs much faster.

## Report Symptoms, Not Diagnoses

It is tempting to tell the developer what you think is wrong. Resist this urge---state the symptoms instead. Provide your own diagnosis as an optional extra, not a replacement for the symptoms.

If asked for more information, do not make it up. Try the exact command the developer asked for so they can see the real error message.

## Handle Intermittent Bugs

Intermittent bugs---ones that fail sometimes but not always---are the hardest to fix. Gather as much detail as you can:

- Try on another machine.
- Run the procedure multiple times and note the frequency.
- Record what you were doing when the failure occurred.
- Note the system configuration---especially version numbers for the program, the OS, and any other involved software.

The developer needs to know whether the bug is specific to your machine or happens more broadly.

## Write Clearly

- Be specific. If an action has multiple ways to perform it, state which one you used.
- Be verbose. If you provide too much information, the developer ignores the irrelevant bits. If you provide too little, they have to ask follow-up questions.
- Avoid ambiguous pronouns. Instead of "it crashed," write "FooApp crashed."
- Read your report back to yourself before sending it. Follow the steps yourself to check that you did not miss anything.

## Summary

1. Let the developer see the failure happen. Give them precise, reproducible steps.
1. If that fails, describe what went wrong---including exact error messages and your expectations.
1. When something unexpected happens, stop and take notes. Do not try random fixes.
1. Report symptoms first; your own diagnosis is optional.
1. Have version numbers ready---they will likely be needed.
1. Write clearly and precisely.

---

*Based on ["How to Report Bugs Effectively"](https://www.chiark.greenend.org.uk/~sgtatham/bugs.html) by Simon Tatham. Used under the [OpenContent Licence](https://www.opencontent.org/openpub/).*

## Related Topics

- [Getting Started with QA](../getting-started-with-qa.en.html)
- [Bug Report Tool](./index.en.html)
- [How to Report a Bug](../report-bug.en.html)
- [Release QA Checklist](./release-qa-checklist.en.html)
