=====================================
Showing BVG Departures In Your Office
=====================================

:tags: Git, Linux, Python, Studium
:author: Markus Holtermann


Yesterday evening I gave a lightning talk at the `Python User Group Berlin`_
called "*Showing BVG Departures In Your Office*". You can download the slides
`here`_.

The whole idea to the project came up when our student organization
(`Freitagsrunde`_) had to relocate to a new building at the end of 2012.

Since our new student organization meeting room is quite near to the next bus
stop (bee-line), but the actual distance is way longer and we have to cross
several doors, waiting in the room and heading to the bus stop when the bus
arrives is not going to work.

As computer scientists we had to come up with a solution to somehow grab the
departures of the bus stop and show them in the room.

.. gallery::
   :small: 2

   .. image:: BVG-Grabber-LightningTalk-installation1.jpg
      :alt: bvg-grabber in use

   .. image:: BVG-Grabber-LightningTalk-installation2.jpg
      :alt: bvg-grabber in use

At first the information retrieval was hard-coded and it was only possible to
get the departures for a single bus stop. After a short time we got the feature
request to also display the departures of nearby subways and other public
transport. We ended up rewriting the entire application and created a library
we then called `bvg-grabber`_.

The quite simple API allows us to use both information provided by the `BVG`_:
the actual departures which, in that days, only returned departures about
busses, and the scheduled departures as they are written on the time tables:

A class inheriting from ``QueryApi`` must implement a ``call()`` function that
returns a ``Response`` object.

.. code-block:: python

    class QueryApi(object):
        """Performs the requests to the data source"""

        def call(self):
            """Needs to return a Response"""
            raise NotImplementedError("The inheriting class needs to "
                                      "implement the call() method!")

A ``Response`` object must contain a ``state`` (True/False for success/failed
request) and, for a successful request, the departing station and a list of
Departures, or, for a failed request, the error that occurred.

.. code-block:: python

    class Response(object):
        """Returned by a QueryApi, contains list of Departures"""

        def __init__(self, state, station=None, departures=None,
                     error=None):
            self._state = state
            self._departures = [(station, departures)]
            self._error = error

        @property
        def departures(self):
            return self._departures

Finally, a ``Departure`` defines *when* a certain *line* leaves at a certain
*start* station and at which station the ride will *end*.

.. code-block:: python

    @total_ordering
    class Departure(object):
        """Start and end station, next departure time"""

        def __init__(self, start, end, when, line, since=None,
                     no_add_day=False):
            # Some magic happens here

As we are using the actual and the scheduled information from the BVG as you
can see above, here are 2 short examples how to use them:

.. code-block:: python

    In [1]: from bvggrabber.api.actualdeparture import ActualDepartureQueryApi

    In [2]: resp = ActualDepartureQueryApi("Ernst-Reuter-Platz").call()

    In [3]: resp.departures
    Out[3]: 
    [('Ernst-Reuter-Platz',
      [Start: Ernst-Reuter-Platz, End: S+U Zoologischer Garten, when: 13:56, now: 13:54, line: Bus 245,
       Start: Ernst-Reuter-Platz, End: S+U Zoologischer Garten, when: 14:01, now: 13:54, line: Bus X9,
       Start: Ernst-Reuter-Platz, End: S+U Zoologischer Garten, when: 14:05, now: 13:54, line: Bus M45,
       Start: Ernst-Reuter-Platz, End: Johannesstift, when: 13:54, now: 13:54, line: Bus M45,
       Start: Ernst-Reuter-Platz, End: Flughafen Tegel, when: 13:55, now: 13:54, line: Bus X9,
       Start: Ernst-Reuter-Platz, End: Johannesstift, when: 14:01, now: 13:54, line: Bus M45])]

    In [4]: from bvggrabber.api.scheduleddeparture import ScheduledDepartureQueryApi

    In [5]: resp = ScheduledDepartureQueryApi("Ernst-Reuter-Platz").call()

    In [6]: resp.departures
    Out[6]: 
    [('Ernst-Reuter-Platz',
      [Start: Ernst-Reuter-Platz, End: Johannesstift (Berlin), when: 13:54, now: 13:54, line: Bus  M45,
       Start: Ernst-Reuter-Platz, End: Hertzallee (Berlin), when: 13:56, now: 13:54, line: Bus  245,
       Start: Ernst-Reuter-Platz, End: S+U Pankow (Berlin), when: 13:56, now: 13:54, line: U2,
       Start: Ernst-Reuter-Platz, End: Hertzallee (Berlin), when: 13:57, now: 13:54, line: Bus  M45,
       Start: Ernst-Reuter-Platz, End: U Theodor-Heuss-Platz (Berlin), when: 13:58, now: 13:54, line: U2])]

I'm looking forward to your ideas and feature requests.

Markus

Links
=====

* `Slides`_
* `bvg-grabber on github.com`_


.. _Python User Group Berlin: http://www.meetup.com/Python-Users-Berlin-PUB/events/105128552/
.. _Slides:
.. _here: https://speakerdeck.com/markush/showing-bvg-departures-in-your-office
.. _Freitagsrunde: http://freitagsrunde.org
.. _bvg-grabber on github.com:
.. _bvg-grabber: https://github.com/MarkusH/bvg-grabber
.. _BVG: http://bvg.de
