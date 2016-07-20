=====================================
DjangoCon US 2016: SSL All The Things
=====================================

:tags: Apache, Django, DjangoCon, Network, Nginx, Security, Server, Talk
:author: Markus Holtermann
:image: djangoconus2016/talk-cover.jpg
:summary: Django migrations are complex. They do a lot for you but sometimes
   you need to tell 'em how to do things. There's no reason to be afraid of
   that, though.


.. image:: /images/djangoconus2016/logo.png
   :align: right
   :alt: DjangoCon 2016 -- Philadelphia
   :class: margin-left

Introduction
============

Ever since Snowden revealed that the NSA is spying on all of us the urge to
more secure systems increased. At least over in Germany and plenty other
European countries.

There's also the risk of public and unencrypted Wi-Fis. You don't want the
owner of the cafe next door or the other people sitting in the cafe be able to
wiretap your network traffic.

And some internet service providers even inject their own advertisement in
websites you access. That's scary. And a bad idea from a user's perspective.
Not to mention from a security perspective.


Disclaimer
==========

I'm not a cryptographer. All examples I give here are either to the best of my
knowledge or I've talked to skilled people I trust and asked them for their
knowledge. Which still means there can be errors as we all a humans!

This blog post will not cover everything you could possibly know about SSL and
TLS, by all means, that would be enough to fill an entire conference with
talks.

Also, SSL 2 and 3 are broken and insecure. Do not use them! Period. TLS 1.0 and
1.1 are discouraged and superseded and should also not be used anymore as well.
Unless you really need to `support old browsers
<https://www.ssllabs.com/ssltest/clients.html>`_.


What is SSL / TLS?
==================

SSL stands for Secure Socket Layer. TLS stands for Transport Layer Security.
But that's just words. They are both cryptographic protocols for communication
systems most notably networks. Either one provides 2 of the 3 parts of
"Information security":

* Confidentiality which is provided through encryption
* Integrity which is provided through signing

Availability is the third part in Information Security but needs to be handled
on a different layer.


Web Server Configuration
========================

Because this is the blog post for my talk from DjangoCon US 2016 and most
things we do with Django these days are website, let us have a look at how to
configure web servers to handle SSL.

Apache 2 / httpd
----------------

Let's start with Apache 2 or httpd

.. code-block:: apache

    <VirtualHost *:443>
        ServerName  example.com
        SSLEngine   on

        # Details at https://cipherli.st/
        SSLCipherSuite         EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH
        SSLHonorCipherOrder    on
        SSLProtocol            all -SSLv3
        SSLCertificateFile     /etc/nginx/ssl/example.com.crt
        SSLCertificateKeyFile  /etc/nginx/ssl/example.com.key
        SSLOpenSSLConfCmd      DHParameters   "/etc/nginx/ssl/example.com.dh"
    </VirtualHost>

You need to switch on the SSL engine. You want to define which ciphers you want
and make sure the connection is going to use the best cipher it can, according
to **your** list, not the client's.

You also want to ensure to not use SSL and only TLS and maybe go for TLS 1.2
only.

Defining a custom Diffie-Hellman Parameter is also a good idea. That is used
for the initial key exchange between a client and a server.

Nginx
-----

And this is the syntax for Nginx. It looks pretty much the same as the one for
Apache 2.

.. code-block:: nginx

    host {
        listen       [::]:443 ssl;
        server_name  example.com;

        # Details at https://cipherli.st/
        ssl_ciphers                EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH;
        ssl_prefer_server_ciphers  on;
        ssl_protocols              TLSv1 TLSv1.1 TLSv1.2;
        ssl_certificate            /etc/nginx/ssl/example.com.crt;
        ssl_certificate_key        /etc/nginx/ssl/example.com.key;
        ssl_dhparam                /etc/nginx/ssl/example.com.dh;
    }


What is Let's Encrypt?
======================

Now that we know how to configure web servers where the heck do we get the
certificates from?

And what the heck is "`Let's Encrypt <https://letsencrypt.org/>`_"?

And how does the whole SSL certificate thing work anyway??

In order to answer these questions I need to tell you a bit about how the
entire certificate machinery works.

How does SSL work?
==================

.. gallery::
   :small: 1
   :medium: 2
   :large: 3
   :nocrop:

   .. image:: djangoconus2016/truststore.png
      :alt: Certificate Authorities and Trust Store concept in browsers
      :class: offset-l2

Let us start with CAs: CA stands for Certificate Authority. These are "trusted"
entities we or our browsers rely on in order to establish a *chain of trust*

Browsers, email clients, and other programs have a pre-installed set of root
certificates. These are provided by Root CAs, CAs that e.g. browser vendors --
such as Mozilla and Google -- trust. That database of root certificates is the
"trust store".

The Root CAs sign intermediate certificates. Most Root CAs just sign their own
intermediate certificates. Some Root CAs though (in the diagram "Root CA 3")
are not in the trust store. So they are not automatically trusted by our
browsers.

Trusted Root CAs can *cross sign* other CA's intermediate certificates and make
certificates signed by "Intermediate CA 3" trusted by a browser.

Which brings me to the next point: the certificate you can buy from well known
vendors are not signed by their root certificates but are signed by the
intermediate certificates.

As a result, when your browser trusts Root Cert 1, it trusts Intermediate Cert
1, and hence it trusts all certificates signed by Intermediate Cert 1.

If your browser trusts Root Cert 2, it trusts Intermediate Cert 3, and hence it
trusts all certificates signed by Intermediate Cert 3.


What is Let's Encrypt?
===========================

It's a Root CA, that's not in global trust stores. At least not yet. Their
Intermediate certificate is cross-signed by IdenTrust which is in all common
trust stores.

But Let's Encrypt has control over their intermediate Cert, which allows them
to sign arbitrary other certificates, which we will use for our servers.

Let's Encrypt offers an API to get "unlimited" SSL certificates for your
domains, free of charge.

By now they issued more than 5 million certificates through their API.

The process during which one can get a certificate is defined as `ACME
<https://github.com/letsencrypt/acme-spec>`_ or Automatic Certificate
Management Environment.

It's a fairly simple JSON API with some crypto magic separated in 4 major
steps.

In order to use the Let's Encrypt API one needs three things:

1. An Account Key -- This is most likely an RSA public key pair

2. A Certificate Key -- That's the key you put in your web server config

3. A Certificate Signing Requests (CSR) -- This contains the list of domains
   you want to be part of the certificate

.. gallery::
   :small: 1
   :medium: 2
   :large: 3
   :nocrop:

   .. image:: djangoconus2016/acme.png
      :alt: The ACME process
      :class: offset-l2

The first API endpoint is "new-reg". This authenticates *you* as a "person" or
"server" against Let's Encrypt. You send your Account Key's public key signed
with the private key to Let's Encrypt. You can optionally include a mail
address to get notified about expired certificates.

Second, there is "new-authz". You send your CSR to Let's Encrypt signed with
your Account Key. The API responds with a list of challenges. These are
specially crafted URLs, with specific content, under each requested domain, you
need to make available. This is the step to proof you have control over the
content served under a given domain.

"challenge" is the next step. For each challenge you received, Let's Encrypt is
going to request the related challenge you made available and check for its
correctness.

Lastly, "new-cert". When all challenges succeeded you can request the
certificate and put that in the place where your web server finds it.

And here's the Apache 2 / httpd config to make those challenges available

.. code-block:: apache

    <VirtualHost *:80>
        ServerName  example.com

        Redirect    /  https://example.com/

        Alias "/.well-known/acme-challenge/" "/srv/http/acme-challenges/"
        <Directory "/srv/http/acme-challenges">
            AllowOverride None
            Options None
            Require all granted
        </Directory>
    </VirtualHost>

And the same one for Nginx.

.. code-block:: nginx

    host {
        listen       [::]:80;
        server_name  example.com;

        location /.well-known/acme-challenge/ {
            alias      /srv/http/acme-challenges/;
            try_files  $uri =404;
        }

        location / {
            return  301  https://example.com$request_uri;
        }
    }


How to use Let's Encrypt?
=========================

There's an official client which does "all" the magic. Literally, it rewrites
your Apache config file.

That's the wrong approach, in my opinion. That's a task for configuration and
system management tools. `Watch my talk from 2015th PyCon Australia
<{filename}/Development/2015-08-01__en__the-necessity-of-configuration-and-system-management-tools.rst>`_
for details on that topic.

There's a script `acme-tiny by Daniel Roesler
<https://github.com/diafygi/acme-tiny>`_ which has 200 lines. Easy to
understand. I Recommended to read through the code. `I forked that
<https://github.com/MarkusH/acme-tiny/tree/systemd>`_ and added support for
Systemd and a few other things.

There are also a bunch of other tools. E.g. `letsencrypt-aws
by Alex Gaynor <https://github.com/alex/letsencrypt-aws>`_. I haven't used it
myself, but it probably just does what the name suggests.

And there's `Rproxy by Amber Brown <https://github.com/hawkowl/rproxy>`_

Personally and at djangoproject.com we use my fork of acme-tiny.

But all the scripts boil down to the same things: You need an account key, a
certificate signing request, a place to put the challenges, and a final
location for the full certificate.

.. code-block:: bash

    $ python3 /etc/acme-tiny/acme-tiny.py \
        --account-key "/etc/acme-tiny/account.key" \
        --csr "/etc/acme-tiny/example.com.csr" \
        --acme-dir "/srv/www/acme-challenges" \
        --output "/etc/nginx/ssl/example.com.crt" \
        --combine "https://letsencrypt.org/certs/lets-encrypt-x3-cross-signed.pem"


Adjusting Django
================

Now that this is sorted, how do we use HTTPS in Django and what do you need to
change?

As it turns out, not much.

You want to make cookies only accessible via HTTPS. But only on production
systems. You can't use HTTPS locally at least not without some complex steps.
At least not with built-in features. There is, however, a ``runserver_plus``
command in the `django-extensions
<https://github.com/django-extensions/django-extensions>`_ 3rd party app.
Hence, set the settings variables through environment variables:

.. code-block:: python

        import os

        CSRF_COOKIE_SECURE = os.getenv('SECURE_COOKIES') == 'yes'
        SESSION_COOKIE_SECURE = os.getenv('SECURE_COOKIES') == 'yes'

If you use secure cookies with the runserver command this might manifest as a
HTTP 403 error when you try to login to the admin because the CSRF cookie won't
be submitted.

Apart from that, there a couple of things you can optionally enable.  Have a
look at the `Security Topic in the Documentation
<https://docs.djangoproject.com/en/dev/topics/security/>`_.

Most things you don't want to do in Django though, but in your reverse proxy if
at all possible. It'll be faster.


What I didn't cover ... but want to mention
===========================================

Let's Encrypt's certificates are only valid for 90 days. If you need to revoke
one before, there's an API call for that.

If you lost your account key or it was compromised you can change it as well.

You probably want `HSTS (HTTP Strict Transport Security)
<https://en.wikipedia.org/wiki/HTTP_Strict_Transport_Security>`_. Really.
Running a website on HTTP and HTTPS may make it possible for attackers to force
HTTP requests.

Similar to HSTS there's also `HPKP (HTTP Public Key Pinning)
<https://en.wikipedia.org/wiki/HTTP_Public_Key_Pinning>`_.

This feature is neat but mostly not too useful unless you're a big organization
and you are regular victim of DNS attacks.

And of course you can use the Let's Encrypy certificates for services other
than HTTPS. The only thing you need to make sure is that the domains for that
certificate serve valid challenge responses on port 80 as explained above.

Things that could go wrong -- An incomplete list
=================================================

And because we're talking about cryptographic tropic, here's an incomplete list
of things that can go wrong:

* Both, HSTS and HPKP come with a risk of making your website unavailable for
  previous users. Check out how it works. You want it, but be aware of the risks!

* When you deal with cryptographic keys, there's always a possibility to leak
  keys. Be aware of that and have a process in place to handle the case of a
  leak certificate or account key!

* Some people claim HTTPS is causing too much resourcen usage and they can't use
  it. With not too old hardware that's not an issue.


Resources
=========

* `Slides <https://speakerdeck.com/markush/ssl-all-the-things-djangocon-us-2016>`_

* https://cipherli.st/
* https://www.ssllabs.com/ssltest/index.html
* https://hynek.me/talks/tls/
* https://ssldecoder.org/
* https://securityheaders.io/
* https://github.com/ietf-wg-acme/acme/blob/bf34c2a/draft-ietf-acme-acme.md
* https://security.googleblog.com/2016/07/experimenting-with-post-quantum.html
