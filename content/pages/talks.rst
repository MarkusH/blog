=====
Talks
=====

:slug: talks
:lang: en


2018
====

On The Look-Out For Your Data -- DjangoCon EU
---------------------------------------------

My `DjangoCon Europe 2018 <https://2018.djangocon.eu/>`__ talk.

Do you have data in the database of your Django project? Do you want to find
that needle in the haystack of your data? There are plenty options how you can
achieve that. With various levels of complexity, confidence, and reliability.
I'll give an insight into what the most common are nowadays.

.. speakerdeck:: 1fe1af1a182749789e1b9f4629eab723
   :ratio: 1.77777777777

* `Video recording <https://www.youtube.com/watch?v=GpynTvoxPHI>`__

Oh, I Found a Security Issue -- PyCaribbean
-------------------------------------------

An extended version of my PyCon CA 2017 talk. I'm additionally looking into
what security issues existed in Django and what types of security issues are
out there in the web context.

.. speakerdeck:: 1b4aa86a50b34ac28aaaf67882776ed4
   :ratio: 1.77777777777


2017
====

Oh, I Found a Security Issue -- PyCon CA
----------------------------------------

A 10 minutes talk about Django's Security Process and how one can implement a
similar process for their own projects.

`Blog article <{filename}/Misc/2017-11-22__en__oh-i-found-a-security-issue.rst>`__

.. speakerdeck:: 0803d05dbd78495691cce016b00d3b37
   :ratio: 1.77777777777

* `Video recording <https://www.youtube.com/watch?v=ugcQr6kjA4A>`__

Thoughts About Normal and Abnormal Data -- PyCon UK
---------------------------------------------------

A lot of data lives in relational databases. And there are relations between
records in these databases. Relations that might be normal or abnormal.

`Blog article <{filename}/Misc/2017-10-27__en__thoughts-about-normal-and-abnormal-data.rst>`__

.. speakerdeck:: cc07d328d61549348dd70afdd5e4644a
   :ratio: 1.77777777777

To Index Or Not, That’s Not The Questions -- DjangoCon EU
---------------------------------------------------------

As databases are used to store more and more information every day, these are
also a key component in every Django project. Thus it's important to understand
how they work.

`Blog article <{filename}/Development/2017-04-05__en__to-index-or-not-is-not-the-question.rst>`__

.. speakerdeck:: b34ad0c583854e6cba4764dc1b44e928
   :ratio: 1.77777777777


2016
====

Django and 2 Factor Authentication -- DjangoCon AU
--------------------------------------------------

Most websites these days require some kind of authentication. User name &
password is the most common one. OAuth with Facebook / Github / Google /
Twitter is also common. But sometimes you can't rely on 3rd party services and
user name & password is not enough. In those cases 2 Factor Authentication is a
nice, additional security layer. Use e.g. a phone to ensure a more secure
authentication.

`Blog article <{filename}/Development/2016-09-12__en__2-factor-authentication-in-django.rst>`__

.. speakerdeck:: c3beb76e4f0747a58412d7bc5ce5144f

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

Don't be afraid of writing migrations -- DjangoCon EU
-----------------------------------------------------

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
<http://www.meetup.com/SyDjango/events/225080835/>`__ on Nov 24th, 2015.

See the full Django 1.9 release notes for details and all changes:
https://docs.djangoproject.com/en/dev/releases/1.9/

.. speakerdeck:: 63961d8b68d743688bf5c72a820c3a11


The Necessity of Configuration and System Management Tools -- PyCon AU
----------------------------------------------------------------------

I gave this talk during `PyCon Australia 2015 <http://2015.pycon-au.org/>`__ in
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

* `Video recording <https://www.youtube.com/watch?v=1NowxI9WATs>`__


"Forms are static" -- "No, they aren't" -- DjangoCon EU
-------------------------------------------------------

I gave this talk during `DjangoCon Europe 2015 <http://2015.djangocon.eu/>`__ in
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
<http://www.meetup.com/django-user-group-berlin/events/219547330/>`__.

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
<http://blog.pykonik.org/2014/09/september-meeting-spotkanie-wrzesniowe.html>`__,
the Krakow Python meetup, where I have been invited to by the amazing `Ola
Sendecka <https://twitter.com/asendecka>`__ and `Tomasz Paczkowski
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
