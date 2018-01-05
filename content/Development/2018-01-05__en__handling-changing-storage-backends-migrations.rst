================================================
Handling Changing Storage Backends In Migrations
================================================

:tags: Django, Migration
:author: Markus Holtermann
:image: django-logo.png
:summary: Migrations serialize everything, even the storage backend. When you
   have different backends during development and production, how do you cope
   with that?
:status: draft


First off, you should know that the Django migration framework attempts to
freeze *everything* that belongs to a model. Not just the field names and
types, but also the arguments one provides in the model class definition. This
is by design and intended behavior. This allows you to do pretty much anything
and everything in a `RunPython operation
<https://docs.djangoproject.com/en/dev/ref/migration-operations/#runpython>`_.

The First Approach
==================

Now, let's look at the issue or behavior at hand. Let's set the following
scenario: during development, you use your local file system to store media
data. In your ``settings.py`` you have

.. code-block:: python

    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'

You model will look a bit like this:

.. code-block:: python

    from django.conf import settings
    from django.db import models

    class UserProfile(models.Model):
        user = models.ForeignKey(settings.AUTH_USER_MODEL)
        avatar = models.ImageField(upload_to='avatars')

This will eventually put user uploaded images into
``$BASE_DIR/media/avatars/``. Furthermore, the avatars will be available
through http://127.0.0.1:8000/media/avatars/some-image.png. The migration
adding the ``avatar`` field will look a bit like this:

.. code-block:: python

    from django.db import migrations, models

    class Migration(migrations.Migration):
        dependencies = [
            ("myapp", "0001_initial"),
        ]
        operations = [
            migrations.AddField(
                model_name='userprofile',
                name='avatar',
                field=models.ImageField(upload_to='avatars'),
            ),
        ]

Let's take the next step. You're about to release your website to production.
It doesn't really matter where you deploy and what service you use. But you
decide to use AWS S3 for serving the media file. Great! You browse the Django
documentation and find `DEFAULT_FILE_STORAGE
<https://docs.djangoproject.com/en/2.0/ref/settings/#default-file-storage>`_.
You now only need to change ``DEFAULT_FILE_STORAGE`` to something that can deal
with S3 and you're done. With a bit of research you find `django-storages
<https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html>`_ by
`Josh Schneier <https://github.com/jschneier>`_ and update your `settings.py`:

.. code-block:: python

    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

All is well. You configured the ``DEFAULT_FILE_STORAGE``, a bunch of ``AWS_*``
settings. Everything works.

Your Project Grows
==================

Your project grows, and you are about to introduce a new feature. While the
avatars were publicly readable you now need a way to upload images that are
only visible to an individual user. To further improve the security and not
accidentally publish those files, you decide to use another S3 bucket. That's
where you get stuck. How are you supposed to configure different buckets when
you only have the ``DEFAULT_FILE_STORAGE`` setting available? You find the
`storage <https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FileField.storage>`_
attribute on the ``FileField``. You set the attribute to the
``storages.backends.s3boto3.S3Boto3Storage`` class you're already using on
production:

.. code-block:: python

    from django.conf import settings
    from django.db import models

    from storages.backends.s3boto3 import S3Boto3Storage

    class Invoice(models.Model):
        user = models.ForeignKey(settings.AUTH_USER_MODEL)
        pdf = models.FileField(upload_to='invoices', storage=S3Boto3Storage())

You're starting up the development server using ``manage.py runserver`` and try
to upload files to test the new invoicing system. But the PDF files are not
created. You can't see them in ``$BASE_DIR/media/invoices/``. What is going on?
The next moment the scales fall from your eyes. You just configured the upload
to be to AWS S3. But you don't want that. You want that to be the local
filesystem during development times and S3 on production. How do you do this?
Each time you change the value of storage to one or the other, Django complains
that there are changes in models that have not been reflected in migrations.

This is where it get's interesting. At `LaterPay <https://www.laterpay.net/>`_
we have data that is publicly readable, such as our customer's logos, but we
also have data that we don't want anybody to see except for the rightful owner,
such as invoices. We have exactly the problem described above. How did we solve
it? Here's the code for the a wrapping storage class that we use:

.. code-block:: python

    from importlib import import_module

    from django.conf import settings

    class GenericStorage(object):

        def __init__(self, storage_class, storage_settings):
            self.storage_class = storage_class
            self.storage_settings = storage_settings

        def __getattr__(self, name):
            return getattr(self._storage, name)

        def __call__(self):
            storage_class = getattr(settings, self.storage_class)
            storage_settings = getattr(settings, self.storage_settings)
            self._storage_class = self._import(storage_class)
            self._storage = self._storage_class(**storage_settings)
            return self

        def _import(self, storage_class):
            module_name, attr_name = storage_class.rsplit('.', 1)
            module = import_module(module_name)
            try:
                return getattr(module, attr_name)
            except AttributeError:
                raise ImportError("Couldn't import %s from %s" % (attr_name, module_name))

        def deconstruct(self):
            module_name = self.__module__
            name = self.__class__.__name__
            return (
                '%s.%s' % (module_name, name),
                (self.storage_class, self.storage_settings),
                {},
            )

    InvoiceStorage = GenericStorage('INVOICE_STORAGE_CLASS', 'INVOICE_STORAGE_SETTINGS')
    LogoStorage = GenericStorage('LOGO_STORAGE_CLASS', 'LOGO_STORAGE_SETTINGS')

The name ``GenericStorage`` is deliberate. It acts as a proxy for an arbitrary
storage backend. You can configure the underlying storage backend as well as
the ``__init__()`` arguments for that backend. You do that through a set of 2
settings variables. But instead of passing the *value* of those settings
variables to ``GenericStorage`` you pass the *name* of these settings
variables. ``GenericStorage`` will take care of retrieving the value from the
settings.

The ``settings.py`` file can then look a bit like this:

.. code-block:: python

    if PRODUCTION:
        INVOICE_STORAGE_CLASS = 'storages.backends.s3boto3.S3Boto3Storage'
        INVOICE_STORAGE_SETTINGS = {
            'bucket_name': 'invoices-bucket',
            'region_name': 'eu-central-1',
        }
        LOGO_STORAGE_CLASS = 'storages.backends.s3boto3.S3Boto3Storage'
        LOGO_STORAGE_SETTINGS = {
            'bucket_name': 'logos-bucket',
            'region_name': 'eu-central-1',
        }
    else:
        INVOICE_STORAGE_CLASS = 'django.core.files.storage.FileSystemStorage'
        INVOICE_STORAGE_SETTINGS = {'location': 'invoices'}
        LOGO_STORAGE_CLASS = 'django.core.files.storage.FileSystemStorage'
        LOGO_STORAGE_SETTINGS = {'location': 'logos'}

In the models we then use the storage backends like this:

.. code-block:: python

    from django.conf import settings
    from django.db import models

    from .utils.storages import InvoiceStorage, LogoStorage

    class Invoice(models.Model):
        user = models.ForeignKey(settings.AUTH_USER_MODEL)
        pdf = models.FileField(storage=InvoiceStorage())


    class Logo(models.Model):
        merchant = models.ForeignKey('Merchant')
        image = models.ImageField(storage=LogoStorage())

Pros & Cons
===========

This approach has some pros and cons. The major downside for us is the number
of variables we need to configure all our different storages. I won't say how
many, but it's more than 2 storages we have 😉. Furthermore, we retrieve the
value of the ``*_STORAGE_CLASS`` and ``*STORAGE_SETTINGS`` from environment
variables, following the `12 Factor <https://12factor.net/>`_ approach. And as
we've learned, Elastic Beanstalk has a hard limit of 4096 bytes for environment
variables.

Definitively on the plus side is the sheer unlimited configurability. You can
migrate storage by storage from one cloud provider to another or change from
``boto`` to ``boto3`` one storage backend at a time.

Another Approach
================

Another approach that descends from the above `was written up
<https://github.com/fission6/django-generic-storage>`_ by `fission6
<https://github.com/fission6>`_. It combines the idea of wrapping "the real
storage" but only refers to the storage by a unique identifier, much like the
`CACHES <https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-CACHES>`_
settings variable.
