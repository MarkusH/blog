============================
SSL All The Things In Python
============================

:tags: Network, PyCon, Security, Server, Talk
:author: Markus Holtermann
:image: pyconau2016/talk-cover.jpg
:summary: Getting SSL / TLS right is hard. As an update to my DjangoCon US 2016
   talk here's how you use Python's SSL library.


.. image:: /images/pyconau2016/logo.png
   :align: right
   :alt: PyCon AU 2016 -- Melbourne
   :class: margin-left

.. image:: /images/pyconnz2016/logo.png
   :align: right
   :alt: Kiwi PyCon 2016 -- Dunedin
   :class: clearfix margin-left

Introduction
============

Following my `DjangoCon US 2016 Talk
<{filename}/Development/2016-07-19__en__ssl-all-the-things.rst>`_ I gave a talk
at PyCon Australia in Melbourne and PyCon New Zealand in Dunedin.

Most of the slides from the former talk are the same. The major difference is
the replacement of Django specifics with examples for a Python client and
server implementation using the ``ssl`` standard library package.

How to use SSL in Python
========================

Client Side
-----------

The client side of SSL connections is comparably easy as opposed to the server
side. That doesn't mean you can't easily mess up things and make the entire
encryption layer you intend to have useless. But what would security be without
some danger, right 😉.

First of all you create a socket. That's the normal Python socket layer. You
then create a default SSL context which has all the best practices of the
installed Python version. You can furthermore drop some protocols if you feel
like it and your requirements allow for that. Next you wrap the socket into an
SSL socket. While you do that, make sure you check the host name! And finally
you connect to the server.

.. code-block:: python

    import socket, ssl

    HOST, PORT = 'example.com', 443

    def handle(conn):
        conn.write(b'GET / HTTP/1.1\n')
        print(conn.recv().decode())

    def main():
        sock = socket.socket(socket.AF_INET)
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # optional
        conn = context.wrap_socket(sock, server_hostname=HOST)
        try:
            conn.connect((HOST, PORT))
            handle(conn)
        finally:
            conn.close()

    if __name__ == '__main__':
        main()

Server Side
-----------

The server side of SSL connections is more complicated and you can mess up much
more. But let us start at the beginning.

You create a socket and bind it to an address and port. You, again, create a
SSL default context for a server.  The first thing you probably want to do is
load the key, certificate and all intermediate certificates. You can put all of
these into one file in that order. You can also provide them as separate
arguments to the ``load_cert_chain()`` function. Again, you can exclude some
protocols and update other context options based on your requirements. In the
example we're disabling TLS 1.0 and 1.1, because nobody needs them, right 😉.
Lastly, you want to set a bunch of ciphers. That list comes from `cipherli.st
<https://cipherli.st>`_. Finally you start listening on the socket and wrap it
with the SSL context for each connection.

.. code-block:: python

    import socket, ssl

    HOST, PORT, CERT = 'example.com', 443, '/path/to/example.com.pem'

    def handle(conn):
      print(conn.recv())
      conn.write(b'HTTP/1.1 200 OK\n\n%s' % conn.getpeername()[0].encode())

    def main():
      sock = socket.socket()
      sock.bind((HOST, PORT))
      sock.listen(5)
      context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
      context.load_cert_chain(certfile=CERT)  # 1. key, 2. cert, 3. intermediates
      context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # optional
      context.set_ciphers('EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH')
      while True:
        conn = None
        ssock, addr = sock.accept()
        try:
          conn = context.wrap_socket(ssock, server_side=True)
          handle(conn)
        except ssl.SSLError as e:
          print(e)
        finally:
          if conn:
            conn.close()
    if __name__ == '__main__':
      main()

Resources
=========

* `Slides PyCon AU <https://speakerdeck.com/markush/ssl-all-the-things-pycon-au-2016>`_
* `Slides PyCon NZ <https://speakerdeck.com/markush/ssl-all-the-things-pycon-nz-2016>`_
