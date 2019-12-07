============================================
All Hands on Deck — Handling Security Issues
============================================

:tags: Incident Handling, LeadDev, Management, Security, Talk, Titanic
:author: Markus Holtermann
:image: all-hands-on-deck/titanic.jpg
:image_credits: `F.G.O. Stuart
    <https://commons.wikimedia.org/wiki/File:RMS_Titanic_3.jpg>`_
:summary: Building a service that exposes millions of user records or is open
    to all kinds of security issues is very quickly done. Let's look into who's
    going to fix it?


Building a service that unintentionally exposes millions of people's user data
or is open to all kinds of other security issues is, unfortunately, very
quickly done.  Reason enough to look at who's going to be involved when
responding to an issue.

A Historic Event
================

On April 10th, 1912, the `R.M.S. Titanic`_ on April 10, 1912 was on its maiden
voyage from the port in Southampton to New York City. At that time, the
*Titanic* was the largest ocean liner in service. There were about 2,224 people
on board.

Four days into the journey, on April 14, at about 9 am ship time, `Captain
Edward Smith`_ received this message from steamship `Caronia`_:

   West-bound steamers report bergs, growlers, and field ice […]

A few hours later, at 1:42 pm, this message from steamship `Baltic`_ made it to
the captain:

   […] Greek steamer `Athenia`_ reports passing icebergs and large quantities
   of field ice today […]

The captain acknowledged both messages. But it wasn't uncommon to see icebergs
and field ice in that area in April. And it was also a general assumption that
ocean liners weren't at risk when hitting an ice berg.

Throughout the day, four more messages were received by the radio operators on
board *Titanic*. At 1:45 pm:

   `Amerika`_ passed two large icebergs […]

At 7:30 pm, a message from the `Californian`_ to the *Antillian*:

   […] Three large bergs 5 miles southward of us. […]

And at 9:40 pm from the *Mesaba* to the *Titanic*:

   Ice report […]. Saw much heavy pack ice and great number large icebergs.
   Also field ice.

These three messages got lost and never made it to the captain.

The sixth and final message which was about to be received by the radio
operators on the *Titanic* at 11 pm from the *Californian*. The *Californian*
was another steam ship which stopped nearby in the middle of the ice. However,
the radio operator on duty at that time was still busy processing a backlog of
messages from the day before. Instead of responding he, shut up the sending
operator with:

   Shut up! Shut up! I'm working Cape Race.

`Cape Race`_ was a radio station on shore, close by.

Ten minutes later, at 11:40 pm, after sighting an iceberg right ahead, the
*Titanic* hit it starboard. Over the next 2 hours and 40 minutes, more and more
water made its way into the hull.

The *Titanic* sank at 2:20 am on April 15, 1912, killing more than 1500 people.

A Present Company
=================

Receiving Security Issue Report
-------------------------------

Not as dramatic is receiving a notice of a possible security issue in a tech
company or department. Usually, nobody's life is on the line. But it may very
well be in case of — for example — hospitals.

Support teams at companies receive several messages a day, be it support
requests, spam, or reports of possible security problems. The people who
receive those messages need to sort through them, assess and triage them, and
process them appropriately.

When their triage of a security issue report is off, the report will not be
classified as a potential security issue. It will instead pile up among the
other bug reports.

But even when the triaging is right, the report needs to reach the team who is
going to deal with it next: the security team, project managers, or product
managers. And they need to act upon it.

Freeing Up Resources
--------------------

Product and project managers will need to budget and plan for engineers to work
on the problem. But the report might also go to a dedicated security team that
will do a more in-depth analysis of the issue and will then communicate with
the product and project managers or fixes it themselves.

Once assessed, if there is an immediate workaround that mitigates the issue in
the short term, all other customers should be informed accordingly. That will
again involve customer support or key account management.

Fixing The Security Issue
-------------------------

When the developers came up with a security fix for the issue, other parties in
the engineering department will need to get involved as well: testing and
quality assurance, technical writers and documentarians, and whoever else in
the company that is involved in any regular change to a product.

Getting A Fix To Customers
--------------------------

Most of the positions mentioned so far are part of the "Engineering
Department." But they are not the only ones involved.

Looking at proprietary products where customers usually need to pay for an
update, the sales department needs to get involved and decide if they are going
to hand out an update for free or if they are going to charge customers for it
despite the vulnerability. The product managers, in conjunction with the sales
department, should also decide if and how much time and money they invest in
backporting a security fix to older versions that may still be used by
customers.

Dealing With The Fallout
------------------------

Imagine one of these leaks that exposed millions of user data records. That's a
PR nightmare. The public relations office will have their hands full. And so
does the marketing department. A product slogan like "*your secure thing-y*" can
quickly become a mockery.

Furthermore, the legal department is going to be involved. The data protection
officer will need to talk to the authorities and inform them about the leak.

In the case of a production company, if the bad press about the issue causes
sales of products to go down, then the purchasing department should probably
think about reducing the number of purchased parts.

What Do We Learn From The Disaster?
===================================

(Re)evaluate Requirements
-------------------------

While standards, requirements, guidelines, and such are great things, they can
also be incomplete, incorrect, or inadequate.

At the time when the *Titanic* sank, British vessels over 10,000 tons needed to
carry 16 lifeboats. The *Titanic* carried 20 and was thus well above the
requirements. But the lifeboats only provided space for 1.178 people, just
about half of the number of people on board the *Titanic*. And only a third of
the total number of people fitting on the *Titanic*. But that should have been
fine. Because lifeboats were meant to get people from one ship onto another
that was in close proximity. Nobody expected an ocean liner to sink within 2
hours.

In today's world, just because sending TANs for online banking via SMS is
common practice, it doesn't mean it's the right thing to do.

Practice Makes Perfect
----------------------

It's also been documented that a lot of crew members had no understanding of
the evacuation procedures. This is not only because of a lack of communication.
But more importantly, because of the lack of practice. Even with 40 years on
the job, captain Smith appeared to be paralyzed when he grasped the enormity of
the problem.

Translating this into the tech world means we need to train ourselves for the
case of a security incident. A documented procedure is excellent. But without
practice, people will act in all kinds of ways, possibly irrationally.

Communication Is Crucial
------------------------

And lastly, and most importantly, communication is crucial.

It's been documented that captain Smith ordered his first and second officers
to "*put the women and children in [the lifeboats] and lower away*." But the
officers interpreted it differently. One put men next to the woman and children
when no women or children were around. The other one lowered lifeboats with
empty seats.

As you can see, there can be numerous people involved when it comes to handling
a security issue. And a lot of people mean a lot of communication. Clear
communication is important in any company. But it's crucial when it comes to
handling security issues.

Resources
=========

* The `Oceanus magazine, volume 28, number 4, winter 1985/86`_. This edition
  gives an in-depth insight into what happened around the *Titanic* tragedy.

* And `Agile Application Security`_ by Laura Bell and others. It's about how
  agile teams can deal and handle security issues. And they can do that despite
  their ability to iterate quickly.

* `Slides <https://speakerdeck.com/markush/all-hands-on-deck-handling-security-issues-leaddevberlin-2019>`_


.. _R.M.S. Titanic: https://en.wikipedia.org/wiki/RMS_Titanic
.. _Captain Edward Smith: https://en.wikipedia.org/wiki/Edward_Smith_(sea_captain)
.. _Caronia: https://en.wikipedia.org/wiki/RMS_Caronia_(1904)
.. _Baltic: https://en.wikipedia.org/wiki/RMS_Baltic_(1903)
.. _Athenia: https://en.wikipedia.org/wiki/SS_Athenia_(1903)
.. _Amerika: https://en.wikipedia.org/wiki/USS_America_(ID-3006)
.. _Californian: https://en.wikipedia.org/wiki/SS_Californian
.. _Cape Race: https://en.wikipedia.org/wiki/Cape_Race
.. _Oceanus magazine, volume 28, number 4, winter 1985/86: https://archive.org/stream/oceanusv2804wood
.. _Agile Application Security: https://www.oreilly.com/library/view/agile-application-security/9781491938836/
