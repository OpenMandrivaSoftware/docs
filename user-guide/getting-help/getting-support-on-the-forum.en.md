---
layout: default
title: Getting Support on the Forum
nav_order: 10
parent: Getting Help
has_toc: true
lang: en
---

# Getting Support on the Forum

When you cannot solve a problem on your own, the OpenMandriva community forum is the best place to ask for help. Community members volunteer their time and knowledge---no one is paid to assist you. Follow these guidelines to get useful responses quickly.

{: .important }
Spend time carefully describing your question in as much detail as you can. If you do not, you cannot expect that people, however well-intentioned, reply.

## Before You Post

1. Search the [forum](https://forum.openmandriva.org/search) for existing topics similar to yours.

2. Read the [Release Notes and Errata](../../community/releases/current-releases.en.html) for your version of *OpenMandriva Lx* before reporting an issue.

3. Check the [Resources category](https://forum.openmandriva.org/c/resources/13)---most common questions are already answered there, including detailed how-tos.

4. Choose the proper category for your post.

5. Use a descriptive subject title. Avoid vague titles like "Help me!" or "It's broken." Posts like "Graphics broken" are useless unless you tell what graphics hardware and driver you use. Posts like "System broken after updates" are useless unless you list the packages that updated recently---see [the list of latest updates](../managing-software/tips-and-tricks/list-the-latest-updates.en.html).

6. Tag your post with relevant information.

## Writing Your Post

1. Specify your OpenMandriva version (Cooker, ROME, or Rock with the version number) and architecture (x86_64, znver1, or aarch64). Note whether you are on real hardware or in a virtual machine like VirtualBox.

2. Specify your desktop environment: Plasma, LXQt, or other.

3. Be precise: explain exactly what happens, under what conditions, and what you expected to happen. If necessary, give steps to reproduce your issue. Include any external links that may be relevant---other project bug trackers, upstream errata, FAQs, or how-tos.

4. Write in correct language. If English is not your native language, check your text with an online translator. Mention that you used a translator. If you are a native English speaker, use simple, basic writing that non-native users can understand. Avoid slang and idiomatic expressions.

5. Do not type in ALL CAPS---this is perceived as shouting.

6. Provide screenshots if relevant. Use the upload icon with the up arrow in the forum editor.

## Include Technical Details

1. If your console output is not in English, prefix commands with `LC_ALL=C`. This forces English output, which makes it easier for all developers and helpers to understand:

   ```bash
   $ sudo LC_ALL=C dnf [your-command]
   ```

2. Provide logs and/or output of `journalctl` pertinent to the issue.

3. Provide the output of `inxi -Fz` to show your hardware information. See [Get Logs and Hardware Info for Issue Reports](./get-logs-and-hardware-info-for-issue-reports.en.html) for details.

4. When someone requests the full console output, include everything---starting from the command you typed to the end---not only the part you assume is relevant.

5. Post code using the [code formatting instructions](https://forum.openmandriva.org/t/3863). For large outputs (more than 20-30 lines), save the code in a `.txt` file and upload it, or use [Pastebin](https://pastebin.com/) or a similar service.

6. Give as much additional technical information as you think may be relevant---hardware details, software versions, and logs. If you do not know how to gather something, ask for help.

7. Be patient. The community is small and does its best. You may be asked for additional information or given actions to perform.

## After You Get a Solution

1. If your problem is solved, [mark which reply solved the problem](https://forum.openmandriva.org/t/new-feature-solved-topic/150).

2. If you found a solution on your own, share it so that it is available for others.

3. Post a short note about how your problem was resolved. This helps others who encounter the same issue.

## Be Kind

Community members who help you are volunteering their time.

- Use "Please" and "Thank you" generously.
- "Like" posts that were helpful to make people earn karma points in the forum.
- Be kind and show appreciation for those dedicated to solving your issue. Courtesy never hurts.

{: .tip }
Other Linux distributions such as Arch Linux, Fedora, Gentoo, openSUSE, and Ubuntu also have good wikis and documentation.

## Related Topics

- [How to Report a Bug](./how-to-report-a-bug.en.html)
- [Get Logs and Hardware Info for Issue Reports](./get-logs-and-hardware-info-for-issue-reports.en.html)
- [Using DNF](../index.en.html)
