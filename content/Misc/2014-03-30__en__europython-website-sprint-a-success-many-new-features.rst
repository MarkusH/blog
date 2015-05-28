===================================================================
EuroPython website sprint a success - many new features implemented
===================================================================

:tags: Community, Django, EuroPython, Sprint
:author: Markus Holtermann
:summary: Last weekend the EuroPython web team met in Berlin in order to bring
   the EuroPython 2014 website software forward.


Last weekend the web team `met`_ in Berlin (and was supported by one member
remotely) in the rooms of Veit Schiele Communications GmbH in order to bring the
`EuroPython 2014 website software`_ forward. The team under the leadership of
Markus Holtermann implemented the following new features:

* A short while ago we made some heavy changes to the main menu. Unfortunately
  the user experience wasn’t the way we expected it to be. Thus we got some
  comments on the EuroPython `mailing list`_. It took us some time to decide how
  to change the way the menu should work. Eventually, a click on a main menu
  item only toggles the menu as of now (`GitHub issue #103`_)
* We want to generate the badges (and other stuff for the conference) directly
  from the user data you provide on the website. This presented us with some
  kind of challenge as you will see in the next bullet point, too. We decided
  that the singe point of truth for the user data is the user profile. We
  therefore added a field where you can enter your interests. (`GitHub issue
  #105`_)
* As said before, the single point of truth for the user data is and will be the
  user profile. Unfortunately, during the purchase process of a ticket, we only
  have information about the buyer, not any of the intended ticket users.
  Although we didn’t change this part in the update (and we won’t change it in
  the future), you are now able to assign a ticket to another user. This is
  incredible useful for those buyers ordering multiple tickets, eg. for their
  colleagues or friends. To assign the ticket to somebody else, ask him/her for
  the user name and assign the ticket to him/her from `your purchase view`_. If
  the intended user doesn’t have a account yet, ask him to create one. All
  tickets that are *not* assigned to somebody will use the first and last name
  given during purchase. (`GitHub issue #101`_)
* Since many attendees are not from Germany, we looked for a way to hand out SIM
  cards. Due to legal restrictions this is not *that* simple in Germany (you
  normally need to present a photo ID). Fortunately we found a reseller where we
  become some kind of reseller ourselves (it's a bit more complicated than that
  ;) ). Hence we will offer SIM cards within the next days that you can buy
  beforehand and you can pick up during check-in (more details soon). (`GitHub
  issue #100`_)
* When you modify your profile and try to upload a new avatar, but there are
  errors in some other fields, the avatar gets lost. We solve this by adding
  front-end validation to this and many other forms. (`GitHub issue #47`_)
* If you are looking for a job (in your real live, not the one on the internet
  :D), or if you think about getting a new job for whatever reason, you can now
  opt-in (and later opt-out) of job offers by our sponsors. We will **not** hand
  over any of your data to the sponsors. The sponsors have to give us their
  offer and we will send it only to those users interested in job offers.
  (`GitHub issue #78`_)
* The list of your purchases now shows canceled purchases too. (`GitHub issue
  #102`_)

Apart from those changes interesting to you as an attendee, loads of other
changes made it into production. If you are interested, have a look at our
repository on GitHub: https://github.com/EuroPython/djep

All new features went into production today with an update of the portal
software.

Thanks a lot to the web team and all other sprinters for their dedicated work on
the EuroPython 2014 web software.


Source: `blog.europython.eu`_, Mar 30, 2014, 20:30pm CEST


.. _met: http://www.meetup.com/Python-Users-Berlin-PUB/events/168403892/
.. _EuroPython 2014 website software: https://github.com/EuroPython/djep
.. _mailing list: https://mail.python.org/pipermail/europython/2014-February/008323.html
.. _GitHub issue #103: https://github.com/EuroPython/djep/issues/103
.. _GitHub issue #105: https://github.com/EuroPython/djep/issues/105
.. _your purchase view: https://ep2014.europython.eu/en/tickets/mine/
.. _GitHub issue #101: https://github.com/EuroPython/djep/issues/101
.. _GitHub issue #100: https://github.com/EuroPython/djep/issues/100
.. _GitHub issue #47: https://github.com/EuroPython/djep/issues/47
.. _GitHub issue #78: https://github.com/EuroPython/djep/issues/78
.. _GitHub issue #102: https://github.com/EuroPython/djep/issues/102
.. _blog.europython.eu: http://blog.europython.eu/post/81187947812
