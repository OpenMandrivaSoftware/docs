---
layout: default
title: Report Bugs Effectively
nav_order: 30
parent: Getting Started with QA
has_toc: true
lang: en
---
# Report Bugs Effectively

A good bug report helps a developer reproduce your problem. Here's how to write reports that get results.

## Give Details, Not Vague Statements

When you say "It doesn't work," you give developers nothing to investigate. Since the software works for them, you are doing something differently or your environment differs. Provide all the information you can; more is almost always better than less. Give them exact error messages. Instead of saying "it doesn't work," describe what happens. 

Check existing bug lists before reporting. If the bug is already known, adding details helps more than duplicating the report.

## Let the Developer Reproduce It

To fix a bug, developers must see it fail on their own machine. Give step-by-step instructions they can follow exactly:

- For graphical programs, which buttons you pressed and in what order.
- For command-line programs, the exact command you typed.
- Wherever possible, include a verbatim transcript of the session (your commands and the computer's output).

If the program reads a file, include a copy. If it talks to a network service, describe the service and software.

## Describe What Happened

If the developer runs your steps but nothing goes wrong, you have not given enough information. Describe everything you observed: what appeared on screen, what you expected to see, and how they differ.

Note every error message, especially any numbers in them. Numbers often contain clues the programmer can read even when the text description is vague.

## Do Not Try Random Fixes

When something goes wrong, stop and notice the current state. Do not try reinstalling software, running cleanup tools, or making other changes. Each action can destroy the evidence the developer needs.

If you do get the system working again, try to reproduce the bug a second time. Developers fix reproducible bugs much faster.

## Report Symptoms, Not Diagnoses

It is tempting to tell the developer what you think is wrong. Resist this urge; state the symptoms instead. Provide your own diagnosis as an optional extra, not a replacement for the symptoms.

If asked for more information, do not make it up. Try the exact command you were asked for so developers can see the real error message.

## Handle Intermittent Bugs

Intermittent bugs (ones that fail sometimes but not always) are the hardest to fix. Gather as much detail as you can:

- Try on another machine.
- Run the procedure multiple times and note the frequency.
- Record what you were doing when the failure occurred.
- Note the system configuration, especially version numbers for the program, the OS, and any other involved software.

Developers must know whether the bug is specific to your machine or happens more broadly.

## Write Clearly

- Be specific. If an action has multiple ways to perform it, state which one you used.
- Be verbose. If you provide too much information, developers ignore the irrelevant bits. If you provide too little, they have to ask follow-up questions.
- Avoid ambiguous pronouns. Instead of "it crashed," write "FooApp crashed."
- Read your report back to yourself before sending it. Follow the steps yourself to check that you did not miss anything.

## Summary

1. Let developers see the failure happen. Give them precise, reproducible steps.

1. If that fails, describe what went wrong: including exact error messages and your expectations.

1. When something unexpected happens, stop and take notes. Do not try random fixes.

1. Report symptoms first; your own diagnosis is optional.

1. Have version numbers ready; they are needed.

1. Write clearly and precisely.

---

*Based on ["How to Report Bugs Effectively"](https://www.chiark.greenend.org.uk/~sgtatham/bugs.html) by Simon Tatham. It was licensed under the OpenContent license, which is now the [Creative Commons CC-BY-SA license](https://creativecommons.org/licenses/by-sa/4.0/deed.en).*

## Related Topics

- [Getting Started with QA](../getting-started-with-qa.en.html)
- [Bug Report Tool](./index.en.html)
- [How to Report a Bug](../../user-guide/getting-help/how-to-report-a-bug.en.html)
- [Release QA Checklist](./release-qa-checklist.en.html)
