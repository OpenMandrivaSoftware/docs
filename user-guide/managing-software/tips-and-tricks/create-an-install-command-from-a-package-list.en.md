---
layout: default
title: Create an Install Command from a Package List
nav_order: 30
parent: Tips and Tricks
has_toc: true
lang: en
---

# Create an Install Command from a Package List

Generate a list of all installed packages and turn it into a single `dnf install` command you can run on a fresh installation.

## Generate the Package List

1. Run this command in a terminal to list all installed packages:

   ```bash
   $ dnf list --installed
   ```

   The output is long and difficult to work with directly.

   ![The DNF list command output shows a long list of installed packages in the terminal.](./images/create-an-install-command-from-a-package-list-01.png)

   ![The terminal continues to show package entries further down the list.](./images/create-an-install-command-from-a-package-list-02.png)

2. Save the list to a text file in your home directory:

   ```bash
   $ dnf list --installed > ~/packagelist.txt
   ```

   No output appears on screen; the command creates `packagelist.txt` in your home directory.

   ![The terminal shows the command completed with no visible output.](./images/create-an-install-command-from-a-package-list-03.png)

3. Open `~/packagelist.txt` in *Kate*. The file contains package names along with version numbers, architecture, and repository information that is not useful for reinstalling.

   ![The Kate text editor shows the file open with the package list including version details.](./images/create-an-install-command-from-a-package-list-04.png)

   ![The Kate editor shows the full package list with version and repository columns.](./images/create-an-install-command-from-a-package-list-05.png)

## Clean the Package List

1. In Kate, open the *Find and Replace* tool using `Ctrl+R`.

2. Enable the *Regular expression* option.

3. In the **Find** field, enter `\..*$` and leave the **Replace** field empty.

4. Click *Replace All*.

   ![The Kate editor shows the list after regex replacement with version numbers stripped.](./images/create-an-install-command-from-a-package-list-06.png)

   This removes the version number, architecture, and repository from each line, leaving only package names.

   Most of these packages are installed automatically from the ISO. Manually remove any lines for packages you do not need. If you leave a package in the list that is already installed on the new system, DNF skips it automatically.

   ![The Kate editor shows the cleaned list after manual removal of unwanted packages.](./images/create-an-install-command-from-a-package-list-07.png)

## Build the Install Command

1. Select all text, then choose *Selection > Join Lines* using `Ctrl+J` to combine all package names into a single line.

   ![All package names are joined into one long line in the Kate editor.](./images/create-an-install-command-from-a-package-list-08.png)

2. Prepend `sudo dnf install ` to the start of the line and append `--refresh` at the end:

   ```bash
   sudo dnf install [package-name-1] [package-name-2] [package-name-3] --refresh
   ```

   ![The final install command appears as a single line ready to copy and paste.](./images/create-an-install-command-from-a-package-list-09.png)

## Related Topics

- [Listing Installed Packages](./index.en.html)
- [List the Latest Updates](./list-the-latest-updates.en.html)
- [Using DNF](../index.en.html)
