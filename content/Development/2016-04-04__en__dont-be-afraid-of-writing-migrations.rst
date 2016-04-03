=====================================
Don't be afraid of writing migrations
=====================================

:tags: Django, DjangoCon, Migration, Talk
:author: Markus Holtermann
:image: djangoconeu2016/talk-cover.jpg
:summary: Django migrations are complex. They do a lot for you but sometimes
   you need to tell 'em how to do things. There's no reason to be afraid of
   that, though.

Introduction
============

`Django's migration framework
<https://docs.djangoproject.com/en/dev/topics/migrations/>`_ evolved a lot
since it first release with 1.7.  Heaps of bugs have been fixed and numerous
features added.

However, there are still lots of things that can be improved to make migrations
faster, some tasks more convenient to use, and some tasks even possible. One
thing in particular is the ``makemigrations`` management command that
automatically outputs the required migrations when you changed a model. But
there are things ``makemigrations`` just can't do. In those cases you need to
write migrations by hand.

Writing migrations may sound scary, but in this blog post and the related talk
I want to explain why you don't need to be afraid of writing migrations. I
provide 3 recipes, an easy, and intermediate and a more complex one, which you
can use for to get a feeling for how migrations work and how to solve problems
you encounter in your own projects. Be advised that some of the recipes may
only work with PostgreSQL. SQLite doesn't enforce ForeignKey integrity and on
MySQL you're screwed when migrations fail. I didn't try Oracle.


General Layout
==============

Before I go into any details or internals, let me explain the general layout of
a migration:

.. code-block:: python

    from django.db import migrations

    class Migration(migrations.Migration):
        dependencies = []
        operations = []

You start off with a class called ``Migration`` inheriting from
``django.db.migrations.Migration``.

You then have an attribute ``dependencies`` which is a list of 2-tuples
pointing to other migrations which this migration depends on. As an example,
when you have a "Profile" model with a ``ForeignKey`` to a "User" model, the
user database table needs to exist before the profile table can point to the
user table.

The "operations" attribute holds a list of migration operations, such as
``CreateModel``, ``AddField``, or ``AlterField``. These operations will be run
in order when you apply a migration file.


Recipes
=======

* `Recipe #1 -- Optimize the initial creation of related models
  <{filename}/Development/2016-04-04__en__django-migrations-recipe-1.rst>`_
* `Recipe #2 -- Add a non-nullable column to a table with already existing data
  <{filename}/Development/2016-04-04__en__django-migrations-recipe-2.rst>`_
* `Recipe #3 -- Rename an app without incoming dependencies
  <{filename}/Development/2016-04-04__en__django-migrations-recipe-3.rst>`_


Resources
=========

* `Slides <https://speakerdeck.com/markush/dont-be-afraid-of-writing-migrations>`_
* `Repository <https://github.com/MarkusH/migration-recipes>`_
