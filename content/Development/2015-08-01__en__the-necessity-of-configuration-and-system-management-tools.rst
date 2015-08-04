==================================================================
Update: The Necessity of Configuration and System Management Tools
==================================================================

:tags: Ansible, Chef, Linux, Network, Puppet, Server, Studium
:author: Markus Holtermann
:image: mastersthesis/taxonomy.png
:summary: Over the last months I wrote my Master's Thesis which I'm publishing
   with this post.
:modified: 2015-08-04


Over the last months I wrote my Master's Thesis in Computer Science about
configuration and system management tools at the `Technical University of
Berlin, Germany`_, supervised by `Prof. Dr. Odej Kao`_. I was also supported by
`Flying Circus Internet Operations GmbH`_.

The official title of my thesis is "*Evaluating Methods to Maintain System
Stability and Security When Reversing Changes Made by Configuration and System
Management Tools in UNIX Environments*". In essence it's points out what you as
a system administrator should care about and take into account when using
configuration and system management tools, such as `Ansible`_, `Chef`_, and
`Puppet`_. Using these tools is easy, and takes a lot of your plate when
dealing with larger IT environments, but without considering certain things you
likely break your environment at some point.

Consider the following example:

   A hosting provider offers virtual machines that have an IP address that is
   assigned from a pool of free addresses when the machine is first set up. At
   some point a customer requests the server to be shut down and removed. Once
   the server is removed, its IP address is freed and goes back into the pool.
   However, a customer is able to request a restore of a server from a backup
   within a given time frame after its removal. This works perfectly fine as
   long as the original IP address is not in use. However, configuring the
   network setup will fail if the IP address has been recycled to a different
   machine. [ch. 1, p. 1]

My master's thesis deals with this and many other cases where problems might be
hard to spot.

In order for you to inspect your IT environment and find those problems I came
up with a taxonomy of IT resources that helps you classify all resources
[ch. 5.1, p. 23]:

.. gallery::
   :small: 1

   .. image:: mastersthesis/taxonomy.png
      :alt: classification of IT resources.

For the example given above, the IP addresses of VMs are identifying resources.

After classifying your resources you can follow the rules I derived from the
taxonomy ([ch. 5.2, p. 26]) to narrow down potential conflicts. In the above
case "*Rule 6: Use environment-wide unique identifiers*" is violated. The
hosting provider should keep a record of IP addresses that are still in use
inside backups before actually recycling the addresses.

In chapter 5.3 I provide a variety of use cases that you might encounter in
your IT environment. Chapter 6 takes up those cases and outlines possibilities
of how to solve potential issues.


License
=======

You are allowed to use all resources that are part of this article free of
charge as long as you include my name and a reference to this article in a
place the end-user of your product sees.

You may not copy, distribute, or publish the thesis as a whole unless
explicitly granted.


Download
========

* `Master's Thesis`_
* `Presentation from PyCon Australia 2015`_
* `Video recording from PyCon Australia 2015`_ -- I have to admit I was quite
  nervous


.. _Technical University of Berlin, Germany: http://www.tu-berlin.de
.. _Prof. Dr. Odej Kao: http://www.cit.tu-berlin.de/kao/parameter/en/
.. _Flying Circus Internet Operations GmbH: http://flyingcircus.io

.. _Ansible: http://ansible.com
.. _Chef: https://www.getchef.com
.. _Puppet: https://docs.puppetlabs.com

.. _Master's Thesis: {filename}/files/masterthesis-v1.1.pdf
.. _Presentation from PyCon Australia 2015: https://speakerdeck.com/markush/the-necessity-of-configuration-and-system-management-tools
.. _Video recording from PyCon Australia 2015: https://www.youtube.com/watch?v=1NowxI9WATs
