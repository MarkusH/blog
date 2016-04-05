===========================
Django Migrations Recipe #2
===========================

:tags: Django, DjangoCon, Migration
:author: Markus Holtermann
:image: migration-recipe-2.jpg
:summary: This recipe show how one can add a non-nullable column to a table
   with already existing data.

This is the second migration recipe I publish for Django's migration framework.
I published it as part of my `talk at DjangoCon Europe 2016 in Budapest
<{filename}/Development/2016-04-04__en__dont-be-afraid-of-writing-
migrations.rst>`_. This recipe will show how to add a non-nullable column to a
table with already existing data.

Adding columns is a common behavior when we write our software. Requirements
change and so do our models. Sometimes we'd like to add a column that we don't
want to be nullable on database level.

The following recipe works only when you have some data source where you can
get the value for existing values from. That could be a CSV file, an API that
you query or anything else.

Let's start with an Author model this time. The additional "create"
``classmethod`` is for demo purposes only and reflects all places in your code
where you create an Author instance:

.. code-block:: python

    from django.db import models

    class Author(models.Model):
        name = models.CharField(max_length=50)

        @classmethod
        def create(cls, name):
            return cls.objects.create(name=name)

Before we add a field we need to create the migration for the current state.
We'll also create a migration for initial data:

.. code-block:: bash

    $ python manage.py makemigrations
    Migrations for 'non_nullable_field':
      0001_initial.py:
        - Create model Author
    $ python manage.py makemigrations non_nullable_field --empty --name initial_data
    Migrations for 'non_nullable_field':
      0002_initial_data.py:

We'll use the empty migration to create some initial data:

.. code-block:: python

    from django.db import migrations

    def forwards(apps, schema_editor):
        Author = apps.get_model('non_nullable_field', 'Author')
        Author.objects.create(name='Author 1')
        Author.objects.create(name='Author 2')

    def backwards(apps, schema_editor):
        Author = apps.get_model('non_nullable_field', 'Author')
        Author.objects.filter(name='Author 1').delete()
        Author.objects.filter(name='Author 2').delete()

    class Migration(migrations.Migration):
        dependencies = [
            ('non_nullable_field', '0001_initial'),
        ]
        operations = [
            migrations.RunPython(forwards, backwards),
        ]

Each time this migration is applied the "forwards" function is being called and
two authors are being created. Each time the migration is unapplied the "backwards" function is being called
and the two authors are being deleted.

We can then apply all migrations

.. code-block:: bash

    $ python manage.py migrate non_nullable_field
    Operations to perform:
      Apply all migrations: non_nullable_field
    Running migrations:
      Rendering model states... DONE
      Applying non_nullable_field.0001_initial... OK
      Applying non_nullable_field.0002_initial_data... OK

Now we can proceed with adding an author's homepage. This is fairly easy by adding an URLField! Note that this is nullable for the
moment! We will change this to ``null=False`` a bit later:

.. code-block:: python

    from django.db import models

    class Author(models.Model):
        name = models.CharField(max_length=50)
        homepage = models.URLField(null=True)

        @classmethod
        def create(cls, name):
            return cls.objects.create(name=name)

But first, let's create and run migrations! Again

.. code-block:: bash

    $ python manage.py makemigrations
    Migrations for 'non_nullable_field':
      0003_author_homepage.py:
        - Add field homepage to author
    $ python manage.py migrate non_nullable_field
    Operations to perform:
      Apply all migrations: non_nullable_field
    Running migrations:
      Rendering model states... DONE
      Applying non_nullable_field.0003_author_homepage... OK

The next step is taking care of the homepage field. Each time we are creating
an author we want to ensure the homepage is set. This applies to all new items.

However, for existing rows we still need to take care of NULL values when
displaying the value:

.. code-block:: python

    from django.db import models
    from django.utils import html, safestring

    class Author(models.Model):
        name = models.CharField(max_length=50)
        homepage = models.URLField(null=True)

        @classmethod
        def create(cls, name, homepage):
            return cls.objects.create(name=name, homepage=homepage)

        @property
        def homepage_tag(self):
            if self.homepage:
                return html.format_html('<a href="{u}">{u}</a>', u=self.homepage)
            return safestring.mark_safe('<i>No homepage</i>')

Before we can eventually drop the so called "NULL constraint", we need to
populate records with NULL for homepage in the database with values. We do that
in another migration. Go ahead and create an empty one

.. code-block:: bash

    $ python manage.py makemigrations non_nullable_field --empty --name populate_data
    Migrations for 'non_nullable_field':
      0004_populate_data.py:

It doesn't really matter where you get the values for existing rows from. As
already said, this can be a CSV file, an API or anything else. The important
thing is that you ensure that in the end every row has a value. No row must be
NULL:

.. code-block:: python

    from django.db import migrations

    LOOKUP_DATA = {
        'Author 1': 'http://example.com',
        'Author 2': 'http://other.org',
    }

    def forwards(apps, schema_editor):
        Author = apps.get_model('non_nullable_field', 'Author')
        for author in Author.objects.filter(homepage__isnull=True):
            author.homepage = LOOKUP_DATA[author.name]
            author.save(update_fields=['homepage'])

    class Migration(migrations.Migration):
        dependencies = [
            ('non_nullable_field', '0003_homepage'),
        ]
        operations = [
            migrations.RunPython(forwards, migrations.RunPython.noop),
        ]

Go ahead and apply that migration. Everything past this comparably easy

.. code-block:: bash

    $ python manage.py migrate non_nullable_field
    Operations to perform:
      Apply all migrations: non_nullable_field
    Running migrations:
      Rendering model states... DONE
      Applying non_nullable_field.0004_populate_data... OK

Let's start by dropping the "null=True" from the URLField:

.. code-block:: python

    from django.db import models
    from django.utils import html, safestring

    class Author(models.Model):
        name = models.CharField(max_length=50)
        homepage = models.URLField()

        @classmethod
        def create(cls, name, homepage):
            return cls.objects.create(name=name, homepage=homepage)

        @property
        def homepage_tag(self):
            if self.homepage:
                return html.format_html('<a href="{u}">{u}</a>', u=self.homepage)
            return safestring.mark_safe('<i>No homepage</i>')

When you now run "makemigrations" Django is asking you how to handle the
change. Django doesn't know that we took care of all NULL values. Hence we need
to tell it: Select option 2

.. code-block:: bash

    $ python manage.py makemigrations --name not_null_constraint

    You are trying to change the nullable field to non-nullable without a default ...
    Please select a fix:
     1) Provide a one-off value ...
     2) Ignore for now ...
     3) Quit ...
    Select an option: 2
    Migrations for 'non_nullable_field':
      0005_not_null_constraint.py:
        - Alter field homepage on author

This is the resulting migration. As you can see in the AlterField operation,
the URLField doesn't have a ``null=True`` anymore and will therefore add a ``NOT NULL``
constraint to the database:

.. code-block:: python

    from django.db import migrations, models

    class Migration(migrations.Migration):
        dependencies = [('non_nullable_field', '0004_populate')]
        operations = [
            migrations.AlterField(
                model_name='author',
                name='homepage',
                field=models.URLField(),
            ),
        ]

Go ahead and apply that migration

.. code-block:: bash

    $ python manage.py migrate non_nullable_field
    Operations to perform:
      Apply all migrations: non_nullable_field
    Running migrations:
      Rendering model states... DONE
      Applying non_nullable_field.0005_not_null_constraint... OK

Lastly, you should remove the code that handles NULL values from your code
base:

.. code-block:: python

    from django.db import models
    from django.utils import html

    class Author(models.Model):
        name = models.CharField(max_length=50)
        homepage = models.URLField()

        @classmethod
        def create(cls, name, homepage):
            return cls.objects.create(name=name, homepage=homepage)

        @property
        def homepage_tag(self):
            return html.format_html('<a href="{u}">{u}</a>', u=self.homepage)


Resources
=========

* `Slides <https://speakerdeck.com/markush/dont-be-afraid-of-writing-migrations>`_
* `Repository <https://github.com/MarkusH/migration-recipes>`_
