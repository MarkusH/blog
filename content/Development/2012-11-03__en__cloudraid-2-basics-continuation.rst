====================================
[CloudRAID] 2. Basics (Continuation)
====================================

:tags: Apache, CloudRAID, Cluster, Eclipse, Encryption, Java, Network,
   Security, Server, Studium
:author: Markus Holtermann


This post is a continuation of the blog series about the student research paper
`CloudRAID`_.


2. Basics
=========


2.3. Background on RAID Technology
----------------------------------

In order to provide data-safety on a common server a RAID can be used. First
introduced in 1988 under the title *Redundant Arrays of Inexpensive Disks*
[DK88]_, the usage of hard drives in an array collection is state of the art
nowadays. The paper by Petterson, Gibson and Katz introduces the RAID levels 1
to 5 as follows.

.. figure:: /images/cloudraid/raid1.png
   :align: right
   :alt: RAID 1

   Source: [Cbu06a]_

**RAID Level 1** provides a high data-safety with a complete fall-back to a
secondary device. This "mirroring" has a space efficiency of 50% of the total
disk capacity [DK88]_ (ch. 7, p. 112) for two disks. In general the space
efficiency is at $$1/n$$. The fault tolerance is $$n-1$$ since all disks
contain the same data and all but the last can fail without any data-loss.

.. figure:: /images/cloudraid/raid2.png
   :align: right
   :alt: RAID 2

   Source: [kna09]_

**RAID Level 2** defines a bit-level striping with an Error Correction Code
(ECC) for recovery [DK88]_ (ch. 8, p. 112) that uses the Hamming Code [Wik12a]_
which is stored on multiple check disks. Nowadays RAID systems of level 2 are
not used any more. They are too prohibitive and do not provide more fault
tolerance than RAID level 3, 4 or even 5. RAID level 2 can recover from one
drive failure and has a space efficiency of $$1 - 1/(n * log_2(n-1))$$
[Wik12b]_.

.. figure:: /images/cloudraid/raid3.png
   :align: right
   :alt: RAID 3

   Source: [Cbu06b]_

**RAID Level 3** provides byte-level striping with a single parity per byte
[DK88]_ (ch. 9, pp. 112f). Taking at least three disks, two for content and one
dedicated for the parity, RAID level 3 provides a space efficiency of ``1 -
1/n`` and a fault tolerance of one broken disk [Wik12b]_. These statistics for
minimum number of disks, space efficiency and fault tolerance are the same for
RAID level 4 and 5.

.. figure:: /images/cloudraid/raid4.png
   :align: right
   :alt: RAID 4

   Source: [Cbu06c]_

**RAID Level 4**, similar to level 2 and level 3, uses striping to spread the
data over multiple disks. But RAID level 4 splits the data block-wise and not
bit- or byte-wise [DK88]_ (ch. 10, pp. 113f). This improves *Input / Output*
(I/O) performance, but can result in a bottleneck, since the parity is stored
on a single device.

.. figure:: /images/cloudraid/raid5.png
   :align: right
   :alt: RAID 5

   Source: [Cbu06d]_

**RAID Level 5** introduces a distribution of the check disk in order to
resolve the bottleneck that exists in RAID level 4. This does not change any
minimum requirements or fault tolerance, but increases the I/O [DK88]_ (ch. 11,
p. 114), [Wik12b]_ and therefore is one of the most used RAID levels nowadays.


2.4. Encryption Standards and Hash Algorithms
---------------------------------------------

In modern computer science cryptography is an important topic while planning
and designing software. It is mostly used when data is transferred over an
insecure channel or is stored at a place that cannot be guaranteed to protect
sensitive or confidential data. Encryption algorithms like the `Advanced
Encryption Standard (AES)`_ and `RC4`_ (*also known as ARC4*) are widely used
and provide strong encryption. The former algorithm is a `block cipher`_ which
means that a certain number of bytes is encrypted simultaneously with the given
key. In contrast, the RC4 algorithm is a `stream cipher`_, meaning that each
byte is encrypted on its own with respect to the previously encrypted bytes and
the secure key.

Both named algorithms use the same key for encryption and decryption and
therefore belong to the group of `symmetric encryption`_ algorithms. The `RSA`_
algorithm (see `U.S. Patent 4,405,829`_) on the other hand belongs to the group
of `asymmetric encryption`_ algorithms or *public-key* algorithms because it
uses a *private key* for decryption and a *public key* for encryption. One
cannot construct one of these keys form the other without knowing an additional
private information.

Even if all stated encryption algorithms ensure that the data that has been
encrypted is secure, they cannot provide data integrity and consistency. If an
encrypted message or file is changed, the decryption will return data that
differs from the original data. To eliminate this issue, so called `hash
algorithm`_ are used.  Given some input data, a hash function will return a
*hash sum* (also referred as *checksum* or only *hash*) to this data. Since
hash functions are one-way functions, one cannot get the original data from the
hash sum. A strong hash function will always return a distinct hash sum for a
specific input and does not (or at least tries to minimize) the likelihood of
hash collisions. Hash collisions occur when a hash function returns the same
hash sum for two different input values. This can easily be shown by the
following formula, where $$x$$ and $$y$$ define the input values and $$H$$
defines the hash function:

.. math::

   \exists x \exists y: H(x)=H(y) \quad x \neq y

Based on these requirements, the NIST and the German "Bundesnetzagentur"
recommend and claim the use of algorithms of the `Secure Hash Algorithm (SHA)-2
family`_ [Eck12]_ with 224, 256, 384 or 512 bits rather than MD5 (128 bits) or
SHA-1 (160 bits)


Sources
=======

.. [Cbu06a] Cburnett. RAID 1. Wikimedia Commons, GNU Free Documentation
   License, December 31, 2006.  http://en.wikipedia.org/wiki/File:RAID_1.svg

.. [Cbu06b] Cburnett. RAID 3. Wikimedia Commons, GNU Free Documentation
   License, December 31, 2006.  http://en.wikipedia.org/wiki/File:RAID_3.svg

.. [Cbu06c] Cburnett. RAID 4. Wikimedia Commons, GNU Free Documentation
   License, December 31, 2006.  http://en.wikipedia.org/wiki/File:RAID_4.svg

.. [Cbu06d] Cburnett. RAID 5. Wikimedia Commons, GNU Free Documentation
   License, December 31, 2006.  http://en.wikipedia.org/wiki/File:RAID_5.svg

.. [DK88] Garth Gibson David A. Patterson and Randy H. Katz. A Case for
   Redundant Arrays of Inexpensive Disks (RAID). Technical report, University
   of California Berkeley, 1988.

.. [Eck12] Claudia Eckert. *IT-Sicherheit – Konzepte – Verfahren – Protokolle*.
   Oldenbourg Verlag München, 7 edition, 2012.

.. [kna09] knakts. RAID 2. Wikimedia Commons, GNU Free Documentation License,
   January 18, 2009.  http://en.wikipedia.org/wiki/File:RAID2_arch.svg

.. [Wik12a] Wikipedia. Hamming code — Wikipedia, The Free Encyclopedia, January
   22, 2012.
   http://en.wikipedia.org/w/index.php?title=Hamming_code&amp;oldid=472688059

.. [Wik12b] Wikipedia. RAID — Wikipedia, The Free Encyclopedia, January 25,
   2012 http://en.wikipedia.org/w/index.php?title=RAID&amp;oldid=473130999


.. _CloudRAID:
   {filename}/Development/2012-10-28__en__cloudraid-1-introduction.rst
.. _Advanced Encryption Standard (AES):
   https://en.wikipedia.org/wiki/Advanced_Encryption_Standard
.. _RC4: https://en.wikipedia.org/wiki/RC4
.. _block cipher: https://en.wikipedia.org/wiki/Block_cipher
.. _stream cipher: https://en.wikipedia.org/wiki/Stream_cipher
.. _symmetric encryption: https://en.wikipedia.org/wiki/Symmetric_encryption
.. _RSA: https://en.wikipedia.org/wiki/RSA_(algorithm)
.. _U.S. Patent 4,405,829: http://www.google.com/patents/US4405829
.. _asymmetric encryption: https://en.wikipedia.org/wiki/Asymmetric_encryption
.. _hash algorithm: https://en.wikipedia.org/wiki/Hash_function
.. _Secure Hash Algorithm (SHA)-2 family: https://en.wikipedia.org/wiki/SHA-2
