===========================
Django Migrations Recipe #3
===========================

:tags: Django, DjangoCon, Migration
:author: Markus Holtermann
:modified: 2016-05-02
:image: migration-recipe-3.jpg
:summary: This recipe shows how to rename an app that does not have any incoming
   dependencies.

This is the third migration recipe I publish for Django's migration framework.
I published it as part of my `talk at DjangoCon Europe 2016 in Budapest
<{filename}/Development/2016-04-04__en__dont-be-afraid-of-writing-
migrations.rst>`_. This recipe will show how to rename an app. For simplicity
the app must not have any dependencies from other apps!

Take an app "rename_app" with the following 2 models, an "Author" and a "Book".

.. code-block:: python

    # rename_app/models.py

    from django.db import models

    class Author(models.Model):
        name = models.CharField(max_length=50)

    class Book(models.Model):
        title = models.CharField(max_length=50)
        author = models.ForeignKey('rename_app.Author')

Similar to the previous recipe we create the initial migration and a data
migration and apply them:

.. code-block:: bash

    $ python manage.py makemigrations
    $ python manage.py makemigrations rename_app --empty --name initial_data

    # Edit rename_app/migrations/0002_initial_data.py

    $ python manage.py migrate rename_app

The first step in order to rename the app from "rename_app" to "new_app_name"
is forcing Django to a particular table name by adding the db_table attribute
on the models' meta classes:

.. code-block:: python

    # rename_app/models.py

    from django.db import models

    class Author(models.Model):
        name = models.CharField(max_length=50)

        class Meta:
            db_table = 'rename_app_author'

    class Book(models.Model):
        title = models.CharField(max_length=50)
        author = models.ForeignKey('rename_app.Author')

        class Meta:
            db_table = 'rename_app_book'

Also create the respective migration for this change and apply it:

.. code-block:: bash

    $ python manage.py makemigrations --name pin_db_tables

.. code-block:: python

    # rename_app/migrations/0003_pin_db_tables.py

    from django.db import migrations, models
    class Migration(migrations.Migration):
        dependencies = [
            ('rename_app', '0002_initial_data'),
        ]
        operations = [
            migrations.AlterModelTable(name='author', table='rename_app_author'),
            migrations.AlterModelTable(name='book', table='rename_app_book'),
        ]

.. code-block:: bash

    $ python manage.py migrate

The next step is letting Django think you've never applied these migrations
whilst not changing the database. You do that by passing the string "zero" as a
migration name together with the --fake flag to the migrate management command:

.. code-block:: bash

    $ python manage.py migrate rename_app zero --fake
    Operations to perform:
      Unapply all migrations: rename_app
    Running migrations:
      Rendering model states... DONE
      Unapplying rename_app.0003_pin_db_tables... FAKED
      Unapplying rename_app.0002_initial_data... FAKED
      Unapplying rename_app.0001_initial... FAKED

After that you need to do the actual rename of the files and references from
"rename_app" to "new_app_name" in every file, including your settings, models
and migration files.

EXCEPT for the "db_table" attribute! DO NOT CHANGE THIS NOW!

.. code-block:: python

    # in settings.py
    INSTALLED_APPS = [
        # ...
        'new_app_name.apps.NewAppNameConfig',
    ]


    # in new_app_name/models.py
    class Author(models.Model):
        author = models.ForeignKey('new_app_name.Author')

        class Meta:
            db_table = 'rename_app_book'  # Keep as is for now!


    # in new_app_name/migrations/0003_pin_db_tables.py and others
    dependencies = [
        ('new_app_name', '0002_initial_data'),
    ]

When you're done with that and you didn't make a mistake along the way, let
Django know about the new migrations. Again, you need to pass the --fake flag
in order to only record the migration as applied and not do any database
operations:

.. code-block:: bash

    $ python manage.py migrate new_app_name --fake
    Operations to perform:
      Apply all migrations: new_app_name
    Running migrations:
      Rendering model states... DONE
      Applying new_app_name.0001_initial... FAKED
      Applying new_app_name.0002_initial_data... FAKED
      Applying new_app_name.0003_pin_db_tables... FAKED

Last but not least, you can optionally drop the db_table attribute to rename
the tables from for example "rename_app_author" to "new_app_name_author". When
you remove the db_table attribute you have to run makemigration again:

.. code-block:: python

    # new_app_name/models.py

    from django.db import models

    class Author(models.Model):
        name = models.CharField(max_length=50)

    class Book(models.Model):
        title = models.CharField(max_length=50)
        author = models.ForeignKey('new_app_name.Author')

When you remove the db_table attribute you have to run makemigration again:

What you can see here is, that the table name is reset to None. Django will
therefore automatically derive the name from the app name and model name.

.. code-block:: bash

    $ python manage.py makemigrations --name rename_tables

.. code-block:: python

    # new_app_name/migrations/0004_rename_tables.py

    from django.db import migrations, models

    class Migration(migrations.Migration):
        dependencies = [
            ('new_app_name', '0003_pin_db_tables'),
        ]
        operations = [
            migrations.AlterModelTable(name='author', table=None),
            migrations.AlterModelTable(name='book', table=None),
        ]


.. code-block:: bash

    $ python manage.py migrate


Resources
=========

* `Slides <https://speakerdeck.com/markush/dont-be-afraid-of-writing-migrations>`_
* `Repository <https://github.com/MarkusH/migration-recipes>`_
