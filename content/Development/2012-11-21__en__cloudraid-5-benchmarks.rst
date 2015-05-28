=========================
[CloudRAID] 5. Benchmarks
=========================

:tags: Apache, C/C++, CloudRAID, Cluster, Eclipse, Encryption, Java, Network,
   Security, Server, Studium
:author: Markus Holtermann
:summary: This post is a continuation of the blog series about the student
   research paper CloudRAID. It provides some timing insights that on our
   prototype and final implementation.


This post is a continuation of the blog series about the student research paper
`CloudRAID`_.


5. Benchmarks
=============

Since the performance is an integral part and a key aspect of the software and
even more one of the most important piece, the following chapter will show some
performance tests and benchmark results.


5.1. Environments
-----------------

In order to make the benchmarks reproducible this chapter will set up some
benchmark environments. They define the hardware as well as the software that is
used for the benchmark tests.


Environment 1
~~~~~~~~~~~~~~

================  ================================================
CPU               Intel® Core™ 2 Duo CPU P8600 @ 2.40 GHz
RAM               4 GiB
Hard disk         Samsung HM320II, 16 MiB Cache
File system       ext4, Block size: 4096 Byte
Disk Encryption   LUKS, cipher: aes-xts-plain, 512 bits
Disk Management   LVM: 2.02.88(2), Library: 1.02.67 Driver: 4.22.0
Operating System  Arch Linux 64bit
================  ================================================


Environment 2
~~~~~~~~~~~~~

================  ================================================
CPU               Intel® Core™ 2 Duo CPU E6600 @ 2.40 GHz
RAM               2 GiB
Hard disk         2x Samsung SpinPoint HD501LJ, 16 MiB Cache
File system       ext4, Block size: 4096 Byte
Disk Encryption   LUKS, cipher: aes-xts-plain, 512 bits
Disk Management   LVM: 2.02.88(2), Library: 1.02.67 Driver: 4.22.0
RAID              Software RAID 1, mdadm 3.2.3
Operating System  Arch Linux 64bit
================  ================================================


Environment 3
~~~~~~~~~~~~~

================  ================================================
CPU               AMD Phenom™ II X6 1090T
RAM               16 GiB
Hard disk         Seagate ST31000524AS, 32 MiB Cache
File system       ext4, Block size: 4096 Byte
Operating System  Arch Linux 64bit
================  ================================================


Environment 4
~~~~~~~~~~~~~

================  ================================================
CPU               Intel® Core™ i7 920 @ 2.67 GHz
RAM               8 GiB
Hard disk         Kingston SH100S3 120G (SSD)
File system       ext4, Block size: 4096 Byte
Operating System  Arch Linux 64bit
================  ================================================


5.2. Comparison of Java, Python, and C
--------------------------------------

One of the key functions of ``CloudRAID`` is to ensure data-security and
data-safety. Therefore ``CloudRAID`` uses the previously explained ARC4
encryption standard andthe RAID level 5 implementation. Since this time critical
operation is used during each ``CloudRAID`` cloud interaction, a run-time
evaluation during the prototype state was interesting.

To make this key component fast, there have been prototypes in Java, Python 2
and C. All three implementations were working with the same algorithm but of
course had a big differences when comparing their run-time.

The following table shows the run-time for the "split" process on a 15 MiB file
using bitwise RAID level 5 without encryption and without hash calculation.


=============  ============
Language       Runtime[sec]
=============  ============
C (Clang)      1.526
C (Clang -O3)  1.123
C (GCC)        1.975
C (GCC -O3)    1.490
Java           155.000
Python2.6      122.300
Python2.7      121.909
PyPy 1.6       20.967
=============  ============

*Table 12: Prototype benchmarks for Java, Python and C*

As one can see from the previous table the run-time for Java is more than 2.5
times as long as for CPython2, more than 7 times longer than for `PyPy`_ and 77
times longer than the native C implementation. The speed of CPython2 and PyPy is
most likely due to the small overhead between the Python interpreter and the
underlying native code, while the Java implementation must leave the Java
Runtime Environment (JRE) for each read and write operation, since they are also
natively implemented and a JNI call is relatively expensive. The speed advantage
of the PyPy based execution is probably based on the just-in-time compiler that
can increase the speed many times.

The results from this prototype gave the crucial factor to implement the RAID
feature in native C – independent of the programming language that would be used
for the remaining part of the software. To get better benchmarking results for C
there was a test with a 1.9 GB file including compiler optimization like the -O3
flag:


=============  ============
Language       Runtime[sec]
=============  ============
C (Clang -O3)  1.123
C (GCC -O3)    1.490
=============  ============

*Table 13: Large file benchmarks for GCC and Clang*

This table clearly shows, that `Clang`_ is doing a better optimization than GCC
does. But nevertheless, using the JNI, the performance of both implementations
changed and GCC was slightly faster than Clang.


5.3. RAID Level 5 Benchmarks
----------------------------

To get the performance of the final implementation, some benchmarks on the
environments, that have been defined in 6.1 on page 54, have been performed.
Therefore files of the sizes 10 kib, 100 kiB, 1 MiB, 20 MiB, 50 MiB, 100 MiB,
250 MiB, 500 MiB and 1 GiB have been created, split and merged. Every complete
process (creation - split - merge) has been run eight times for each size on
each benchmark environment. On the third environment additional tests for the
sizes 2 GiB, 3 GiB, 4 GiB and 5 GiB have been performed to find and show
anomalies for large files.


5.3.1. Split
~~~~~~~~~~~~

Figure 1 shows the average run-time for the split process in the given benchmark
environments. One can see that for the files 100 kiB to 100 MiB the run-time
increases mostly linear to the file size for every environment. For the range
from 10 kiB to 100 kiB the run-time even slightly decreases, relative to the
file size, probably caused by the overhead opening the five files.

.. gallery::
   :small: 1

   .. image:: cloudraid/final_combined_raid5_split.png
      :alt: Runtime for split in various benchmark environments

Figure 1: Runtime for split in various benchmark environments

Using the T400 notebook with above specifications, the run-time increases for
the files larger than 100 MiB. There is no proved explanation for this
phenomenon yet, but it has been appeared during all benchmark runs and is not
just a single outlier distorting the statistics.

Environment 2 keeps a linear run-time up to files of size 500 MiB and is much
slower for files of size 1 GiB.

For the third and forth environments the run-time is linear for all files, even
for the huge files. As one can see in figure 2, the relative run-time increases
for files of size 2 GiB and larger as well.

.. gallery::
   :small: 1

   .. image:: cloudraid/final_env3_raid5_split_zoom.png
      :alt: Split statistics for Tower 2 for huge files

Figure 2: Split statistics for Tower 2 for huge files


5.3.2. Merge
~~~~~~~~~~~~

After a file has been split into its three *device files* and regarding
information has been stored in the *meta data file*, the benchmark tool combines
these *device files* to the original file. Again one can see from figure 3 that
the overall process is mostly linear, except for the range of very small and
very large files. Similar to the split process the hard drive accesses to open
the files is probably the main reason for the decreasing relative run-time
between 10 kiB and 100 kiB.

Similar to the split process, environment 3 shows an increasing relative
run-time for files greater or equal to 2 GiB as one can determine from figure 4
on page 60.

.. gallery::
   :small: 1

   .. image:: cloudraid/final_combined_raid5_merge.png
      :alt: Runtime for merge in various benchmark environments

Figure 3: Runtime for merge in various benchmark environments

Further comparisons of the benchmark environments show differences in the hard
drive caches. While the hard drives in the environments 1 and 2 have a cache
size of 16 MiB the hard disks from environment 3 provide 32 MiB. Comparing the
ages of the used hard disks lead to similar assumptions. While the hard disks
for the first and the second environment are about three, respectively five,
years old, the age of hard disks used in environments 3 and 4 are about one
year.

Besides that, the storage devices for the primary two environments are encrypted
while the other two hard drives are plain. But due to the implementation of the
underlying encryption as part of the *Device Mapper* of the Linux Kernel, the
hardware access is fully transparent and does not do any further hits or
accesses on caches. Thus this has probably no or at least not a high impact on
the hard drive throughput and only affects the *Central Processing Unit* (CPU)
usage.

   [The] Device-mapper uses block devices, such as hard disks and flash-storage
   devices, and represents them as other block devices by adding various
   features. The LVM for example provides flexible partitioning of the block
   device, while dm-crypt adds a transparent symmetric encryption layer to the
   device by using the Linux in-kernel Crypto API. [Hol12]_

Finally, the slight difference in the throughput between the SSD and the third
environment is probably caused by the amount of available memory. While the
former benchmark environment can use up to 8 GB minus the memory used by the OS
itself, the latter has twice that memory available (minus those used by the OS).
Thus the files are being cached in in-memory and are not even written to disk.
But unfortunately there is no way to check whether the data has been written to
disk. Another influence leading to the performance disadvantages of in the forth
environment might be caused by the SATA controller.

.. gallery::
   :small: 1

   .. image:: cloudraid/final_env3_raid5_merge_zoom.png
      :alt: Merge statistics for third environment for huge files

Figure 4: Merge statistics for third environment for huge files


5.3.3. Comparison
~~~~~~~~~~~~~~~~~

While the figures above only show the compared speed for either split or merge
for all four benchmark environments, figure 5 illustrates the relative speed
between the split and merge processes for the benchmark environments. One can
see, that the split process takes much more time than the merge process for the
same file size. This is most likely caused by the number of bytes that are
written to the hard disk. While a call to ``split_file()`` with an input file of
size ``n`` writes ``1.5 × n + 518 bytes`` and reads ``n`` bytes, the regarding
merge done by ``merge_file()`` only writes n bytes but reads ``1.5 × n + 518
bytes``. Since reading is generally much faster than writing this explains the
speed of merge processes.

.. gallery::
   :small: 2

   .. image:: cloudraid/final_env1_raid5_comparison.png
      :alt: Split and merge comparisons for environment 1

   .. image:: cloudraid/final_env2_raid5_comparison.png
      :alt: Split and merge comparisons for environment 2

   .. image:: cloudraid/final_env3_raid5_comparison.png
      :alt: Split and merge comparisons for environment 3

   .. image:: cloudraid/final_env4_raid5_comparison.png
      :alt: Split and merge comparisons for environment 4

Figure 5a - 5d: Split and merge comparisons for environments one to four


Sources
=======

.. [Hol12] Markus Holtermann. Bachelorthesis: Testing Approach for an in-kernel Crypto Functionality – For Linux on System z, June 4, 2012. *(unpublished)* 


.. _CloudRAID:
   {filename}/Development/2012-10-28__en__cloudraid-1-introduction.rst
.. _PyPy: http://pypy.org/
.. _Clang: http://clang.llvm.org/
