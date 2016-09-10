=====
Talks
=====

:slug: talks
:lang: en


2016
====

SSL All The Things -- PyCon AU / PyCon NZ
-----------------------------------------

A revised version of my talk from DjangoCon US targeted at a more generic
Python audience. Instead of having Django specific code and slides I show how
to use Python's built-in ``ssl`` module.

`Blog article <{filename}/Development/2016-09-10__en__ssl-all-the-things-in-python.rst>`__

.. speakerdeck:: 857314c6dbe64db1be8fb5bcafb17a7f

.. speakerdeck:: a1a78b393ebc4a569d83f57346aa025e

SSL All The Things -- DjangoCon US
----------------------------------

Over the last few years SSL/TLS encryption of not only websites but many other
services as well has risen tremendously. The Let’s Encrypt organization and
certificate authority (CA) makes that pretty easy. Since September 2015 almost
1.8 million certificates have been issued. And you can use it, too. For free!

In this talk I'll demonstrate how to integrate SSL/TLS and point out some
common pitfalls. I’ll briefly layout the Let's Encrypt ACME protocol and
explain what you need to set up in Django to make SSL/TLS the default and only
way to access your site.

`Blog article <{filename}/Development/2016-07-19__en__ssl-all-the-things.rst>`__

.. speakerdeck:: 4b3c84c76a764060b434e3782245665b

Don't be afraid of writing migrations
-------------------------------------

With Django 1.7 the built-in migrations framework was introduced. With the
release of version 1.9, the migrations framework is much more robust, faster
and can handle many more edge cases.

While the makemigrations management command became smarter in the last two
releases in terms of detecting what has changed and what migrations to
generate, there are still a couple of things Django cannot do automatically.

I will point out some of the common cases where you should get your hands
dirty, and show you how writing migrations is easier than you think. Migrations
are just Python code, and are as much a part of your apps as your models,
forms, and views. After all, they were always meant to be human-writable.

`Blog article <{filename}/Development/2016-04-04__en__dont-be-afraid-of-writing-migrations.rst>`__

.. speakerdeck:: 4a655fe76c8c4526992c313885e66920
   :ratio: 1.77777777777


2015
====

What's new in Django 1.9
------------------------

I gave this presentation at the `Sydney Django meetup
<http://www.meetup.com/SyDjango/events/225080835/>`_ on Nov 24th, 2015.

See the full Django 1.9 release notes for details and all changes:
https://docs.djangoproject.com/en/dev/releases/1.9/

.. speakerdeck:: 63961d8b68d743688bf5c72a820c3a11


The Necessity of Configuration and System Management Tools
----------------------------------------------------------

I gave this talk during `PyCon Australia 2015 <http://2015.pycon-au.org/>`_ in
Brisbane.

In practically every moment of our life we rely on the possibly largest
communication medium humanity ever had. The Internet. Being able to at least
partially understand how this *thing* works, we know that it takes a lot of
work to keep it running smoothly.

To do that IT administrators use configuration and system management tools to
deploy changes to thousands of servers and keep them in sync. But how can one
roll back a change done in the past that turned out to introduce a bug?

This talk I will introduce you to configuration management and explain the
problems that arise over time and make changing something back complicated or
even impossible.

.. speakerdeck:: 3c742309f97a46f682f4679746221545

* `Video recording <https://www.youtube.com/watch?v=1NowxI9WATs>`_


"Forms are static" -- "No, they aren't"
---------------------------------------

I gave this talk during `DjangoCon Europe 2015 <http://2015.djangocon.eu/>`_ in
Cardiff, Wales.

.. speakerdeck:: 6d6ba705ba7849fc983204b1cfb7b175


Introduction to Django
----------------------

This is an introductory talk I gave to a course of Bachelor students at
Technical Univeristy of Berlin as guide about how to build a *basic* web
application.

.. speakerdeck:: 07c3c95bac5b4e9ca6c126eea96568dc


Combining Django & Elasticsearch
--------------------------------

Some thoughts and ideas on how to intregrate Elasticsearch into your Django
project. I gave that talk at a `Django Users Berlin meetup
<http://www.meetup.com/django-user-group-berlin/events/219547330/>`_.

.. speakerdeck:: 449ec3df8af14d82827040327391fed2
   :ratio: 1.77777777777


2014
====

You Should(n't) Normalize Your Database
---------------------------------------

This talk you make you start thinking about when database normalization -- as
you might have learned during computer science lessens at school or university
-- is a good approach and when you should actually avoid it. I gave this talk
at various occasions, one being the `pykonik
<http://blog.pykonik.org/2014/09/september-meeting-spotkanie-wrzesniowe.html>`_,
the Krakow Python meetup, where I have been invited to by the amazing `Ola
Sendecka <https://twitter.com/asendecka>`_ and `Tomasz Paczkowski
<https://twitter.com/oinopion>`_.

.. speakerdeck:: 0ae3593038fb013275d462001b84dca3


Introduction to Django-CMS
--------------------------

An introduction to a very early stage of Django-CMS 3.

.. speakerdeck:: 4434fbc034660132fdaa460f5c31d588


2013
====

Showing BVG Departures In Your Office
-------------------------------------

.. speakerdeck:: e945a6d0309a0132ab4a06da7886ac56
