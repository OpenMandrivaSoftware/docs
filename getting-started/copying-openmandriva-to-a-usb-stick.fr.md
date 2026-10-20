---
layout: default
title: Copier OpenMandriva sur une clé USB
nav_order: 20
parent: Premiers pas
has_toc: true
lang: fr
---
# Copier OpenMandriva sur une clé USB

Le fichier ISO que vous avez téléchargé à l'étape précédente ne peut pas être copié directement sur une clé USB pour l'installation. À la place, toute la clé USB doit être réservée au contenu de l'ISO : il faut donc la copier bloc par bloc. Assures-vous d'avoir une clé USB d'au moins 8 Go.

Si vous êtes sur Windows, certains programmes peuvent le faire pour vous. Si vous êtes déjà sous un autre Linux, vous avez tout ce qu'il vous faut.

## Créer une clé USB d'installation sous Windows

1. Téléchargez Balena Etcher depuis ce site : <https://etcher.balena.io>.

1. Cliquez sur l'exécutable Etcher depuis la notification de téléchargement de votre navigateur.

1. Etcher démarre. Suivez la [documentation Etcher](https://etcher-docs.balena.io/) pour vous aider avec Etcher.

## Créer une clé USB d'installation sous Linux

Balena Etcher étant également disponible sous Linux, vous pouvez l'utiliser pour créer votre clé_usb amorçable. Cela dit, vous n'êtes pas obligé·e de l'utiliser ; si vous ne voulez rien installer, vous pouvez créer votre clé d'installation directement depuis la CLI.

1. Insère la clé USB, mais ne la monto ni ne l'ouvre.

1. Ouvre un terminal et tape `lsblk`. Une liste apparaît, showing tous les appareils de ta machine :

    ```bash
     NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
     sda           8:0    1  58.2G  0 disk
     ├─sda1        8:1    1  58.2G  0 part
     └─sda2        8:2    1    32M  0 part
     zram0       253:0    0  15.6G  0 disk [SWAP]
     zram1       253:1    0     0B  0 disk
     zram2       253:2    0     2G  0 disk /var/tmp
     nvme0n1     259:0    0   1.9T  0 disk
     ├─nvme0n1p1 259:1    0   300M  0 part /boot/efi
     ├─nvme0n1p2 259:2    0   1.9T  0 part /var/log
     │                                     /var/cache
     │                                     /home
     │                                     /boot
     │                                     /
     └─nvme0n1p3 259:3    0  12.7G  0 part [SWAP]
    ```

1. Trouve l'appareil USB ; c'est généralement sous la forme sdX, où X est une lettre. Dans l'exemple ci-dessus, c'est sda.

1. Va dans le dossier où tu as téléchargé l'ISO ; par défaut, c'est ton dossier Téléchargement (Downloads).

1. Tape la commande suivante :

    ```bash
     dd bs=4M if=[chemin vers l'iso openmandriva] of=/dev/[usb device] status=progress oflag=sync
    ```

    Par exemple, si tu es dans ton dossier Téléchargement, que le nom du fichier ISO d'OpenMandriva est `OpenMandrivaLx.rolling-snapshot.20260927.4760-plasma6wayland.znver1.iso`, et que ta clé USB est identifiée sous sda, tu taperais ceci :

    ```bash
     dd bs=4M if=OpenMandrivaLx.rolling-snapshot.20260927.4760-plasma6wayland.znver1.iso of=/dev/sda status=progress oflag=sync
    ```

    Appuie sur Entrée pour exécuter la commande.

Celà prend un certain temps, mais l'ISO sera finalement écrit sur ta clé USB. Une fois terminé, tu es prêt·e à installer !
