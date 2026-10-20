---
layout: default
title: Set Your User Avatar
nav_order: 10
parent: Post Installation Configuration
has_toc: true
lang: en
---

# Set Your User Avatar

The user avatar is the picture that represents your account in the login screen, user switcher, and system settings. You can choose from default images or upload a custom picture.

First, verify that the `om-user-manager` package is installed:

```bash
$ rpm -q om-user-manager
```

If the command returns no output, install the package:

```bash
$ sudo dnf --refresh install om-user-manager
```

![User manager installed](./images/set-user-avatar-01.jpg)

## Set Your Avatar

1. Open *System Settings*.

   ![System Settings](./images/set-user-avatar-02.jpg)

1. Navigate to *Account Details > User Account*.

   ![Account Details](./images/set-user-avatar-03.jpg)

1. Click your username to reveal avatar options.

   ![Username](./images/set-user-avatar-04.jpg)

1. Click the default user image to open the avatar selection dialog.

   ![Avatar dialog](./images/set-user-avatar-05.jpg)

1. Browse the available images. Adjust the icon size to see all options more easily, then pick one you like.

   ![Pick avatar](./images/set-user-avatar-06.jpg)

1. Apply the changes.

   > **Warning:** You will be asked for your root password before leaving the settings.
   {: .warning }

   ![Applied avatar](./images/set-user-avatar-07.jpg)

## Use a Custom Image

To use a custom image as your avatar:

1. Place the image file in `/usr/share/mdk/faces/`:

   ```bash
   $ sudo cp [your-image.jpg] /usr/share/mdk/faces/
   ```

   ![Custom image location](./images/set-user-avatar-08.jpg)

1. Return to *System Settings > Account Details > User Account*, click your avatar, and select your custom image.

   ![Custom avatar](./images/set-user-avatar-09.jpg)

## Related Topics

- [Post Installation Configuration](./index.en.html)
- [Maintaining Your System](../maintaining/index.en.html)
