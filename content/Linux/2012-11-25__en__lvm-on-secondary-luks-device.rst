============================
LVM on secondary LUKS device
============================


:tags: Arch, Encryption, Linux, Security
:author: Markus Holtermann


Today I ran into a problem when I set up my new `SSD`_. I have two fully
encrypted disks (one SSD and one HDD) and two `volume groups (VGs)`_ on top.
Each disk has its own VG. I thought about the following partition scheme.
``sda`` is the SSD and ``sdb`` the HDD::

   /dev/sda2            → LUKS → /dev/mapper/luksmain
   /dev/sdb1            → LUKS → /dev/mapper/luksdata
   /dev/mapper/luksmain → LVM  → /dev/mapper/main
   /dev/mapper/luksdata → LVM  → /dev/mapper/data

And from these block devices set up the following file systems::

   /dev/mapper/main-root     /
   /dev/sda1                 /boot
   /dev/mapper/main-home     /home
   /dev/mapper/data-var      /var
   /dev/mapper/data-music    /home/Music
   /dev/mapper/data-videos   /home/Videos
   /dev/mapper/main-mysql    /var/lib/mysql

As one can see, the `logical volume (LV)`_ ``data-var`` is required by the system.
It contains e.g. the logs or the package cache.

To use it during startup, enable the ``lvm-on-luks`` systemd service::

   systemctl enable lvm-on-luks.service


.. _SSD: http://en.wikipedia.org/wiki/Solid-state_drive
.. _volume groups (VGs): http://en.wikipedia.org/wiki/Volume_group
.. _logical volume (LV): http://en.wikipedia.org/wiki/Logical_volume