===========================
Django Migrations Recipe #1
===========================

:tags: Django, DjangoCon, Migration
:author: Markus Holtermann
:modified: 2016-05-02
:image: migration-recipe-1.jpg
:summary: This recipe shows how one can optimize a migration Django creates.

This is the first migration recipe I publish for Django's migration framework.
I published it as part of my `talk at DjangoCon Europe 2016 in Budapest
<{filename}/Development/2016-04-04__en__dont-be-afraid-of-writing-
migrations.rst>`_. This recipe will show that migration code is just Python and
Django's built-in "makemigrations" command might not output the most efficient
migration.

This recipe show how one can optimize a migration Django creates.

Take the following 2 models, a "Book" and a "Library". Each book is associated
with exactly one library:

.. code-block:: python

    from django.db import models

    class Book(models.Model):
        title = models.CharField(max_length=200)
        library = models.ForeignKey('Library')

    class Library(models.Model):
        name = models.CharField(max_length=200)

When you run ``makemigrations`` for an app with these models you get 3
operations.

* The first one is a ``CreateModel`` operation and ensures the Book model
  exists with a primary key and a name. But the reference to the library is
  nowhere to be found.

* The ``CreateModel`` operation for the Library looks as expected. There's a
  primary key and a name.

* The next operation is an ``AddField``. And there it is, the library field for
  the Book model.

.. code-block:: bash

    $ python manage.py makemigrations
    Migrations for 'optimize_makemigrations':
      0001_initial.py:
        - Create model Book
        - Create model Library
        - Add field library to book

You may ask now why the ``ForeignKey`` is added as a separate operation. There
are 2, maybe 3 reasons behind that:

* Firstly, having references at the end of a migration when automatically
  creating one is always safe.

* Secondly, Django's migration framework processes all models within the same
  app in alphabetical order to provide a deterministic behavior. "Book" comes
  before "Library", last time I checked.

* Thirdly, nobody has contributed a patch yet. If you're staying for the
  sprints, that might be something to look into.

.. code-block:: python

    from django.db import migrations, models

    class Migration(migrations.Migration):
        dependencies = []
        operations = [
            migrations.CreateModel(
                name='Book',
                fields=[
                    ('id', models.AutoField(...)),
                    ('title', models.CharField(max_length=200)),
                ],
            ),
            migrations.CreateModel(
                name='Library',
                fields=[
                    ('id', models.AutoField(...)),
                    ('name', models.CharField(max_length=200)),
                ],
            ),
            migrations.AddField(
                model_name='book',
                name='library',
                field=models.ForeignKey(to='app.Library'),
            ),
        ]

Now, that we have this example, how can it be optimized? I guess some of you
already have an idea:

.. code-block:: python

    from django.db import migrations, models

    class Migration(migrations.Migration):
        dependencies = []
        operations = [
            migrations.CreateModel(
                name='Library',
                fields=[
                    ('id', models.AutoField(...)),
                    ('name', models.CharField(max_length=200)),
                ],
            ),
            migrations.CreateModel(
                name='Book',
                fields=[
                    ('id', models.AutoField(...)),
                    ('title', models.CharField(max_length=200)),
                    ('library', models.ForeignKey(to='app.Library')),
                ],
            ),
        ]

The answer to that is, to re-order the ``CreateModel`` operations and merge the
``AddField`` into the ``CreateModel`` for the Book.


Resources
=========

* `Slides <https://speakerdeck.com/markush/dont-be-afraid-of-writing-migrations>`_
* `Repository <https://github.com/MarkusH/migration-recipes>`_
