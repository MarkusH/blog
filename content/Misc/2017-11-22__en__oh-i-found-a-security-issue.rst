============================
Oh, I Found a Security Issue
============================

:tags: Django, PyCon, Security, Python, Talk
:author: Markus Holtermann
:image: pyconca2017/talk-cover.jpg
:summary: An explanation and insight into Django's security process and how you
   can adopt a similar process for your project.


.. image:: /images/pyconca2017/logo.png
   :align: right
   :alt: PyCon CA 2017 logo
   :class: margin-left


Django's Security Process
=========================

When you've used Django and follow one of our email lists you will likely have
seen an announcement of a Django security release much like this one from April
4th this year:

   | Date: Tue, 4 Apr 2017 08:31:25 -0700 (PDT)
   | From: Tim Graham <.....@gmail.com>
   | To: django-announce <django-announce@googlegroups.com>
   | Subject: [django-announce] Django security releases issued: 1.10.7, 1.9.13,
     and 1.8.18

   Today the Django team issued 1.10.7, 1.9.13, and 1.8.18 as part of our
   security process. These releases address two security issues, and we
   encourage all users to upgrade as soon as possible:
   https://www.djangoproject.com/weblog/2017/apr/04/security-releases/

   As a reminder, we ask that potential security issues be reported via private
   email to security@djangoproject.com and not via Django's Trac instance or
   the django-developers list. Please see
   https://www.djangoproject.com/security for further information.

This post is how we, the Django team, get to the state where we are able to
send out such an announcement.

Reporting the issue
-------------------

The process usually starts with somebody reporting a security issue to the
security team. The preferred way to contact us is security@djangoproject.com.

While we can't give a guaranteed response time you can expect an acknowledgment
within 24 hours. Please do not hesitate to send a follow-up email if you do not
get a response within 2-3 days. Depending on the severity of the issue maybe
even earlier.

Apart from that, do not under any circumstances, communicate your findings to
anybody else. The Django security team will take care of the public
announcement later.

Assessing the reported issue
----------------------------

Once the security team got your email, it will assess the issue. You can expect
to be included in the discussion. This allows you to make sure your reported
issue is addressed and that the security team is not missing the point.

Fixing the issue
----------------

The security team will also ask you if you want to supply a patch or if it
should fix the issue itself.

Fixing the issue is often not hard. We are allowed to sacrifice backward
compatibility in case of security issues. On top of that, history has shown
that many patches are only a few lines of code checking just ONE MORE THING

Confirming the fix
------------------

At some point, there is a patch available.

If you wrote the patch the security team will review it.

If somebody from the security team wrote the patch, we kindly ask you to review
the patch to ensure it actually fixes the issue you reported and we don't miss
something.

This is a very important part of the process, even with multiple people
confirming that the patch works, there is still the possibility of missing
something.

Pre-notification
----------------

Once the patch is "ready", to be committed to the release branches, we send out
pre-notification emails to some people and organizations. We will not make this
list public. It mostly consists of distributors and organizations with lots of
personal data.

Aside from the detailed, private notification, we announce the upcoming
security release on the django-announce mailing list with a time frame during
which the release will be made available.

Release & Announcement
----------------------

About a week after the pre-notification there's the security release.

At that point, we will commit the security patches publicly. From that point on
we consider the security issue to be disclosed publicly.

After that, somebody from the release team will cut the corresponding Django
releases.

We will then publish a blog post with some details on the security issue. We
will not publish exploits.

We will publish Common Vulnerability and Exposure numbers — or CVEs — so that
you can check against your downstream vendor's CVE database to see if they
patched the vulnerability.

Furthermore, we will announce the releases to the django-announce and `oss-
security OpenWall mailing list <http://www.openwall.com/lists/oss-security/>`_.

Implementing these steps yourself
=================================

As you can see, there's a lot of process on handling security issues properly.
At least we think we handle them properly.

How can you apply this to your library and make it more secure?

Setup reporting channel
-----------------------

First and foremost, communicate a way people can securely reach out to you to
report a security issue.

A sentence like "If you think you found a security issue please get in touch
via FOO" goes a long way. And PLEASE, including the actual email address there
goes a long way.

Don't let somebody who wants to help you find a communication channel
themselves. Tell them that even a suspicion of a security issue is worth
reporting privately. Even if it turns out to not be an issue.

Monitor reporting channel
-------------------------

I hope it goes without saying that you have to monitor whatever communication
channel you choose.

If you don't have the time to monitor 24/7, which I believe nobody in the room
has, add something like "you should receive an acknowledgment within 7 days" or
whatever is reasonable FOR YOU! This gives the reporter the information that
they may need to wait for a short time.

Just because YOU develop an open source library in your free time doesn't mean
that you need to be around fixing it 24/7. Have a life besides it, please.

Fix the issue
-------------

Find a way to fix the bug. Communicate with the reporter. Once you think you
are good with you have, ask the reporter to confirm your patch. BEFORE you make
it public!

Release & Announce
------------------

Commit and release a new version of your library or program. Inform people
about the release. Communicate where you are going to release such information
at a prominent place so people can subscribe to updates.

My suggestion is to generally report to the oss-security OpenWall list.

Learn from it
-------------

For your own sake, accept the fact that you had a security issue in your
software and don't stress out over it. We're all humans. We all make mistakes!
Learn from it and try to not make this mistake again.

For what it's worth, Django received over 60 CVEs since its release. And
there's a whole bunch of people reviewing code.

OWASP Top 10
============

One thing I want to mention here is the `Open Web Application Security Project
<https://www.owasp.org/>`_ or OWASP. They provide a Top 10 of security issue
classifications that people should care about. It's often considered a
"standard" but there are some loud voices that claim OWASP is not focusing on
the real issues but tries to tackle them from a higher or business level. Have
a look at it and decide for yourself.

Resources
=========

* The PyCon Canada `illustration <https://github.com/pyconca/2017-web/blob/28bb39347b1e044feb930aae6de6be8095973233/pyconca2017/static/toolkit/images/illustrations/illustrations.svg>`_ and `logo <https://github.com/pyconca/2017-web/blob/28bb39347b1e044feb930aae6de6be8095973233/pyconca2017/static/toolkit/images/logo-full.svg>`_ are licensend under the MIT license.

* `Slides <https://speakerdeck.com/markush/oh-i-found-a-security-issue-pycon-ca-2017>`_
