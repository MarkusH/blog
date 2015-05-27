===========================
[CloudRAID] 1. Introduction
===========================

:tags: Apache, CloudRAID, Cluster, Eclipse, Encryption Java, Network, Security,
   Server, Studium
:author: Markus Holtermann


During last year a fellow student of mine, `Florian Bausch`_, and I wrote a
student research paper about how to provide availability, redundancy and
security of data in the overall existing and "well known" *cloud*. In this
context we additionally developed a prototype that we call ``CloudRAID``. The
software is licensed under the terms of the `Apache 2 License`_ and published
on `GitHub`_.

During the next weeks we are going to publish our paper as a series of posts on
our blogs. This post makes the start of this series and is going to introduce
the general idea behind the topic. The next part of the student research paper
will be published by Florian on his blog and covers some basic topics like the
"OSGi Framework" and "Cloud". I will announce the publication here. So, stay
tuned.


0. Table of Contents
====================

#. `Introduction`_
#. `Basics`_

   #. `The OSGi Framework`_
   #. `Cloud`_
   #. `Background on RAID Technology`_
   #. `Encryption Standards and Hash Algorithms`_

#. `Concept`_

   #. `Requirements`_
   #. `General Architecture`_
   #. Server Architecture (`Part 1`_, `Part 2`_)
   #. `Client Architecture`_

#. `Implementation`_

   #. `JNI API`_
   #. `RESTful API Endpoint Specifications`_
   #. `Compression on RESTful API`_
   #. `Client Software`_

#. `Benchmarks`_

   #. `Environments`_
   #. `Comparison of Java, Python and C`_
   #. `RAID Level 5 Benchmarks`_

#. `Conclusion and Outlook`_


1. Introduction
===============

In a world that gets more and more mobile, everybody wants to have access to
his data all the time. The knowledge that one needs an important document and
cannot access it because it is on the computer at home, makes one use cloud
storage providers. But relying on the availability of those cloud providers is
not a good idea as is shown later on. To work around the availability concerns,
one might use multiple cloud storage provides and ends up with a lot of work to
synchronize the storages.

.. figure:: /images/cloudraid/structural-idea.png
   :align: right
   :alt: Structural layout idea
   :class: margin-left

   *Figure 1: Structural layout idea*

This student research paper by `Florian Bausch`_ and `Markus Holtermann`_ finds
a solution to this problem. It describes and evaluates the idea, concept and
example implementation of a cloud-based *Redundant Array of Independent Disks*
(RAID) storage system. The research goal is a file storage system, that
combines multiple cloud services as back-end storages and represents them as a
single front-end storage to the user. Providing several features like
encryption, authorization, availability and redundancy, the cloud-based RAID
can be used as a reliable backup storage even for sensitive personal
information.

After introducing the basic knowledge and requirements of the research project,
mainly *Open Services Gateway initiative framework* (OSGi), Cloud Computing,
RAID and cryptography, there will be the concept of how to implement the
features and building a cloud-based RAID. This elaboration is then followed by
detailed implementation notes. The program will be titled ``CloudRAID`` to
combine the terms "Cloud" and "RAID" as they are the foundational backgrounds
for the project. To show the validity of ``CloudRAID``, there are some
benchmarks that point out the advantages and disadvantages as well as the
problems that might occur.

One must keep in mind that ``CloudRAID`` will not be a RAID system in the
strict sense, but uses the ideas and techniques of those systems.


.. _Florian Bausch: http://blog.fbausch.de
.. _Apache 2 License: http://www.apache.org/licenses/LICENSE-2.0.html
.. _GitHub: https://github.com/MarkusH/CloudRAID
.. _Markus Holtermann: https://markusholtermann.eu

.. _Introduction:
   {filename}/Development/2012-10-28__en__cloudraid-1-introduction.rst

.. _Basics: http://blog.fbausch.de/cloudraid-2-basics/
.. _The OSGi Framework: http://blog.fbausch.de/cloudraid-2-basics/
.. _Cloud: http://blog.fbausch.de/cloudraid-2-basics/
.. _Background on RAID Technology:
   {filename}/Development/2012-11-03__en__cloudraid-2-basics-continuation.rst#background-on-raid-technology
.. _Encryption Standards and Hash Algorithms:
   {filename}/Development/2012-11-03__en__cloudraid-2-basics-continuation.rst#encryption-standards-and-hash-algorithms

.. _Concept: http://blog.fbausch.de/cloudraid-3-concept/
.. _Requirements: http://blog.fbausch.de/cloudraid-3-concept/
.. _General Architecture: http://blog.fbausch.de/cloudraid-3-concept/
.. _Part 1: http://blog.fbausch.de/cloudraid-3-concept/
.. _Part 2: http://blog.fbausch.de/cloudraid-3-concept-continuation/
.. _Client Architecture:
   http://blog.fbausch.de/cloudraid-3-concept-continuation/

.. _Implementation:
   {filename}/Development/2012-11-13__en__cloudraid-4-implementation.rst
.. _JNI API:
   {filename}/Development/2012-11-13__en__cloudraid-4-implementation.rst#jni-api
.. _RESTful API Endpoint Specifications:
   {filename}/Development/2012-11-15__en__cloudraid-4-implementation-continuation.rst#restful-api-endpoint-specifications
.. _Compression on RESTful API:
   http://blog.fbausch.de/cloudraid-4-implementation-continuation/
.. _Client Software:
   http://blog.fbausch.de/cloudraid-4-implementation-continuation/

.. _Benchmarks:
   {filename}/Development/2012-11-21__en__cloudraid-5-benchmarks.rst
.. _Environments:
   {filename}/Development/2012-11-21__en__cloudraid-5-benchmarks.rst#environments
.. _Comparison of Java, Python and C:
   {filename}/Development/2012-11-21__en__cloudraid-5-benchmarks.rst#comparison-of-java-python-and-c
.. _RAID Level 5 Benchmarks:
   {filename}/Development/2012-11-21__en__cloudraid-5-benchmarks.rst#raid-level-5-benchmarks

.. _Conclusion and Outlook:
   http://blog.fbausch.de/cloudraid-6-conclusion-and-outlook/
