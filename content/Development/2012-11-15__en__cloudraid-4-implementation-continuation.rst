============================================
[CloudRAID] 4. Implementation (Continuation)
============================================

:tags: Apache, CloudRAID, Cluster, Eclipse, Encryption, Java, Security, Server,
   Studium
:author: Markus Holtermann
:summary: This post is a continuation of the blog series about the student
   research paper CloudRAID. It features the API implementation.


This post is a continuation of the blog series about the student research paper
`CloudRAID`_.


4. Implementation
=================


4.2. RESTful API Endpoint Specifications
----------------------------------------


4.2.1. URL Mapping for API Endpoints
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The default ``CloudRAID`` package contains a RESTful HTTP API. This is realized
using *Java Servlets*. A Java web and application server will be used to deploy
the servlet. To activate the servlet this is bound to a base path that will be
required to be prefixed to the *Uniform Resource Locator* (URL) path. The
actual functionality provided by this servlet will then be bound to sub paths
as described in chapters 4.2.2 to 4.2.4 (see below). The basic concept of how
the mapping between the sub paths and URL parameters is done, has been taken
from the `Django`_ `URL dispatcher`_.

The complete pattern and mapping implementation is done in the class
``RestApiUrlMapping`` within the package 
``de.dhbw_mannheim.cloudraid.api.impl`` and is part of the ``CloudRAID``-REST
bundle. The ``RestApiUrlMapping`` constructor takes two to four parameter of
various type as one can see in listing 9 below:

#. The first parameter must be the pattern that needs to be matched. This can
   either be a ``java.lang.String`` or a regular expression pattern of type
   ``java.util.regex.Pattern``. If a ``String`` is passed, this is converted to
   a ``Pattern`` and hence must be a correct regular expression. Otherwise a
   ``IllegalArgumentException`` will be thrown.
#. The second, optional, parameter can be used to restrict a mapping to a
   specific HTTP request method. This allows a developer to have different
   callback functions for the same URL path, depending on the HTTP method.
#. The remaining parameters define the callback function which is called if the
   URL matches a HTTP request. This can either be a single parameter of type
   ``java.lang.reflect.Method`` or two parameters whereof the first must be of
   type ``Class<?>`` and the second of type ``java.lang.String``. In the latter
   case, the static function ``findFunction()`` will be used to resolve both
   parameters to a ``Method``. If the (resolved) method is null, this will
   result in a ``IllegalArgumentException``. If the method needs to be
   resolved, any failure will raise as ``NoSuchMethodException`` or
   ``SecurityException``.

.. code-block:: java

    package de.dhbw_mannheim.cloudraid.api.impl;

    public class RestApiUrlMapping {
      public static Method findFunction(Class<?> klass,
        String function);

      public RestApiUrlMapping(Pattern pattern, Class<?> klass,
        String function);
      public RestApiUrlMapping(Pattern pattern, Method function);
      public RestApiUrlMapping(Pattern pattern, String method,
        Class<?> klass, String function);
      public RestApiUrlMapping(Pattern pattern, String method,
        Method function);
      public RestApiUrlMapping(String pattern, Class<?> klass,
        String function);
      public RestApiUrlMapping(String pattern, Method function);
      public RestApiUrlMapping(String pattern, String method,
        Class<?> klass, String function);
      public RestApiUrlMapping(String pattern, String method,
        Method function);
    }

*Listing 9: The URL mapping API*

The actual mapping will be initialized in the constructor of the
``RestApiServlet`` as shown in the listing 10. The shipped REST API uses only
the ``RestApiUrlMapping`` constructor defined in lines 17 and 18 of listing 9
because of its simplicity. But one can use this class to extend the API with
own functions. Hence the other constructors are still in the code and will not
be removed.

.. code-block:: java

    package de.dhbw_mannheim.cloudraid.api.impl;

    public class RestApiServlet extends HttpServlet {
      private static ArrayList<RestApiUrlMapping> mappings =
        new ArrayList<RestApiUrlMapping>();

      public RestApiServlet() {
        RestApiServlet.mappings.add(new RestApiUrlMapping(
          "^/api/info/$", "GET", RestApiServlet.class,
          "apiInfo"));
        RestApiServlet.mappings.add(new RestApiUrlMapping(
          "^/file/([^/]+)/$", "DELETE", RestApiServlet.class,
          "fileDelete"));
        // Similar for other URL sub paths
      }
    }

*Listing 10: The URL mapping initialization*

On each request to the ``RestApiServlet`` the list of available mappings will
be checked for a matching mapping with the path information of the current
request and its HTTP method. If a valid mapping exists, the regarding callback
function will be executed. This callback function must accept exactly three
arguments:

#. ``javax.servlet.http.HttpServletRequest req``: The current request. This
   variable will contain session information, the HTTP headers and allows to
   access the request body.
#. ``de.dhbw_mannheim.cloudraid.api.responses.IRestApiResponse resp``: The
   response object that will be returned to the client. It will contain a HTTP
   response code as defined by the specifications in the following chapters and
   a payload, depending on the request.
#. ``java.util.ArrayList<String> args``: The URL patterns may contain matching
   groups, enclosed by ``(`` and ``)``. The content of each matching group will
   be added to this parameter and is therefore available to the callback
   function. The *Create, Read, Update, Delete* (CRUD) endpoints as defined in
   chapter *4.2.3 – File Related Function* make use of a single matching group
   that contains the file name of the uploaded file.[/olist]


4.2.2. Version Information
~~~~~~~~~~~~~~~~~~~~~~~~~~

The RESTful API already supports many features. But since the API might change
someday, some kind of versioning is needed to tell the client side, which
features are supported. This information, along with the version information of
the *Core-*, *Metadata-* and *Configuration-Services* and the currently running
RAID version and the versions of the activated storage connectors is provided
via this URL.

+--------------+--------------------------------------------------------------+
|Method:       |``GET``                                                       |
+--------------+--------------------------------------------------------------+
|Endpoint:     |``/api/info/``                                                |
+--------------+--------------------------------------------------------------+
|Description:  |Displays the version and author/vendor information about      |
|              |various service components, such as the Core service, the     |
|              |cloud storage connectors, the configuration, etc.             |
+--------------+--------------------------------------------------------------+
|Usage:        |Used on client site to verify that the client is able to      |
|              |handle the provided API.                                      |
+--------------+--------------------------------------------------------------+
|HTTP Response:|* 200 – Success – No special meaning in this response         |
+--------------+--------------------------------------------------------------+

*RESTful API: API and service information*


.. code-block:: code

    HTTP/1.1 200 OK
    X-Powered-By: CloudRAID/0.2
    Content-Type: text/plain; charset=utf-8
    Transfer-Encoding: chunked
    Server: Jetty(6.1.x)

    Core-Service:CloudRAID-Core v0.0.1.prealpha by cloudraid
    RAID-Version:CloudRAID-RAID5 v0.0.2prealpha by cloudraid
    Metadata-Service:CloudRAID-Metadata v0.0.1.prealpha by cloudraid
    Configuration-Service:CloudRAID-Config v0.0.1.prealpha by cloudraid
    API-Service:CloudRAID-RESTful v0.0.1.prealpha by cloudraid
    Storage-Connector-0:CloudRAID-Dropbox v0.0.1.prealpha by cloudraid
    Storage-Connector-1:CloudRAID-AmazonS3 v0.0.1.prealpha by cloudraid
    Storage-Connector-2:CloudRAID-UbuntuOne v0.0.1.prealpha by cloudraid
    API-Version:0.2

*Listing 11: Example HTTP response: header elements and body*


4.2.3. File Related Function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All CRUD functions are provided by the following four URLs. The endpoint for
all of them is ``/file/([^/]+)/``. Based on the HTTP method, a file is either
being created, downloaded, removed or updated.

The *Create* and *Update* endpoints have to handle a huge amount of data.
Therefore they use the ``POST`` and ``PUT`` methods respectively. In both cases
the file will be trans- mitted synchronously to the ``CloudRAID`` service. All
ongoing steps are going to be asynchronous. They do not influence the HTTP
response to the upload.

On the other hand, the *Delete* and *Download* functions are completely
synchronous.  They use the ``DELETE`` and ``GET`` HTTP methods. The cloud
storage connectors will trigger the deletion or get request to the cloud
storage providers and are blocking up to their response or until the regarding
network protocol throws a timeout error. From that follows, that a failure to
the "outbound" connections from the ``CloudRAID`` service may block a client
application, or at least the thread the connection runs in, for some time.

+--------------+--------------------------------------------------------------+
|Method:       |``DELETE``                                                    |
+--------------+--------------------------------------------------------------+
|Endpoint:     |``/file/([^/]+)/``                                            |
+--------------+--------------------------------------------------------------+
|Description:  |Calls on this endpoint will trigger a synchronous deletion of |
|              |the given file from the cloud storage connectors.             |
+--------------+--------------------------------------------------------------+
|Parameter:    |* Cookie: ``JSESSIONID=VALUE``                                |
+--------------+--------------------------------------------------------------+
|HTTP Response:|* 200 – File has been deleted or does not even exist          |
|              |* 401 – The requesting user is not logged in                  |
|              |* 404 – File cannot be found in the meta data manager         |
|              |* 405 – The session identifier has not been transferred via   |
|              |  cookie                                                      |
|              |* 500 – An error occurred during deleting the file            |
|              |* 503 – The session given by the identifier does not exist    |
+--------------+--------------------------------------------------------------+

*RESTful API: file deletion*


+--------------+--------------------------------------------------------------+
|Method:       |``GET``                                                       |
+--------------+--------------------------------------------------------------+
|Endpoint:     |``/file/([^/]+)/``                                            |
+--------------+--------------------------------------------------------------+
|Description:  |Calls on this endpoint will trigger a synchronous download of |
|              |the requested file from the cloud storage, a merge to the     |
|              |original file and download to the client.                     |
+--------------+--------------------------------------------------------------+
|Parameter:    |* Cookie: ``JSESSIONID=VALUE``                                |
+--------------+--------------------------------------------------------------+
|HTTP Response:|* 200 – File has been downloaded                              |
|              |* 401 – The requesting user is not logged in                  |
|              |* 404 – File cannot be found in the meta data manager         |
|              |* 405 – The session identifier has not been transferred via   |
|              |  cookie                                                      |
|              |* 500 – An error occurred during downloading the file         |
|              |* 503 – The session given by the identifier does not exist    |
+--------------+--------------------------------------------------------------+

*RESTful API: file download*


+--------------+--------------------------------------------------------------+
|Method:       |``POST``                                                      |
+--------------+--------------------------------------------------------------+
|Endpoint:     |``/file/([^/]+)/``                                            |
+--------------+--------------------------------------------------------------+
|Description:  |Calls on this endpoint will trigger a synchronous upload of   |
|              |the *new* file. A successful upload of the file will split and|
|              |push it to the cloud storage providers asynchronously.        |
+--------------+--------------------------------------------------------------+
|Parameter:    |* Cookie: ``JSESSIONID=VALUE``                                |
+--------------+--------------------------------------------------------------+
|HTTP Response:|* 201 – File has been uploaded                                |
|              |* 401 – The requesting user is not logged in                  |
|              |* 405 – The session identifier has not been transferred via   |
|              |  cookie                                                      |
|              |* 409 – File already exists                                   |
|              |* 411 – No content length specified                           |
|              |* 500 – An error occurred while storing the new file          |
|              |* 503 – The session given by the identifier does not exist    |
+--------------+--------------------------------------------------------------+

*RESTful API: file upload of a new file*


+--------------+--------------------------------------------------------------+
|Method:       |``PUT``                                                       |
+--------------+--------------------------------------------------------------+
|Endpoint:     |``/file/([^/]+)/``                                            |
+--------------+--------------------------------------------------------------+
|Description:  |Calls on this endpoint will trigger a synchronous upload of   |
|              |the *existing* file. A successful upload of the file will     |
|              |split and push it to the cloud storage providers              |
|              |asynchronously.                                               |
+--------------+--------------------------------------------------------------+
|Parameter:    |* Cookie: ``JSESSIONID=VALUE``                                |
+--------------+--------------------------------------------------------------+
|HTTP Response:|* 201 – File has been uploaded                                |
|              |* 401 – The requesting user is not logged in                  |
|              |* 404 – File cannot be found                                  |
|              |* 405 – The session identifier has not been transferred via   |
|              |  cookie                                                      |
|              |* 411 – No content length specified                           |
|              |* 500 – An error occurred while storing the new file          |
|              |* 503 – The session given by the identifier does not exist    |
+--------------+--------------------------------------------------------------+

*RESTful API: file upload of an existing file*


While using a client application, the user needs to know, which files exist and
can be downloaded and, if the system is under heavy usage, what the states of
the uploads are. The following URL shows all files a user has access to and
displays those information.

+--------------+--------------------------------------------------------------+
|Method:       |``GET``                                                       |
+--------------+--------------------------------------------------------------+
|Endpoint:     |``/list/``                                                    |
+--------------+--------------------------------------------------------------+
|Description:  |Calls on this endpoint will return a list of all files the    |
|              |current user has access to.                                   |
+--------------+--------------------------------------------------------------+
|Parameter:    |* Cookie: ``JSESSIONID=VALUE``                                |
+--------------+--------------------------------------------------------------+
|HTTP Response:|* 200 – Success – No special meaning in this response         |
|              |* 401 – The requesting user is not logged in                  |
|              |* 405 – The session identifier has not been transferred via   |
|              |  cookie                                                      |
|              |* 500 – An error occurred while storing the new file          |
|              |* 503 – The session given by the identifier does not exist    |
+--------------+--------------------------------------------------------------+

*RESTful API: list all accessible file*


4.2.4. User Related Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All connections, except the API version request, need some kind of
authorization or provide and initiate it. The authentication is done on user
base. The creation, authentication and de-authentication (logout) is performed
on the */user/* endpoint namespace. Besides that, a user is able to change the
login password, while user deletion requests are not allowed. This is basically
due to the fact, that a deletion should trigger a deletion of all files
belonging to the user from the cloud storage providers. But since this step is
non-reversible and a full data loss will be the consequence, the decision to
*not* implement this function has been made.

+--------------+--------------------------------------------------------------+
|Method:       |``POST``                                                      |
+--------------+--------------------------------------------------------------+
|Endpoint:     |``/user/add/``                                                |
+--------------+--------------------------------------------------------------+
|Description:  |Calling this endpoint will add a new user to the system.      |
+--------------+--------------------------------------------------------------+
|Parameter:    |* X-Username: ``USERNAME``                                    |
|              |* X-Password: ``PASSWORD``                                    |
|              |* X-Confirm: ``CONFIRMATION``                                 |
+--------------+--------------------------------------------------------------+
|HTTP Response:|* 200 – Success – No special meaning in this response         |
|              |* 400 – The user name is invalid or missing or the password   |
|              |  and its confirmation are missing or do not match            |
|              |* 406 – The user is already logged in                         |
|              |* 500 – An error occurred while retrieving the list           |
+--------------+--------------------------------------------------------------+

*RESTful API: add new user*


+--------------+--------------------------------------------------------------+
|Method:       |``POST``                                                      |
+--------------+--------------------------------------------------------------+
|Endpoint:     |``/user/auth/``                                               |
+--------------+--------------------------------------------------------------+
|Description:  |This endpoint will be used to authenticate the requesting     |
|              |user.                                                         |
+--------------+--------------------------------------------------------------+
|Parameter:    |* X-Username: ``USERNAME``                                    |
|              |* X-Password: ``PASSWORD``                                    |
+--------------+--------------------------------------------------------------+
|HTTP Response:|* 202 – Success – User has been authenticated                 |
|              |* 400 – The user name is invalid or missing or the password is|
|              |  missing or invalid                                          |
|              |* 406 – The user is already logged in                         |
|              |* 503 – The session could not be created                      |
+--------------+--------------------------------------------------------------+

*RESTful API: authenticate a user*


+--------------+--------------------------------------------------------------+
|Method:       |``POST``                                                      |
+--------------+--------------------------------------------------------------+
|Endpoint:     |``/user/chgpw/``                                              |
+--------------+--------------------------------------------------------------+
|Description:  |This endpoint must be used to change a user's password.       |
+--------------+--------------------------------------------------------------+
|Parameter:    |* Cookie: ``JSESSIONID=VALUE``                                |
|              |* X-Username: ``USERNAME``                                    |
|              |* X-Password: ``PASSWORD``                                    |
|              |* X-Confirm: ``CONFIRMATION``                                 |
+--------------+--------------------------------------------------------------+
|HTTP Response:|* 200 – Success – Password has been changed                   |
|              |* 400 – The user name is invalid or missing or the password   |
|              |  and its confirmation are missing or do not match            |
|              |* 401 – The requesting user is not logged in                  |
|              |* 405 – The session identifier has not been transferred via   |
|              |  cookie                                                      |
|              |* 500 – An error occurred while updating the user record      |
|              |* 503 – The session given by the identifier does not exist    |
+--------------+--------------------------------------------------------------+

*RESTful API: change a user password*


+--------------+--------------------------------------------------------------+
|Method:       |``GET``                                                       |
+--------------+--------------------------------------------------------------+
|Endpoint:     |``/user/auth/logout/``                                        |
+--------------+--------------------------------------------------------------+
|Description:  |This endpoint must be used to log-off                         |
+--------------+--------------------------------------------------------------+
|Parameter:    |* Cookie: ``JSESSIONID=VALUE``                                |
+--------------+--------------------------------------------------------------+
|HTTP Response:|* 200 – Success – User has been logged out and session has    |
|              |  been invalidated                                            |
|              |* 401 – The requesting user is not logged in                  |
|              |* 405 – The session identifier has not been transferred via   |
|              |  cookie                                                      |
|              |* 503 – The session given by the identifier does not exist    |
+--------------+--------------------------------------------------------------+

*RESTful API: user logout*


.. _CloudRAID:
   {filename}/Development/2012-10-28__en__cloudraid-1-introduction.rst
.. _Django: https://www.djangoproject.com/
.. _URL dispatcher: https://docs.djangoproject.com/en/1.4/topics/http/urls/
