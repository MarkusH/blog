=================================
bakery -- Where cookies are made!
=================================

:tags: Django, Git, Python
:author: Markus Holtermann

It has been some time since my last blog post. So here's an update. This is
about a great event I participated in last weekend, the `djangodash 2013`_.

The djangodash is an coding contest where teams have 48 hours time to start and
sprint a project. As this dash is called *djangodash*, the Django must be used.
Furthermore the teams are limited to at most 3 members and a couple of other
`rules`_.

So, what project were my friend and I working on? It's called *bakery*. You can
find it on `github`_ as well as a live version at
`djangodash2013.webshox.org`_. But what does *bakery* actually do and what is
it?  In simplified terms *bakery* is an index for `cookiecutter`_ templates. In
longer terms, *bakery* offers an API to create, find, modify, update and share
cookiecutter templates at a central point to clear up the mess with manually
updated readme files providing an incomplete list of templates. Additionally
*bakery* offers some neat features such as forking a template to your own
github account or voting a template up.  We are working on many more planned
features, e.g. automatically updating the index, directly editing the
cookiecutter.json file on the index.

So, what are these *cookiecutter* templates and what is *cookiecutter*?
*cookiecutter* itself is a tool that, given a project template, bootstraps a
project with its directory structure and files (including their content) based
on a set of context variables. To see what these templates (aka cookiecutters)
look like, just have a look at the `list of available cookiecutters`_.

.. _djangodash 2013: http://djangodash.com/
.. _rules: http://djangodash.com/rules/
.. _github: https://github.com/muffins-on-dope/bakery
.. _djangodash2013.webshox.org: http://djangodash2013.webshox.org/
.. _cookiecutter: https://github.com/audreyr/cookiecutter
.. _list of available cookiecutters: https://github.com/audreyr/cookiecutter#available-cookiecutters
