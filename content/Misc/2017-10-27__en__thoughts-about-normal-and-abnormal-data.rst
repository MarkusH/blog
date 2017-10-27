=======================================
Thoughts About Normal and Abnormal Data
=======================================

:tags: Database, Python, Talk
:author: Markus Holtermann
:image: pyconuk2017/talk-cover.jpg
:summary: A lot of data lives in relational databases. And there are relations
   between records in these databases. Relations that might be normal or
   abnormal.


.. image:: /images/pyconuk2017/logo.jpg
   :align: right
   :alt: PyCon UK 2017 logo
   :class: margin-left


A lot of our data lives in databases. A lot of those databases are relational
databases. They are called relational due to the way how objects refer to each
other. But just because having references between certain records is "normal"
and "what you should do" it doesn't mean it's the best choice.

This post is not about files. Neither in a file room nor your spreadsheet or
PDF document. Everyone has their own system of how they store their files. And
I think that's a good thing.

This post is also not about document stores or document databases like MongoDB
or CouchDB. In my opinion all these data stores have their reason to exist.
It's just not something I am looking into here.

What I am going to cover are relational databases, such as PostgreSQL, MySQL
and a whole lot more. The key here lies on *relational* databases.

In order to understand what normal or abnormal data is, I need to talk about
some database theory.

Database Theory
===============

Let's say we want to store a few person names, which planets they are from and
what gender they identify with.

If you were to put that information in a database table this might very well
look a bit like this:

===== =============== ======
Name  Home planet     Gender
===== =============== ======
Padmé Naboo           Female
Luke  Tatooine        Male
Leia  Alderaan, Naboo Female
===== =============== ======

There is a problem with this format, though. You need to store two planet names
in a single cell. This is certainly possible but will eventually lead to
problems. For example filtering for all people from Naboo can get tricky. If
you are using PostgreSQL you can put that into an array field that can get
around a few of these issues but not all.

First Normal Form
=================

This is the time where in relational database theory the so called *First
Normal Form* or *1NF* is introduced.

First mentioned by Edgar Codd in 1971, there are a few criteria a table needs
to fulfill for it to be considered in First Normal Form. Firstly, each cell
must have atomic or indivisible entities. Secondly, each row needs to be
uniquely identifiable.

When we apply these two rules, our table can look like this:

======== ===== =========== ======
PersonID Name  Home planet Gender
======== ===== =========== ======
1        Padmé Naboo       Female
2        Luke  Tatooine    Male
3        Leia  Alderaan    Female
3        Leia  Naboo       Female
======== ===== =========== ======

We introduced a PersonID that we will start to use to reference a person. We
also changed the combined "Alderaan, Naboo" value into two distinct rows.
However, now the PersonID itself is not uniquely identifying anymore. As such,
the key to identify a person now is a combination of PersonID and Home Planet.

This is all great and we're happy now, but we can run into a problem over time
while using our data. This table suffers from Update Anomalies. Let's look at a
subset at the previous table:

======== ===== =========== ========
PersonID Name  Home planet Gender
======== ===== =========== ========
3        Leia  Alderaan    Female
3        Leia  Naboo       **Male**
======== ===== =========== ========

If Leia were to change her gender and would identify herself as male, we would
need to update every row in the table with the new gender. If we don't update
all rows but instead only update some, we end up with inconsistent data. And
that is something you certainly don't want to have happen to your production
data.

Second Normal Form
==================

To remedy this issue there exists a *Second Normal Form* or *2NF*.

The Second Normal Form was defined by Edgar Codd in 1971 as well. In addition
to the criteria from the First Normal Form it requires that *all non-key
attributes are fully functional dependent on the primary key*. Now, what does
that even mean? Let's look at the table again:

======== ===== =========== ======
PersonID Name  Home planet Gender
======== ===== =========== ======
1        Padmé Naboo       Female
2        Luke  Tatooine    Male
3        Leia  Alderaan    Female
3        Leia  Naboo       Female
======== ===== =========== ======

The primary key is the combination of PersonID and Home Planet. Because that's what uniquely identifies are row.

A person's name as well as their gender are each non-key attributes. They both
are also functional dependent on the primary key. But don't depend on the FULL
primary key, but only part thereof. Name and gender only depend on the
PersonID, so to say. The Home Planet doesn't influence either. As such, this
table violate the Second Normal Form.

We can solve this violation, though:

======== ===== ======
PersonID Name  Gender
======== ===== ======
1        Padmé Female
2        Luke  Male
3        Leia  Female
======== ===== ======

======== ===========
PersonID Planet name
======== ===========
1        Naboo
2        Tatooine
3        Alderaan
3        Naboo
======== ===========

If we move the Planet Name into its own table and only reference the PersonID,
we comply with the Second Normal Form. So far so good.

But now we want to extend our table of planet names. We want to add the planet
Dagobah to our list. However, trying to do so will give us some trouble if we
don't have at least one person in our person table that is considering that
planet their home planet. If we were to insert Dagobah into our planet table we
couldn't. There's no person in our person table that would have Dagobah as
their home planet:

======== ===========
PersonID Planet name
======== ===========
1        Naboo
2        Tatooine
3        Alderaan
3        Naboo
**???**  Dagobah
======== ===========

While this might not be an issue for fixed-data scenarios, it certainly is an
issue in most situations these days.

There's also another problem you might have already thought of: when we have
trouble inserting data, we might as well have issues deleting it. And you're
right there.

Deletion Anomalies can happen as well. If we were to delete Luke from our
persons table, then Tatooine wouldn't have a person anymore that it belongs to.
We'd thus need to delete that planet from the planet table as well:

======== ===== ======
PersonID Name  Gender
======== ===== ======
1        Padmé Female
3        Leia  Female
======== ===== ======

======== ===========
PersonID Planet name
======== ===========
1        Naboo
**???**  Tatooine
3        Alderaan
3        Naboo
======== ===========

That's kind of unfortunate, isn't it? Let's remedy this issue. You may already
guess, when there is a First and Second Normal Form there probably is a *Third
Normal Form* as well.

Third Normal Form
=================

And you're right about that! Like the previous two, the *Third Normal Form* or
*3NF* was defined by Edgar Codd in 1971. Simply put, in addition to the
criteria for from the First and Second Normal Forms, it requires that all
non-key attributes are dependent on the primary key, and only the primary key.

Looking at our table schema now, we have the person table with the primary key
PersonID. Name and gender only depend on the PersonID. We could have more
persons with the same name and different genders:

======== ===== ======
PersonID Name  Gender
======== ===== ======
1        Padmé Female
2        Luke  Male
3        Leia  Female
======== ===== ======

Likewise for the planets, although multiple planets with the same name are
somewhat unrealistic. The name and the amount of surface water only depend on
the PlanetID primary key:

======== ===========
PersonID Planet name
======== ===========
1        Naboo
**???**  Tatooine
3        Alderaan
3        Naboo
======== ===========

New to the party here is the table combining PersonID and PlanetID. Those two
fields also represent the table's primary key. The table represents the m-to-n
relationships between persons and planets. Thus preventing insert and deletion
anomalies:

======== ========
PersonID PlanetID
======== ========
1        10
2        11
3        10
3        12
======== ========

.. tip::

   Database normalization is great!

A normalized database can solves the issues of insert, update and deletion
anomalies I pointed out. But should you always normalize your database? Is a
fully normalized database always a good idea?

Another Example
===============

Let's have a look at another example, a wiki. Imagine a simple wiki with pages
where each page can have an arbitrary number of revisions. From a relational
database perspective this could look a bit like this:

Page
----

* **PageID**
* Name
* Slug

Revision
--------

* **RevisionID**
* PageID
* Text
* Date

On the one hand side we have a Page object that identifies a single page. A
page has a unique ID that we use internally to refer to it. A page also has a
name attribute we use for displaying. And there is a slug attribute that also
uniquely identifies a page object, very much like the PageID, but it is "human
readable" and may change together with the name.

On the other side there is a Revision object. That object is used to store
different versions of the text of a wiki page. The date attribute identifies
when the revision was created. As such, the revision object with the newest
date for a page represents the last revision.

Given that schema I would want 2 tasks to be solved:

1. Task 1: Fetch a single page and its current revision
2. Task 2: Fetch all page titles and the date of their current revision

As the first task I want to fetch a single page and the corresponding last or
current revision. This is a quite common scenario. A user navigates to your
wiki and you want to show the recent version of a particular page. How do you
do that given the database structure I just showed?

The second task is somewhat less common but still useful; fetch all page titles
and the date of their current or last revision. This could happen when a user
opens your wiki's sitemap or your index and you want to list all pages with
their last revision data.

Well, for the first task, this is probably the simplest SQL query you could
find that works across different databases. Using common table expressions or
window functions if you are on PostgreSQL could be beneficial. But this is a
pure SQL standard:

.. code-block:: sql

   SELECT
     *
   FROM page
   INNER JOIN revision
     ON
       page.page_id = revision.page_id
   WHERE
     page.slug = 'some-slug'
   ORDER BY
     revision.date DESC
   LIMIT 1;

You filter for the slug of the page, join your page and revision tables on the
page id, sort by the revision date in descending order, and select the top 1
result.

Similarly for the second task we are fetching all pages with their most recent
revision date. Adhering to what pretty much all relational databases
understand:

.. code-block:: sql

   SELECT
     page.name, last_revs.date
   FROM page
   INNER JOIN (
     SELECT
       revision.page_id, MAX(revision.date) date
     FROM revision
     GROUP BY
       revision.page_id
   ) last_revs
     ON
       page.page_id = last_revs.page_id;

We're selecting the maximum revision date and corresponding page id for each
page from the revisions table, join the result with the pages on the page id,
and return the page's name and last revision date.

Now with those two queries, let's look at some numbers and statistics.

Benchmarking
============

These scientifically absolutely unproven tests ran on an Intel i7, 8GB RAM and
PostgreSQL 9.6.5. The database contained 10 thousand pages and 6 million
revisions in total. Randomly created with an overall average distribution.

For my "benchmark" I ran the first query with 10 concurrent connections. Each
connection fetched a fixed random subset of 1000 pages. Each page was fetched
10 times in a row. That comes down to a total of 100 thousand queries.

The second task I decided to just run the same query 10 times to get an idea of
the timing. The second query is also not dependent on a particular page but on
the full table.

For the first task, on average, the first call for a page took almost 20
milliseconds, whereas the subsequent calls were about 2.5 to 3 milliseconds.
That's easily explainable by cache hits for subsequent calls.

For the second task the query run time varied from about 3.5 to 7 seconds.
There also wasn't any useful caching happening. The cache misses are certainly
something one can look at in details, but that's beyond the talk and this post.

What I instead want to do is, restructure and denormalize the database
structure a bit.

Denormalizing our Database
==========================

The only change compared to the previous schema is the added LastRevision
column on a page which references, as you might have guessed, to the currently
active revision for a page.

Page
----

* **PageID**
* Name
* Slug
* *LastRevision*

Revision
--------

* **RevisionID**
* PageID
* Text
* Date

Obviously, our SQL will have to change.

Instead of doing ordering in descending order by date and then limiting the
result set to a single record, we can now directly access to last revision:

.. code-block:: sql

   SELECT
     *
   FROM page
   INNER JOIN revision
     ON
       page.last_revision_id = revision.revision_id
   WHERE
     page.slug = 'some-slug';

For the second task we don't need any subquery anymore which will make the
query significantly more efficient:

.. code-block:: sql

   SELECT
     page.name, revision.date
   FROM page
   INNER JOIN revision
     ON
       page.last_revision_id = revision.revision_id;

The picture the numbers for the first task draw looks quite similar. Except
that the query time for the first call went from 20 milliseconds to just above
0.3 milliseconds. That is about two orders of magnitude faster for the first
call.

The picture for the second task, though, is something I really like. Not only
dropped the absolute query time for all calls, but subsequent calls of the same
query heavily hit the cache.

While the average query time was around 6 seconds before, using the
denormalized schema the query run time is about a 10th of that for the first
call. Subsequent queries are about 200 times faster than the original average.

Conclusion
==========

I guess what I want to show, normalizing your database is a good idea to
prevent anomalies. It's also a good idea to prevent data duplication and to
keep your data consistent.

But what I also want to show you, there's a time at which you should rethink
your database design and may denormalize your database a bit. The important
part is that you don't start with that right in the beginning when you setup
your project. You will not know how your project evolves and denormalization
adds another layer of complexity. When you know your project, and when your
database reaches a certain size, I suggest you look at the single bottleneck at
a time.

Check what's important for your users. And start there to optimize. But only go
as far with denormalization as you feel comfortable. Because every layer of
denormalization you add, needs to be maintained.

Resources
=========

* `Slides <https://speakerdeck.com/markush/thoughts-about-normal-and-abnormal-data-pycon-uk-2017>`_
