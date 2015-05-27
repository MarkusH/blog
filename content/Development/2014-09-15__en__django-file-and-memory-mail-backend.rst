==============================================
Django file and memory mail back-end for tests
==============================================

:tags: Django, Testing
:author: Markus Holtermann
:image: django-logo.png
:summary: Whenever you write unit or integration tests for your Django
    application that involves sending mails, you end up with the LocMem mail
    back-end as a default set by Django during test setup. However, if you want
    to have a look at all the mails that have been sent, you are probably going
    to choose the File mail back-end.


Whenever you write unit or integration tests for your Django application that
involves sending mails, you end up with the ``LocMem`` mail back-end
(``django.core.mail.backends.console .EmailBackend``) as a default set by
Django during test setup. However, if you want to have a look at all the mails
that have been sent, you are probably going to choose the ``File`` mail
back-end (``django.core.mail.backends.filebased.EmailBackend``) [`docs
<https://docs.djangoproject.com/en/1.7/topics/email/#email-backends>`__].

The former give you the possibility to check for the amount of mails that have
been sent and inspect them further through ``django.core.mail.outbox``, the
latter stores all mails in a text file for later inspection.

So, if you are using the ``LocMem`` back-end and want to inspect all mails
after an entire test run, you are first trying to change the back-end with
``@override_settings`` [`docs <https://docs.djangoproject.com/en/dev/topics/testing/tools/#django.test.override_settings>`__]. This works as long as you don't use
``django.core.mail.outbox``, because this will always be ``None`` or ``[]``.
How are you going to make that work?

When this question came up on the Django IRC channel I'll came up with

.. code-block:: python

    import django
    from django.core import mail
    from django.core.mail.backends.filebased import EmailBackend as FileEmailBackend


    class EmailBackend(FileEmailBackend):
        def __init__(self, *args, **kwargs):
            super(EmailBackend, self).__init__(*args, **kwargs)
            if not hasattr(mail, 'outbox'):
                mail.outbox = []

        def write_message(self, message):
            if django.VERSION[:2] > (1, 5):
                super(EmailBackend, self).write_message(message)
                mail.outbox.append(message)

        def send_messages(self, messages):
            ret = super(EmailBackend, self).send_messages(messages)
            if django.VERSION[:2] < (1, 6):
                mail.outbox.extend(messages)
            return ret


I didn't test the code myself, but the user asking for support seemed to find
it a working solution.
