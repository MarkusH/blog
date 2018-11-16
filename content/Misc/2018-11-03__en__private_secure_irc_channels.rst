=========================================
Setting up a private & secure IRC channel
=========================================

:tags: IRC, Security
:author: Markus Holtermann
:image: irc-terminal.jpg
:summary: While over 30y old, IRC is still used today. A lot because of it's
   reliability and configuration options. But those make setting up a private
   IRC channels hard.


The `Internet Relay Chat (IRC) <https://en.wikipedia.org/wiki/Internet_Relay_Chat>`__
was create in 1988 by Jarkko Oikarinen. And it's stil around and used. At least
today there are a ton of configuration options one has at their disposal to
configure their nick, channels, or their client.

In this post I'll show you how you can create and register a private and
secured IRC channel that restricts who has access and can post to it.

This post assumes that you have registered and authenticated at the IRC
network.

First things first, you need to create a channel. Let's call it ``#project``::

    /join #project

You then want to make sure that channel is registered to yourself::

    /msg ChanServ REGISTER #project

You also want to enable the ``ChanServ`` guard so you can reclaim access and
have it keep the channel in the state you want it to be, if you ever are kicked
out::

    /msg ChanServ SET #project GUARD ON

Now, you need to define who has *full* access to that channel. That means they
could add others who have full permissions. And they'd be able to kick you out
and revoke your access::

    /msg ChanServ FLAGS #project USERNAME +AFRefiorstv

Next up, you can hide the channel from channel lists and user profiles. We'll
also enable a verbose logging mode that shows who changed what::

    /msg ChanServ SET #project PRIVATE ON
    /msg ChanServ SET #project VERBOSE ON

We'll then set a couple of channel modes. These are -- in order -- SSL only,
no color, members can invite, invite only, no external messages, private,
block unidentified, secret::

    /msg ChanServ SET #project MLOCK +Scginprs

At this point, nobody else than the people you added above, will have access.
To change that you'll need to add them to the invite list. Replace the
``USERNAME`` part only. The ``$a:`` indicates it's an account and needs to be
part of this statement::

    /mode #project +I $a:USERNAME

Lastly, you may want to check the invite list again::

    /mode #project +I
