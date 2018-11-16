==============================================
Flashing Android 5 "Lollipop": Lessons Learned
==============================================

:tags: Android, Lessons Learned
:author: Markus Holtermann
:image: android5.png
:summary: Yesterday evening Google finally published the Android 5 "Lollipop"
   factory images. Eagerly waiting for the update I couldn't hold myself and
   flashed my Nexus 5. This was the first time on the Nexus 5, the previous
   KitKat updates came OTA. Though I'm not really familiar with the whole
   flashing thing, the entire process went smoothly. At least kind of.


Yesterday evening Google finally published the `Android 5 "Lollipop" factory
images`_. Eagerly waiting for the update I couldn't hold myself and flashed my
Nexus 5. This was the first time on the Nexus 5, the previous KitKat updates
came OTA. Though I'm not really familiar with the whole flashing thing (last
time I flashed my HTC Desire HD with some CyanogenMod fork back in summer
2013), the entire process went smoothly. At least kind of.

.. gallery::
   :small: 1
   :medium: 2

   .. image:: android-5-lollipop1.png
      :alt: Android 5 "Lollipop"

   .. image:: android-5-lollipop2.png
      :alt: Android 5 "Lollipop"

This post is more about the things I messed up because they changed or were
different to flashing on the HTC Desire HD and thus is a note to myself what I
should remember in the future.

* The ArchLinux ``[community]`` repository has a ``android-tools`` package that
  provides ``adb`` and ``fastboot``. No problems at that point.

* Everything that is stored under ``/sdcard/`` isn't on an actual SD card, but
  internal storage! Guess what, I didn't realize that until I ran ``fastboot
  oem unlock`` and eventually booted the device later. The device warned me
  that all user data will be wiped - fair enough - but who thought wiping data
  in ``/sdcard/`` is a good idea? Anyway, the data couldn't have been
  important, I had no backup :D

* Be patient during the first boot after flashing the image! The process takes
  time. It took about 20 minutes (guessing, didn't measure it).

* Remember your two factor authentication setup. Make sure to have the backup
  keys for your Google account or you might not be able to login, because you
  just wiped the second part of the 2FA setup. If you're still logged in to
  your Google account on a second device, you can temporarily turn off 2FA,
  setup your smartphone again and activate 2FA again. Make sure you make a copy
  of the **new** backup codes. The old ones won't work anymore. Same goes for
  e.g. GitHub: you can use an active login to re-enable two factor
  authentication

* If you backup some Chrome data (bookmarks, open tabs, extensions, autofill,
  ...), make sure you have the password to get your data back on the
  smartphone. Open ``about:chrome`` in Chrome and check the value for "Explicit
  Passphrase". If it's ``true``, go and find your password. If it's ``false``,
  the data is encrypted with your  Google account password, you only need that
  one.

* If you use Google Play Music or Spotify or similar apps with loads of offline
  data, make sure you have enough time to sync them or you might find yourself
  on a train without Internet connectivity and without Music :(

.. _Android 5 "Lollipop" factory images:
   https://developers.google.com/android/nexus/images
