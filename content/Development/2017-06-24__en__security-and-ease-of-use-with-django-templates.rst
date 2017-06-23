==============================================
Security and Ease-of-Use With Django Templates
==============================================

:tags: Django, Security
:author: Markus Holtermann
:image: django-logo.png
:summary: Usability is key in modern web applications. But we live in a
   dangerous world where websites get hacked. Thoughts on pros & cons.


.. role:: strike


I engaged in a bit of a Twitter discussion that started when `Samuel Spencer
<https://twitter.com/legostormtroopr>`_ showed `a Django package to modify page
templates <https://twitter.com/legostormtroopr/status/877810010784387072>`_
through the Django admin.

This blog post *is not* intended to blame him for developing the package. This
blog post *is not* intended to discourage anybody from using that package. This
blog post *is* intended to educate about possibly risks that arise from using
that package or, in general, blindly trust and run user supplied content which
is something this package does *to some degree*.

TL;DR: We live in a dangerous world. Security is hard. Don't trust anything.

Ok. Let's me a bit more serious and specific. Let's weigh the pros and cons.
Let's see what's actually at stake.

The Deployment
==============

Deploying Django applications is more complicated than your typical WordPress
site. At least when you get started with Django. There are dozens of articles,
conference talks, and mailing list discussions on that topic. Google it if you
want specifics. In essence, deploying a Django project is not simply done by
copying some files to a document root on a web server as it is common with PHP.
You'll probably use an application server like gunicorn and uwsgi. Or you
figured out how to use mod_wsgi in the Apache HTTP server which then works
similarly to PHP yet completely different. But when you managed to get all
changes to your server, you still need to tell the application server to reload
and restart your application. And this is *a good thing* ™. You'll see why that
is later.

When You Screw Up
=================

Let's assume you have this magic way to modify the HTML template files for your
Django project in the browser. That's great, as you can now make some quick fix
online without the need to commit code and trigger your deployment pipeline. So
it's perfectly suitable to perform those changes from your smartphone given a
`responsive Django admin <https://code.djangoproject.com/ticket/26818>`_.
Wrong!

Guess what happens when you modify your ``base.html`` file and have a syntax
error in there. The potentially harmless case is a broken ``<a>`` tag, a messed
up a list definition or whatnot. Or you accidentally remove the keywords from
the ``<head>`` section so your SEO ranking goes downhill. None of these things
actually are a real issue for the matter of this post. Your site will still be
available. Users can still access your page and read its content. Modern
browsers will cope with all kinds of broken HTML structures. So, all good,
right? Wrong!

What happens if you accidentally removed some escaping from some Django
template language variables, such as ``escapejs`` inside a JavaScript block?
Well, the good thing, your site will still "work" and is not going to throw a
`HTTP 500 Internal Server Error <https://httpstatuses.com/500>`_. Probably, at
least. Lucky you. But maybe not. This is one of those subtle issues you will
only know about once somebody exploited an issue with unescaped JavaScript.
Which is now possible due to to missing ``escapejs``, remember?

I think I'd prefer to completely screw up my Django template syntax. At least
the issue will be brutal when the entire page won't load. You should notice
that, right? Depends! Only if you have proper monitoring or error reporting.

But that's not all. That's just the start. Depending on which template file you
just broke, you might as as well broke your Django admin template.
Congratulations, you're now forced to figure out a way to revert that. Likely
without *any* form of web UI. Oh, and of course, you're on your phone in the
middle of nowhere with crappy internet such that an SSH connection cracks down
every 5 minutes. Sucks for you, I guess.

Something Else Is Insecure
==========================

Given the example from the introduction -- a view in the Django admin that lets
you modify the template files -- what happens if there's a privilege escalation
in the Django admin that lets arbitrary users modify those templates. We'll,
that unfortunate! (On that note, if you encounter or *think* you encountered a
security issue in Django, please reach out to security@djangoproject.com and
**do not** report the issue through the issue tracker).

You're pretty much out of luck here until you there's a patched Django release
you can use. But in the meantime, :strike:`users` (alright, let's start calling
*those* users attackers now) attackers will be able to exploit the privilege
escalation and have all kinds of fun. Starting with one of those "you've been
hacked" memes, over a simple "breaking the page" by messing with the Django
template language syntax over sneaking in some evil JavaScript that performs
`XSS attacks <https://en.wikipedia.org/wiki/Cross-site_scripting>`_ against you
and your users. Of course nobody is going to notice the latter. Thus you're
leaking more and more data to the attackers.

Now, all previous issues assume an attacker only touches the HTML template
files. While that is bad enough, slightly more subtle changes could be
introduced by exploiting an issue in the online editor that would allow an
attacker to modify arbitrary files. Like, the JavaScript files shipped to a
user. But again, this would manifest itself instantly. The "fun" part begins
when an attack would be able to view (and potentially write) Python files
belonging to your project. I mean, what could possibly go wrong when `Django's
SECRET_KEY or database credentials are leaked
<https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-SECRET_KEY>`_,
right? Apart from being able to connect to your database they could also change
the Python code and essentially do whatever they want. Well, almost. Because
most (all?) Python web application servers need to be told to reload the web
application and thus actually see those changes. In order to do that an
attacker would thus need to restart the application server. And that's not
*that* easily possible unless you can already run arbitrary code. On the other
hand with PHP, changes are reflected instantly (at least as far as I remember.
I've not done any PHP development for a while).

When To Use Such Features
=========================

Well, if you want to err on the side of caution: never.

If you do use those tools, make sure you've `come up
<https://www.owasp.org/index.php/Application_Threat_Modeling>`_ with a `threat
model <https://en.wikipedia.org/wiki/Threat_model>`_ and risk model. If they
say the usability and user experience outweighs the risk and threat, sure, go
ahead. If they say it's too risky, well, don't use such things.

On a higher level you can probably reduce the decision making to this: Is your
site on the internet, don't use such features. Is it company internal, e.g.
behind a VPN and only a limited set of users have access to it, you're probably
fine. A company usually has bigger problems when there's a rough admin that
starts XSSing its colleagues. Is it your own tool you use for yourself only and
nobody else has access to it, sure, go ahead, use such tools if they make your
life easier.

In the end it comes down to the `Security, Functionality and Ease-of-Use triad
<https://blog.infosanity.co.uk/2010/06/12/infosec-triads-
securityfunctionalityease-of-use/>`_ where you can only ever actually achieve 2
of them.

Closing Remarks
===============

These are some thoughts I had on the initially linked tweet. I wanted to write
them down to not forget about them. There’s probably a lot more to consider and
at stake that I didn’t mention. I’m more than welcome to continue the
discussion on this topic in said Twitter thread.
