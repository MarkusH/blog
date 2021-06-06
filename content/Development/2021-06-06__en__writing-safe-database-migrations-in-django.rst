==========================================
Writing Safe Database Migrations in Django
==========================================

:tags: Django, DjangoCon, Migration
:author: Markus Holtermann
:image: djangoconeu2021/talk-cover.jpg
:summary: Whenever you deploy your code and apply migrations in production,
   you're entering dangerous territory. I'll show common pitfalls and ways
   to avoid them.

Five years ago, at DjangoCon Europe 2016 in Budapest, I gave a talk `Don't Be
Afraid Of Writing Migrations`_. Back then, while migrations in Django weren't
particularly new, they shipped in 2014, I saw many folks struggle and worry
about touching the migration files. And even fewer wrote migrations by hand.
Mind you, I wouldn't recommend writing entire migration files by hand. Django
has tools to generate them for us. But I do recommend looking at them,
understanding what they do, and then see if they need to be adjusted. Because,
in the end, as an engineer, you will always know more about your application
than Django will ever be able to.

As an example, when you add a non-nullable field to a model and run
``makemigrations``, Django will ask you for a one-off default value. That value
would be set for all existing rows. This is the correct behavior when there's
data in that table already. But if you know that the table is empty everywhere,
it can easily appear to be useless. As an engineer, you can make a distinction
there. As an engineer you can decide that it's fine not to have a default
value. As an engineer, you know more about your project than Django does. But
Django must be conservative to ensure the default way works for everyone.


Migrations! How? When?
======================

I want to start this post with some general considerations. Questions like how
and when do you apply migrations? How are migrations related to deployments?
What are dos and don'ts that follow from that?

If you run a somewhat serious site, you are aiming for something called
zero-downtime deployments. On common way for that is something called a rolling
upgrade or a staged rollout. On a high level, it works like this.

In the beginning, all your servers run the old version of you application. They
are indicated by the blue circle. Then you start rolling out the new version to
a few servers (indicated by the orange part). You keep this state for a short
while, to ensure everything keeps working. Over time, you deploy the new
version to more and more servers. Until the new version is running everywhere.

.. image:: /images/djangoconeu2021/deployment-stages.png
   :alt: Stages of a staged-rollout process.
   :class: responsive-img

The clear benefit of this rolling upgrade or staged rollout is the ability to
notice issues early on, way before the new version is running everywhere. The
benefit is in addition to the fact that your site remains fully available
during the entire time.

But these benefits come at a price.

As you can easily imaging, running two versions of you application means, they
need to be compatible. Essentially, whatever the new version does, the previous
version needs to be able to keep functioning the way it did before. This is not
always easy. And, unless this becomes a habit, this requirement can easily be
forgotten. At least until the next deployment fails because of that.

But while it's often far from trivial to ensure that the backwards
compatibility is kept for the business logic, it becomes even more tricky when
we involve databases. Whatever you do with objects in the database, you need to
remember that there can always be this one server that has not been updated yet
and thus runs the previous version.

Which brings me back to one of the opening questions.

When Do We Deploy Migrations?
-----------------------------

Since you never really know when the last server was updated, but it's somewhat
easy to figure out when you start a deployment, I'd recommend to always apply
migrations right before you start deploying your code.

Now, this comes with some serious implications. If you do so, you cannot remove
a model or a field from a model in the same release as the one that contains
the migration. If you were to do that, because migrations run first, you'd
remove a database table or a column from a table while some servers may still
try to use it.

If you want to remove something, you will need to make two releases. The first
one removes the usage of the model or field from all your code. The release is
deployed everywhere, the second release can remove the table or field from the
database. This is now safe since there's no code anymore that may access them.

In other words: when you add something to a model, or loosen the constraints,
such as the maximum length of a char field, you must do that before the
deployment. When you tighten the constraints or remove something, you must have
two releases, the first one that works with the new constraints and the second
one that then puts them in the database or removes a field or table.

Which leaves the question: how do rename a field? Short answer, you don't. The
long answer is you add a new field, copy the data, and remove the old one.
Something similar to the third migration recipe from my previous talk.

Which brings me to the next question.

How Do We Deploy Migrations?
----------------------------

While I'd love to present the perfect solution to you, I can't. And I can't,
for several reasons.

For once, everyone, every team, every company has their own processes for
releasing new versions of their software.

The spectrum of how these processes work is shier endless. There's that super
hip startup, that has a CI/CD pipeline that automatically deploys to a staging
system where integration and end-to-end tests are run. And if all of them pass,
the CI/CD automatically deploys to production. And the release pipeline runs
for each merged pull request.

On the other hand, you have enterprises where a database administrator types in
the SQL statement manually to make a change to the database. And that process
is preceded with a change request process where 3 department heads have to sign
off. Or something like that.

If we look a little bit below the surface of the variety of those processes, we
can see that they all have something in common.

Only Go Forwards & Never Look Back
----------------------------------

They all only make changes in one direction: forwards.

If you think about it, it actually makes sense. If you made a change to the
database, you might not be able to undo it. Data that was removed is gone. You
can't magically undo a DROP TABLE statement once a transaction is committed.
What you can do, however, is recreate that table and restore the data from a
backup that you obviously took before applying the migration and that you
obviously also tested. Because that's what one does, isn't it?

The thing is, the moment something is shared with others, and that's kind of
the point of databases, you have to expect that somebody else is using it.

So, why does Django provide a way to unapply a migration? Well, I don't know.
But I do know that it's quite a useful tool during development. But when it
comes to databases for staging and production and such, I'd really recommend to
not go backwards. Depending on when exactly the migration occurs compared to
when new code is deployed, you may even be running code that expected a
migration to be applied.

And, given two migrations that depend on each other, but where the first one
has additional, unrelated changes to the second one, how would you roll back
those unrelated changes? The answer to that is, a new migration that rolls back
the corresponding changes.

This "only go forward" and "apply migrations before deployment" has gone so far
for the Django projects I maintain, that the entrypoint script for my Docker
containers is this:

.. code-block:: shell

    #!/bin/sh

    set -e

    cmd="$@"

    until django-admin dbshell -- --command '\q'; do
      >&2 echo "Postgres is unavailable - sleeping"
      sleep 1
    done

    >&2 echo "Postgres is up - executing command"

    django-admin migrate -v 2

    exec $cmd

I'll first try to connect to the database, PostgreSQL in this case, until it
succeeds. Once done, I apply all migrations in the project. And then execute
the actual command, such as running gunicorn.

This approach works very, very well for me.

There's a small gotcha, though. Since applying the migrations is part of the
entrypoint of each Docker container, Django will attempt to apply migrations
each time a container starts, which adds to the startup time. However, if no
migrations need to be applied, the migrate command is like a no-op. However,
when you think back about the staged rollout, you must make sure that the very
first stage is exactly one Docker container.

Now, after all this theory, let's look at something more hands-on.

Adding A Field Is Harmless
==========================

Our database models evolve over time. And one of the most frequent changes we
do to our models, is adding field. And doing so seems rather harmless, doesn't
it?

We have two models.

.. code-block:: python

    from django.db import models

    class AddFieldModel1(models.Model):
        name = models.CharField(max_length=10)

    class AddFieldModel2(models.Model):
        name = models.CharField(max_length=10)

In the first one, we add a nullable field, in the second one, we add a field
with an explicit default value. This seems fine, right?

.. code-block:: python

    from django.db import models

    class AddFieldModel1(models.Model):
        name = models.CharField(max_length=10)
        field = models.CharField(max_length=10, null=True)

    class AddFieldModel2(models.Model):
        name = models.CharField(max_length=10)
        field = models.CharField(default="aaaaaaaaaa", max_length=10)

First, let's look at the migration that Django creates

.. code-block:: python

    from django.db import migrations, models

    class Migration(migrations.Migration):

    dependencies = [
        ("add_field", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="addfieldmodel1",
            name="field",
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name="addfieldmodel2",
            name="field",
            field=models.CharField(default="aaaaaaaaaa", max_length=10),
        ),
    ]

For those of you who have looked at migration files before, this is nothing
new. For everyone else, let me briefly explain what you can see here:

First, this migration depends on another one, namely migration ``0001_initial``
form the app ``add_field``. Which means, this migration can only ever be
applied to the database, when that dependency has been applied. Or in reverse:
when you are applying this migration, that dependency will be applied before.

Second, you see a list of operations. An operation is Django's abstraction
around some so called database instructions that alter your database, such as
adding and removing database columns, creating and removing database tables,
and more.

The two operations here, each add a field called ``field`` to the models
``addfieldmodel1`` and ``addfieldmodel2``, respectively. The field that is
added is then describe there.

We can now use Django's ``sqlmigrate`` command to get the underlying SQL
commands.

.. code-block:: sql

    BEGIN;

    --
    -- Add field field to addfieldmodel1
    --
    ALTER TABLE "add_field_addfieldmodel1" ADD COLUMN "field" varchar(10) NULL;

    --
    -- Add field field to addfieldmodel2
    --
    ALTER TABLE "add_field_addfieldmodel2" ADD COLUMN "field" varchar(10) DEFAULT 'aaaaaaaaaa' NOT NULL;
    ALTER TABLE "add_field_addfieldmodel2" ALTER COLUMN "field" DROP DEFAULT;

    COMMIT;

All of these commands still look fairly harmless, don't they?

Well, you might have guessed it, the answer is no!

The first ``ALTER TABLE`` is kind of okay, but the second one can cause you
some real headache.

To understand why, we need to understand how databases handle these types of
schema alterations.

Adding a nullable column, as we do in the first case, is nothing more than some
metadata update. The so called table header will include the new column, a flag
that its nullable, and that's it. None of the existing records will need to be
updated. Any new record that has a non-null value, will include that value.

For our second case, however, the database will not only need to add the column
to the table header, but it will also need to go through all database records
in that table and set the default value. And this can take quite some time, if
you have a table with a lot of records.

Additionally, since your database will take a fairly heavy lock on the table,
you might even render your site inaccessible, in case the table you're
modifying is used rather frequently. Because both read and write queries might
be blocked.

That is, unless you use PostgreSQL 11 or newer, which also deals with the
second case in a clever and very efficient way. However, since you might not
know which database your code is running on, for example, because you're
writing a reusable Django app, it's a good idea to always take approach number
one and scratch the idea of adding a default value out of your head.

But I Want A Default Value!
===========================

Well, okay. You can get a default value. `The migration recipe number two`_ in
talk linked before gives you step-by-step instructions.

However, I'd only recommend that approach for tables with a fairly small amount
of records.

That is, because Django runs each migration inside a transaction. If you're
updating a hundred million records at ones, depending on what your application,
or rather its users, might be doing during that time, you can easily get to a
point where the transaction needs to be rolled back. Imaging going through 99
million records and then the transaction fails. That's more than annoying. To
ensure that doesn't happen, you'd need to get a write lock on all records in
the table, which can again lead to an unavailability of your entire site.

So, how do you deal with this?

Write a management command and run that after applying the migration:

.. code-block:: python

    from django.core.management.base import BaseCommand
    from django.db import transaction

    from safe_migrations.add_field.models import AddFieldModel1

    CHUNK_SIZE = 5000


        class Command(BaseCommand):
        def handle(self, *args, **options):
            updated = CHUNK_SIZE
            while updated >= CHUNK_SIZE:
                with transaction.atomic():
                    ids = (
                        AddFieldModel1.objects.filter(field__isnull=True)
                        .select_for_update()
                        .values_list("id", flat=True)[:CHUNK_SIZE]
                    )
                    updated = AddFieldModel1.objects.filter(id__in=ids).update(
                        field="bbbbbbbbbb"
                    )

The management command will lock at most 5000 objects at a time, and then
update their field value.

By using ``select_for_update()`` for each chunk, you can be sure that the field
value for those objects won't be overridden by anybody else in the meantime.

Sure, running this command will take longer than updating all records at once
while locking your table. But it allows you to keep your site operational.
Which, very often, I guess, is more important.

But coming back to what I said earlier, as an engineer you know more about the
project than Django does, this applies here as well. If you know that the table
you're adding a field to is small or maybe even empty, it's absolutely okay to
add a default value.

Which brings me to another topic. Databases are usually pretty good a
retrieving data very efficiently. So much so, that, until a certain threshold,
a full table scan is more efficient than looking up rows in an index. But at
some point, your table outgrows that point and you need an index.

Adding An Index
===============

Modern Django versions provide not just one but two ways to do so:

.. code-block:: python

    from django.db import models

    class AddIndexModel1(models.Model):
        name = models.CharField(max_length=10)

    class AddIndexModel2(models.Model):
        name = models.CharField(max_length=10)

Firstly, the old way that's been around forever. You can set ``db_index=True``
on a field and Django will create an index.

Secondly, since Django 1.11, you can define class based indexes in a model's
``Meta`` class. They are far more flexible, and powerful. And since Django 3.2
you can even add indexes on expressions, also known as functional indexes.

.. code-block:: python

    from django.db import models

    class AddIndexModel1(models.Model):
        name = models.CharField(max_length=10, db_index=True)

    class AddIndexModel2(models.Model):
        name = models.CharField(max_length=10)

        class Meta:
            indexes = [
                models.Index(fields=("name",), name="my_idx")
            ]

There's actually a third option. The ``index_together`` / ``unique_together``
attributes in the model's ``Meta`` class allow you to create indexes on
multiple columns.  Personally, I'd consider them outdated as well.
Additionally, for the example at hand, I'm going to ignore them. Because they
behave identically to ``db_index`` and can be replaced with class-based
indexes.

Looking at the auto generated migration, you can see an ``AlterField`` which
adds the ``db_index=True``, as well as an ``AddIndex`` operation.

.. code-block:: python

    from django.db import migrations, models

    class Migration(migrations.Migration):

    dependencies = [
        ("add_index", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="addindexmodel1",
            name="name",
            field=models.CharField(db_index=True, max_length=10),
        ),
        migrations.AddIndex(
            model_name="addindexmodel2",
            index=models.Index(fields=["name"], name="my_idx"),
        ),
    ]

A downside of the ``AlterField`` operation is, that you don't really see on the
Python level what changed on the field. You need to search for the last
migration operation involving a field in order to be able to tell that the
index was added.

In contrast to that, the ``AddIndex`` operation is clear in what it does: it
adds an index.

When we now look at the generated SQL, we can see something very interesting:

.. code-block:: sql

    BEGIN;

    --
    -- Alter field name on addindexmodel1
    --
    CREATE INDEX "add_index_addindexmodel1_name_adf72323" ON "add_index_addindexmodel1" ("name");
    CREATE INDEX "add_index_addindexmodel1_name_adf72323_like" ON "add_index_addindexmodel1" ("name" varchar_pattern_ops);

    --
    -- Create index my_idx on field(s) name of model addindexmodel2
    --
    CREATE INDEX "my_idx" ON "add_index_addindexmodel2" ("name");

    COMMIT;

Firstly, ``db_index`` not only adds a single index, but it adds two. The first
one is the one that we all expect. The second one, however, is one that Django
adds to make ``LIKE`` queries efficient.

Secondly, the name for the auto-generated ``db_index`` indexes is unpleasant to
look at. The 8 random characters are part of an MD5 hash over several
attributes to uniquely identify the index.

Using the class based index, we can, however define out own index name, which
makes it so much more pleasant to look at. Using meaningful index names has the
added benefit that it's easier to debug database issue. The index name can
carry additional context that then allows the database administrators to debug
certain issues more effectively. But it's important to know that some
databases, among them PostgreSQL requires an index name to be unique within a
database. Using ``my_idx`` as I did in the example here, is probably not the
best idea. But it's short to read and makes the code fit on the slides.

Now, if you go ahead and apply this migration on your database, you'll be fine
when there's not really any load on it and when a table doesn't have a lot of
records. However, as with the ``ADD COLUMN`` example earlier, this operation
can lock your table for quite a while.

And the worst thing, using ``db_index``, it does so twice. Once for each index.
Even if you'll never use the one for LIKE queries.

I got to admit, though, using a ``CharField`` as an example here is the worst
example I could give. If you set ``db_index`` on an ``IntegerField`` Django
will only create one index. But this demonstrates that it's a good idea to look
at the migration files and see what they'll actually do.

So, how do we fix the table lock issue?

Well, PostgreSQL can build indexes concurrently, while allowing access to the
data in the underlying table. That, however, comes with the downside that this
needs to run outside of transactions.

Since each migration runs within a transaction, we need to set
``atomic=False``.  Then we can use ``AddIndexConcurrently`` to turn our
class-based index into one that's added concurrently.

.. code-block:: python

    from django.contrib.postgres.operations import AddIndexConcurrently
    from django.db import migrations, models

    class Migration(migrations.Migration):

    atomic = False
    dependencies = [
        ("add_index", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="addindexmodel1",
            name="name",
            field=models.CharField(db_index=True, max_length=10),
        ),
        AddIndexConcurrently(
            model_name="addindexmodel2",
            index=models.Index(fields=["name"], name="my_idx"),
        ),
    ]

Let's look at what actually changed on the SQL level:

.. code-block:: sql

    --
    -- Alter field name on addindexmodel1
    --
    CREATE INDEX "add_index_addindexmodel1_name_adf72323"
    ON "add_index_addindexmodel1" ("name");
    CREATE INDEX "add_index_addindexmodel1_name_adf72323_like"
    ON "add_index_addindexmodel1" ("name" varchar_pattern_ops);

    --
    -- Create index my_idx on field(s) name of model addindexmodel2
    --
    CREATE INDEX CONCURRENTLY "my_idx" ON "add_index_addindexmodel2" ("name");

As you can see, the ``BEGIN`` and ``COMMIT`` statements are gone. And the last
``CREATE INDEX`` statement now has an additional ``CONCURRENTLY``.

Now, if you're asking yourself how you deal with that on MySQL and MariaDB, I
got to disappoint you: you don't. Because luckily, you do not even need to,
because adding indexes there happens without locking the whole table.

Test Your Migrations
====================

Even with all these suggestions and tips, one thing remains. You should test
your migrations. I'm not necessarily talking about unit tests. Yes, maybe, it
depends. No, I mean, you should test your migrations in a production-like
environment. Have some test scenarios available that you can refer to when
migrations touch a particularly large table or one that's accessed frequently.
See and try out how the database behaves.

But it's important to understand, that this level of testing of migrations is
not something I'd do for each migration. But it's something that can help you
understand how your database works and what impact on the production
environment you might see. But in the end, whatever you do in a testing
environment, it's not your production environment and thus _will_ behave
slightly differently. Even if it's just for the users that behave different
than usual.

Summary
=======

Which brings me to the end of this talk.

Let me briefly summarize what we've seen today:

It's usually a good idea to apply migrations before you deploy and run new
code. While not trivial, it's relatively easy to wrap one's head around it.
``CreateModel`` and ``AddField`` can go into the same release as the code;
``DeleteModel`` and ``RemoveField`` need a separate release. Renaming is a
combination of add and remove.

It's a good approach to only ever go forwards. Rolling back database migrations
can lead to additional unexpected behavior, in addition to the one you're
facing already.

When adding fields to existing models, make it a habit to add nullable columns
without a default value. It's a good pattern that's always safe.

If you want default values, that's fine, but populate existing rows manually.

When you add indexes, try to do that concurrently. Again, especially on bigger
tables.

.. _Don't Be Afraid Of Writing Migrations: {filename}/Development/2016-04-04__en__dont-be-afraid-of-writing-migrations.rst
.. _The migration recipe number two: {filename}/Development/2016-04-04__en__django-migrations-recipe-2.rst
