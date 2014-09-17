==========================================
Django 1.7: Database Migrations done right
==========================================

:tags: Database, Django, Migration
:author: Markus Holtermann
:status: draft


.. image:: /images/logos/django-negative-250x.png
   :align: right
   :alt: Django -- The Web framework for perfectionists with deadlines.
   :class: margin-left

About two weeks ago `Django 1.7 was released`_ with a lot of new and shiny
features, such the *App Loading Refactoring*, *Custom Lookups*, the *Checks
Framework* the *buildin Migration support* and many more. The release notes are
the longest in Django's history and span approx. 1,800 lines.

This article is inspired by the questions and problems I saw on Django's IRC
support channel ``#django`` on `Freenode`_ regarding the new migration
framework ``django.db.migrations``. I'll show different problems developers ran
into, explain why their particular way of doing something doesn't work
(anymore) and how to do this now.


Why not integrate South into Django?
====================================

A handful of people asked why `South`_ hasn't just been integrated into Django,
so all the old migrations would *just work*. There are many reasons why `Andrew
Godwin`_, the author of South, a Django core developer and the author of
``django.db.migrations`` did it differently. But one of the main reasons is
probably the way how South stores the state the database has over time, the so
called *frozen ORM*. When you look at a regular sized migration file you often
have about 50 lines of forwards and backwards code and a often continuously
growing *frozen ORM* below.

This is clearly not the best solution. Which is why another way of detecting
the changes between the current implementation of your app / project and the
database state created by the previous migrations had to be found.

Django 1.7 behaves differently. Whenever you run ``python manage.py
makemigrations myapp``, Django first applies all migration changes internally
by constructing the models and fields with their properties on-the-fly. In the
second step Django compares the state generated from all migration files to the
state presented in your code. All differences will be considered changes that
will be written in new migration files.

.. hint::

   One thing you might notice at some point, the models created by Django
   on-the-fly belong to the Python module ``__fake__``. This is the reason why
   you won't be able to access custom function on the model and why e.g. an
   overwritten ``save()`` will not be called.

To work around circular dependencies, Django splits a single migration file
into multiple within the same app. The resulting dependencies are declared in a
list at the top of a ``Migration`` class:

.. code-block:: python

    class Migration(migrations.Migration):

        dependencies = [
            ('thisapp', '0001_initial')
            migrations.swappable_dependency(settings.AUTH_USER_MODEL),
            ('otherapp', '0002_auto_20140915_1402')
        ]

        operations = [
            # some operations
        ]


How do dependencies between migrations work?
============================================

Let's assume you have two Django apps ``author`` and ``book`` with these
models:

.. code-block:: python

    # author/models.py
    from django.db import models

    class Author(models.Model):
        name = models.CharField('Author', max_length=255)
        birthday = models.DateField('Birthday')


    # book/models.py
    from django.db import models

    class Book(models.Model):
        title = models.CharField('Title', max_length=255)
        pages = models.PositiveSmallIntegerField()
        author = models.ForeignKey('author.Author')

What happens when you call ``python manage.py makemigrations``? First of all,
since no apps are given, Django reads the migrations from all apps listed in
``INSTALLED_APPS``. In our case, this is ``('author', 'book',)``. In the next
step Django replays all migrations it can find for those apps internally, as
explained above. Since there are no migrations yet, Django is going to start
from scratch:

.. code-block:: bash

    $ python manage.py makemigrations
    Migrations for 'book':
      0001_initial.py:
        - Create model Book
    Migrations for 'author':
      0001_initial.py:
        - Create model Author


As a result, you will end up with two migrations:

.. code-block:: python

    # author/migrations/0001_initial.py
    # -*- coding: utf-8 -*-
    from __future__ import unicode_literals

    from django.db import models, migrations


    class Migration(migrations.Migration):

        dependencies = [
        ]

        operations = [
            migrations.CreateModel(
                name='Author',
                fields=[
                    ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                    ('name', models.CharField(verbose_name='Author', max_length=255)),
                    ('birthday', models.DateField(verbose_name='Birthday')),
                ],
                options={
                },
                bases=(models.Model,),
            ),
        ]


    # book/migrations/0001_initial.py
    # -*- coding: utf-8 -*-
    from __future__ import unicode_literals

    from django.db import models, migrations


    class Migration(migrations.Migration):

        dependencies = [
            ('author', '0001_initial'),
        ]

        operations = [
            migrations.CreateModel(
                name='Book',
                fields=[
                    ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                    ('title', models.CharField(max_length=255, verbose_name='Title')),
                    ('pages', models.PositiveSmallIntegerField()),
                    ('author', models.ForeignKey(to='author.Author')),
                ],
                options={
                },
                bases=(models.Model,),
            ),
        ]

When you now run ``python manage.py migrate`` Django looks at all migrations
that haven't been applied yet and will perform all their operations in-order,
starting with the migrations that have no dependencies to migrations that
haven't been applied. In the case above, this is ``author.0001_initial``. The
``dependencies`` list is empty. Afterwards ``book.0001_initial`` can be
applied, because all dependencies are resolved.

.. hint::

    Django will try to run the migrations ordered by the name of the app they
    belong to. But obviously only if there are no dependencies that have to be
    resolved first.

You can see all migrations in all installed apps, as well as their status
(applied or not) by running ``python manage.py migrate --list``:

.. code-block:: bash

    $ python manage.py migrate --list
    author
     [ ] 0001_initial
    book
     [ ] 0001_initial


What is the "('myapp', '__first__')" dependency?
================================================

Let's say, ``author`` is a third party app that doesn't ship with Django
migrations. Remove the migrations folder ``author/migrations`` as well as
``book/migrations/0001_initial.py`` to start over. When you now run
``makemigrations``` you will end up with a single migration file for ``book``:

.. code-block:: bash

    $ python manage.py makemigrations
    Migrations for 'book':
      0001_initial.py:
        - Create model Book

.. code-block:: python

    #book/migrations/0001_initial.py
    # -*- coding: utf-8 -*-
    from __future__ import unicode_literals

    from django.db import models, migrations


    class Migration(migrations.Migration):

        dependencies = [
            ('author', '__first__'),
        ]

        operations = [
            migrations.CreateModel(
                name='Book',
                fields=[
                    ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                    ('title', models.CharField(verbose_name='Title', max_length=255)),
                    ('pages', models.PositiveSmallIntegerField()),
                    ('author', models.ForeignKey(to='author.Author')),
                ],
                options={
                },
                bases=(models.Model,),
            ),
        ]

The dependency ``('author', '__first__'),`` tells Django to apply a migration
at some point after the first migration in the referenced app, independent of
its name.


How do I add a data migration?
==============================

If you used `South`_ you might know about the ``datamigration`` command that
simply creates a new migration file in the given app and optionally adds some
models to the frozen ORM state.

In Django 1.7 it is way simpler: run
``python manage.py makemigrations --empty myapp`` You can rename the generated
file if you like as long as it ends with ``.py`` and doesn't contain a ``.``:

.. code-block:: python

    # -*- coding: utf-8 -*-
    from __future__ import unicode_literals

    from django.db import models, migrations


    class Migration(migrations.Migration):

        dependencies = [
            ('myapp', '0001_initial'),
        ]

        operations = [
        ]

Within this migration you can now add the `operations`_ you want to perform.
For data migrations you can use ``migrations.RunSQL`` or
``migrations.RunPython``.

.. important::

    If you add an empty migration file to an app and want to run operations
    that require another app to be migrated to a specific state, you *have to*
    add the required dependencies explicitly!


Running native SQL commands during migrations
---------------------------------------------

If you are able to express your data changes in SQL, *please* do so, this will
be faster than through the ORM. But keep in mind, that this might not be the
solution if you have to fight multiple database back-ends.

``RunSQL`` accepts 1 to 3 arguments: ``sql``, ``reverse_sql`` and
``state_operations``. ``sql`` is required and expects a string (that may
consist of multiple statements).

.. code-block:: python

    migrations.RunSQL("UPDATE myapp_mymodel SET col1 = col2 + col3;"
                      "UPDATE myapp_mymodel SET col2 = col3 * col3;")

If you don't specify the ``reverse_sql`` argument, you won't be able to
roll-back beyond this migration. The default is ``None``, using ``"SELECT 1;"``
is fine for a roll-back.

With the ``state_operations`` attribute you are able to modify the model state
Django internally constructs while running the migrations. I haven't seen a
usecase for that yet.

.. warning::

    As of time of writing, if you want to use ``%`` as a wildecard in e.g. the
    ``WHERE``- clause, you need to escape it with another ``%`` character
    (`Django issue #23426`_)::

        migrations.RunSQL("UPDATE myapp_mymodel SET col1 = 'a' WHERE col2 LIKE '%%val%%';")


Run custom Python code during migrations
----------------------------------------

Apart from the ``RunSQL`` operation Django 1.7 comes with a ``RunPython``
operation. This allows you to run custom Python function during a forwards or a
backwards migration.

``RunPython`` accepts 1 to 3 arguments: ``code``, ``reverse_code`` and
``atomic``. ``code`` is require and accepts any callable with two arguments, so
does ``reverse_code`` which is optional, though. ``atomic`` defaults to
``True``.

Please keep in mind that a ``reverse_code`` of ``None`` (the default) prevents
the migration from being rolled back. If you want to be able to roll-back,
because your Python code in ``code`` computes some initial data for every row
in a newly added column, add something like ``lambda x, y: None`` as
``reverse_code``.

For more details on the ``RunPython`` operation please see the `docs`_.


The callable for e.g. upload_to cannot be found
===============================================

There are a few model fields out their that take callables as arguments to do
further processing. One of those fields is the ``FileField`` that has an
``upload_to`` argument which accepts a string as well as a function to
dynamically derive the storage location. To make migrations work automatically,
this function has to be directly importable from a package or module.

The same goes for classes for custom fields: The way Python works doesn't allow
importing inner classes. Move the class to the module level and you'll be fine.

See the chapter about `serializing values`_ in the docs.


Backwards migrations roll-back too many operations
==================================================

The way Django handles the order of migrations and the fact that Django
strictly enforces dependencies between migration to be present during
migration, is different compared to South. While the forwards migration plans
won't really differ from South's, Django behaves completely different when it
comes to backwards migrations (at least in 1.7, follow `Django issue #23474`_
for updates).

By design Django will roll back the database to the state it would have if you
roll forward and stop after a given migration. To make this more clear, let's
take the following scenario from the Django tests:

.. code-block:: code

    app_a:  0001 <-- 0002 <--- 0003 <-- 0004
                             /
    app_b:  0001 <-- 0002 <-/

If you run ``python manage.py migrate`` you will end up with:

.. code-block:: code

    [X] app_a.0001
    [X] app_a.0002 ... (depends on app_a.0001)
    [X] app_b.0001
    [X] app_b.0002 ... (depends on app_b.0001)
    [X] app_a.0003 ... (depends on app_a.0002, app_b.0002)
    [X] app_a.0004 ... (depends on app_a.0003)

If you run ``python manage.py migrate app_a 0003`` from this state, you will
end up with:

.. code-block:: code

    [X] app_a.0001
    [X] app_a.0002 ... (depends on app_a.0001)
    [X] app_b.0001
    [X] app_b.0002 ... (depends on app_b.0001)
    [X] app_a.0003 ... (depends on app_a.0002, app_b.0002)
    [ ] app_a.0004 ... (depends on app_a.0003)

being applied.

The difference happens when you roll-back past a dependency.

If you run ``python manage.py migrate app_a 0002`` from the initial state, you
will end up with:

.. code-block:: code

    [X] app_a.0001
    [X] app_a.0002 ... (depends on app_a.0001)
    [X] app_b.0001
    [X] app_b.0002 ... (depends on app_b.0001)
    [ ] app_a.0003 ... (depends on app_a.0002, app_b.0002)
    [ ] app_a.0004 ... (depends on app_a.0003)

being applied.

But if you run ``python manage.py migrate app_b 0002``, from the initial state,
you will end up with:

.. code-block:: code

    [X] app_a.0001
    [X] app_a.0002 ... (depends on app_a.0001)
    [X] app_b.0001
    [X] app_b.0002 ... (depends on app_b.0001)
    [ ] app_a.0003 ... (depends on app_a.0002, app_b.0002)
    [ ] app_a.0004 ... (depends on app_a.0003)

being applied.

Do you recognize the missing ``app_a.0003`` here.


.. _Django 1.7 was released:
    https://www.djangoproject.com/weblog/2014/sep/02/release-17-final/

.. _Freenode: http://freenode.net/

.. _South: http://south.aeracode.org/

.. _Andrew Godwin: http://www.aeracode.org/

.. _operations:
    https://docs.djangoproject.com/en/1.7/ref/migration-operations/#special-operations

.. _Django issue #23426: https://code.djangoproject.com/ticket/23426

.. _docs:
    https://docs.djangoproject.com/en/1.7/ref/migration-operations/#runpython

.. _serializing values:
    https://docs.djangoproject.com/en/1.7/topics/migrations/#serializing-values

.. _Django issue #23474: https://code.djangoproject.com/ticket/23426
