====================
A lot has happended!
====================

:tags: Personal, Django, Studium
:author: Markus Holtermann
:image: change.jpg
:image_credits: Licensed under the terms of the `Creative Commons Attribution
   2.0 Generic (CC BY 2.0) <https://creativecommons.org/licenses/by/2.0/>`_ by
   `Kevin Dooley <https://www.flickr.com/photos/pagedooley/8317353637>`_
:summary: It has been 5 months that I wrote something on my blog. I still
   remember the time writing the article. On my way to Django: Under The Hood
   2014. And shortly after that my time to write something here vanished.
   For various reasons.


It has been 5 months that I wrote something on my blog. I still remember the
time writing the article. On my way to `Django: Under The Hood 2014`_, my
favorite conference in 2014 as an attendee. And shortly after that my time to
write something here vanished. For various reasons.


December 2014
=============

While getting `9 commits`_ into Django's code base throughout December, we (the
server team at `ubuntuusers.de`_) finally `upgraded our infrastructure`_ to new
hardware. A few days before the holidays I decided to finally fill out the form
and enrolled for my master thesis.


January 2015
============

2015 began quietly. Not many things happened. Until January 9th! `Carl Meyer`_
queried me on IRC:

    We'd like to invite you to be part of the Django core team, if you're
    interested.

I was super happy and excited (and still am). And according to the `official
announcement`_ I was *the most active non-core-team code contributor* in
2014. Interesting, I wasn't aware of that and haven't even though about it :)

Later that month I got the confirmation for the topic of my Master Thesis. I
won't tell it here until I finished and got my grade for it. It's about
configuration and system management tools. But I'm working on my thesis ever
since which is, together with my work as Django core developer, the reason why
I don't really have time to do anything else.

On 25th I was a coach at `DjangoGirls Berlin`_. That's the second time I've
been coaching (first time was after Django: Under The Hood) and the second time
DjangoGirls came to Berlin (first time was at `EuroPython 2014`_).


February 2015
=============

There are not many things worth mentioning for February. I gave a lightning
talk at the `Python Users Berlin meetup`_ about how to integrate `Sphinx`_ and
`Elasticsearch`_.

A week later I gave a talk at the `Django User Group Berlin meetup`_ about
*Combining Django & Elasticsearch* (`Slides`_).


March 2015
==========

Compared to February, March was really busy in terms of travelling. I went to
the `Django Sprint in Amsterdam`_. Thanks again to the organizers. It was a
pleasure to be back in Amsterdam.

One week later a couple of friends and I finally went on a skiing vacation
again. We had amazing weather. The view from the top of the mountains was
breathtaking. `I took a few photos`_! The photos are licensed under a `Creative
Commons Attribution-NonCommercial-ShareAlike 4.0 International License`_
(CC-BY-NC-SA).


April 2015
==========

On April 1st we released `Django 1.8`_ as our next LTS (Long Term Support)
version with a hole bunch of new features and improvements:

* Native support for multiple template engines.

* Support for complex SQL expressions via the ORM.

* A formalized API for ``Model._meta``.

* New PostgreSQL specific functionality in ``contrib.postgres``.

The features and changes I'm particularly happy about are the serialization of
model managers in migrations (`#23822`_) which I have worked on for quite a
while and of course the performance improvements in migrations. It was some
hard work but thanks to the amazing work `Claude Paroz`_ did on `#23745`_ and
`Marten Kenbeek`_ did on `#24366`_ the migrations in 1.8 are noticeable faster.
Of course thanks to all contributors who made the release the way it is :)



.. _Django\: Under The Hood 2014:
    http://www.djangounderthehood.com/

.. _9 commits:
    https://github.com/django/django/graphs/contributors?from=2014-12-01&to=2015-01-01&type=c

.. _ubuntuusers.de:
    http://ubuntuusers.de
.. _upgraded our infrastructure:
    https://ubuntuusers.statuspage.io/incidents/mb0wt1jnhg3s

.. _Carl Meyer:
    https://github.com/carljm
.. _official announcement:
    https://www.djangoproject.com/weblog/2015/jan/11/new-core-team-members/

.. _DjangoGirls Berlin:
    http://djangogirls.org/berlin/
.. _EuroPython 2014:
    https://ep2014.europython.eu/en/conference/satellite-events/django-girls-workshop/

.. _Python Users Berlin meetup:
    http://www.meetup.com/Python-Users-Berlin-PUB/events/219427342/
.. _Sphinx:
    http://sphinx-doc.org/
.. _Elasticsearch:
    https://www.elastic.co/products/elasticsearch

.. _Django User Group Berlin meetup:
    http://www.meetup.com/django-user-group-berlin/events/219547330/
.. _Slides:
    https://speakerdeck.com/markush/combining-django-and-elasticsearch

.. _Django Sprint in Amsterdam:
    http://www.meetup.com/dutch-django-assocation/events/220368460/

.. _I took a few photos:
    https://plus.google.com/+MarkusHoltermann/posts/h2CiMHpdtRC
.. _Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License:
    http://creativecommons.org/licenses/by-nc-sa/4.0/

.. _Django 1.8:
    https://www.djangoproject.com/weblog/2015/apr/01/release-18-final/
.. _#23822:
    https://code.djangoproject.com/ticket/23822
.. _Claude Paroz:
    https://github.com/claudep
.. _#23745:
    https://code.djangoproject.com/ticket/23745
.. _Marten Kenbeek:
    https://github.com/knbk
.. _#24366:
    https://code.djangoproject.com/ticket/24366
