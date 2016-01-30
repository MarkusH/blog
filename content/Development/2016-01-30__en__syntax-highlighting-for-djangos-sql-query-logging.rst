==================================================
Syntax highlighting for Django's SQL query logging
==================================================

:tags: Database, Django, Logging, SQL
:author: Markus Holtermann
:image: django-logo.png
:summary: Django provides a logger for all SQL queries you run and adds syntax
   highlighting to the console output.


Let's start at the beginning: `Python's logging module`_ is hard to understand.
And it's not much easier to configure it the way that you want it to behave.
There are ``filters``, ``formatters``, ``handlers``, ``loggers``, to only name
a few components.

``filters``
   Provide a fine-grained way to suppress or allow a log record to be send to
   ``handlers``.

``formatters``
   Given a formatting string and a log record, they generate the string that is
   actually logged.

``handlers``
   Define how a log record is handled. This could be an output to the console
   or sending an email.

``loggers``
   Tell the origin of a message on a higher level (stack, file, line number,
   etc is derived automatically).

This is a simple logging example:

.. code-block:: python

   import logging

   logger = logging.getLogger('primes.finder')
   logger.debug('Next prime after %s is %s', 97, 101)

The logger effectively has the name ``'primes.finder'`` and will be referred to
by that name in Django's ``LOGGING`` configuration. Potentially defined filters
on a logger or handler would be consulted before a message is passed to a
handler from the logger. Such a filter could e.g. inspect the two primes and
see if the second has more digits than the first.

A handler takes care of outputting a log record. It could e.g. output the log
message on a command line or send it via email. In the former case a formatter
would be used to define a general format of the log messages, e.g. prepend a
timestamp and log level.

In order to provide syntax highlighting for the SQL queries Django runs we will
need to write our own formatter. To do that, we need to look at the way Django
logs the queries (``django.db.backends.utils.CursorDebugWrapper.execute()``):

.. code-block:: python

   logger.debug(
       '(%.3f) %s; args=%s' % (duration, sql, params),
       extra={
           'duration': duration,
           'sql': sql,
           'params': params,
       }
   )

What we can see here is the ``record`` object that our the formatter will
receive has the attributes ``duration``, ``sql`` and ``params``, derived from
the ``extra`` keyword argument.

.. code-block:: python

   class SQLFormatter(logging.Formatter):
       def format(self, record):
           # Check if Pygments is available for coloring
           try:
               import pygments
               from pygments.lexers import SqlLexer
               from pygments.formatters import TerminalTrueColorFormatter
           except ImportError:
               pygments = None

           # Check f sqlparse is available for indentation
           try:
               import sqlparse
           except ImportError:
               sqlparse = None

           # Remove leading and trailing whitespaces
           sql = record.sql.strip()

           if sqlparse:
               # Indent the SQL query
               sql = sqlparse.format(sql, reindent=True)

           if pygments:
               # Highlight the SQL query
               sql = pygments.highlight(
                   sql,
                   SqlLexer(),
                   TerminalTrueColorFormatter(style='monokai')
               )

           # Set the record's message to the formatted query
           record.message = sql
           return super(SQLFormatter, self).format(record)

Update your ``LOGGING`` configuration to include the ``sql`` formatter, ``sql``
handler and ``django.db.backends`` logger:

.. code-block:: python

   LOGGING = {
       'version': 1,
       'disable_existing_loggers': False,
       'formatters': {
           'sql': {
               '()': 'path.to.your.SQLFormatter',
               'format': '[%(duration).3f] %(message)s',
           }
       },
       'handlers': {
           'console': {
               'level': 'DEBUG',
               'class': 'logging.StreamHandler',
           },
           'sql': {
               'class': 'logging.StreamHandler',
               'formatter': 'sql',
               'level': 'DEBUG',
           },
       },
       'loggers': {
           'django.db.backends': {
               'handlers': ['sql'],
               'level': 'DEBUG',
               'propagate': False,
           },
           'django.db.backends.schema': {
               'handlers': ['console'],
               'level': 'DEBUG',
               'propagate': False,
           },
       }
   }


.. _Python's logging module: https://docs.python.org/3/library/logging.html
