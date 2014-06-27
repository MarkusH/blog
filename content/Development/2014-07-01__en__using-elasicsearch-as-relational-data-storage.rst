==============================================
Using Elasticsearch as relational data storage
==============================================

:tags: AngularJS, Elasticsearch
:author: Alexander Grießer, Markus Holtermann
:status: draft


This lenghty blog post is about a university project Alex, a fellow student at
my university, and I have been developing in the last weeks. We are both quite
experienced software developers focussing on application or web development. As
part of a university project we had absolutely no requirements on a coding
language or styling. As the only requirement was being a web site and we both
knew absolutely nothing about on how to create single page applications, we
looked around and eventually chose `AngularJS`_.

We didn't start from scratch, though. There was a prototype from last semester
from another team we used for inspiration. The only *problem* with the project
was being written as a JavaEE application. The setup, even to make it run
locally, would be too complicated for the use case. Furthermore we both didn't
like the idea coding in Java; Alex already using Java at work and wanting to
expand his knowledge, and Markus trying to avoid Java for various reasons.


About The Project
=================

The web site should list information about all kinds of schools in Berlin. A
user should be able to filter and search for schools by different criteria. The
intention of the university course and the project is to learn about *OpenData*
and *Data Journalism*. The city of Berlin offers a `similar service`_ already,
although the user experience is just *"meh"*.

We took the data set the group acquired in the last semester and normalized it
even more. We also performed some addtional cleaning. For example if a URL was
given for a school we checked whether that URL was reachable or not and
accordingly removed those URLs that couldn't be reached.


The Underlying Data Storage
===========================

Looking at the problem from a system architects point of view clearly shows
relations between many parts. While a school has a single address it might have
multiple types, like elementary school and high school. A school probably
teaches multiple languages, not only German but English, French, Dutch or
Chineese too. Thus a relational data store / database like PostgreSQL or MySQL
would be one's first choices.

Contrary to what a system architect normally would do we chose a technology not
inteded for the given use case: a vanilla `elasticsearch`_ instance. We chose
this technology for several reasons:

* We both professionally develop software using SQL databases. Therefore it was
  unlikely that we would learn anything new while implementing such a easy
  application.
* The data set contains a lot of optional data. So there was a requirement for
  a "dynamic" data model for the schools.
* But most important: we wanted to learn something new that we could
  potentionally use in our further as developers

Import of the data
------------------

The original data source consists of several Excel documents. These were
provided by the city of Berlin and have been normalized by our fellow students
in the semester before. For easier handling we transformed those files to the
CSV format. Later these CSV files are used to import the data into the
elasticsearch instance.

Before doing this we created a data model bringing some of the features of a
realtional database into elasticsearch. Additionally this step is used to set
up and configure how elasticsearch handles the data, mainly (not) analyzing and
(not) indexing.

.. code-block:: json

    {
        "school": {
            "properties": {
                "bsn": {
                    "index": "not_analyzed", "type": "string"
                },
                "name": {
                    "index": "analyzed", "type": "string"
                },
                "phonenumber": {
                    "index": "not_analyzed", "type": "string"
                },
                "wwwaddress": {
                    "index": "no", "type": "string"
                },
                "address": {
                    "properties": {
                        "plz": {
                            "type": "integer"
                        },
                        "location": {
                            "lat_lon": true, "type": "geo_point"
                        },
                        "district": {
                            "type": "string", "index": "not_analyzed"
                        },
                        "street": {
                            "index": "analyzed", "type": "string"
                        },
                        "name": {
                            "type": "string", "index": "analyzed"
                        }
                    },
                    "type": "nested"
                }
            }
        }
    }

As you can see from the excerpt above we are using elasticsearch's `Nested
Mapping Type`_. We decided to use this type over inner objects or `Parent/Child
Types`_ for two reasons:

    [First,] each nested doc remains independent, and [one] can perform a query
    like [``address.district=Kreutzberg AND address.plz = 10999``] without a
    problem. [Second], reading is faster than the parent/child because the
    nested document is stored in the same Lucene block as the main document.
    Although writing may require reindexing the entire document, this is no
    problem for our use case as the data is imported once. [ES13]_

The actual import was done by a small Python script using `Click`_ that
connects to the elasticsearch instance creates the necessary document structure
and later imports the different data types (base data, address data, school
profiles, etc.).


The Front-End 
=============

We are no designers. But we wanted to create a webpage that is both faster and
more functional than what the original web page of the city of Berlin offers.
We did not target mobile browsers in particular but if we could support them in
a reasonable way, then we would do that. Markus is a fan of `Zurb Foundation`_,
therefore we decided to use this CSS framework as a starting point for our
layout.

Since our datastore is an elasticsearch instance we had the possibility to
retrieve data directly from the browser via JSON requests. Therefore we decided
to create a single page application and eventually chose AngularJS. We also
delved a little bit into the world of Website frontend development tooling by
using the current state of the art Bower, Grunt and Compass tooling.

Our app has three important components:

* the filter form
* a map view that shows the schools matching the current filter
* and a detail page of every school

The filter
----------

Multiselect, blablup, sharing/persistent filters? no clue 

The map
-------

The map component is responsible to display the result of a filter operation.
The map is shown using the `Openlayers`_ JavaScript library. 

The detail page
---------------

The detail page is quite straightforward. One requirement we defined for the
detail page was, that we should be able to provide a deep linking option. This
was actually quite easy to implement using the `ngRoute`_ module of AngularJS. 

The url is defined to look like this: "domain.de/#/schools/BSN". The BSN is a
unique identifier for each school in Berlin (we assume it stands for Berlin
school number). The ngRoute module allows to specify parameter captures in the
route definition, so it's very easy to access parts of the current URL in the
javascript code. The route definition for the school detail page is: 

.. code-block:: javascript

    mod.config(['$routeProvider', function ($routeProvider) {
        $routeProvider
        // ...
        .when('/schools/:schoolId', {
            templateUrl: 'views/school.html',
            controller: 'SchoolCtrl'
        })
        // ...
    }]);

Using the schools identifier we make a simple lookup in elasticsearch and get
the document for the school. Since elasticsearch returns data in JSON format we
can just set the returned value in the scope of the detail page controller, the
layout will then be automatically updated by AngularJS.


Lessons lerned
==============


Sources and additional reading
==============================

.. [ES13] Zachary Tong. Managing Relations inside Elasticsearch. February 20, 2013 http://www.elasticsearch.org/blog/managing-relations-inside-elasticsearch/

.. _AngularJS: https://angularjs.org/
.. _similar service: http://www.berlin.de/sen/bildung/schulverzeichnis_und_portraets/anwendung/
.. _elasticsearch: http://www.elasticsearch.org/
.. _Click: http://click.pocoo.org/
.. _Nested Mapping Type: http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/mapping-nested-type.html
.. _Parent/Child Types: http://www.elasticsearch.org/guide/reference/mapping/parent-field.html
.. _Zurb Foundation: http://foundation.zurb.com/
.. _Openlayers: http://www.openlayers.org/
.. _ngRoute: https://docs.angularjs.org/api/ngRoute
