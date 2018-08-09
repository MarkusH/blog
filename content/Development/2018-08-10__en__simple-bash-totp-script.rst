=======================
Simple TOTP Bash Script
=======================

:tags: Bash, 2FA, Security, TOTP
:author: Markus Holtermann
:summary: Most TOTP / 2FA clients are for smartphones. There's not really an
   easy / simple one for Linux. Here's one in Bash


Using Two Factor Authentication (2FA) for services is a good idea. Most
services will require you to have an Android or iOS smartphone and use Google
Authenticator or similar apps to generate TOTP codes.

That's fine if you have a smartphone. If you don't have one you can often use
SMS tokens instead. But SMS for 2FA is not recommended anymore. Also, what do
you do if you don't have a smartphone or mobile phone at all? I know of at
least 2 people who need to use 2FA and don't have a smartphone.

First thing I suggested to them: use Authy, there's a Chrome plugin you can use
instead of a smartphone. But it turns out, they seem to require you to have a
smartphone. I guess for backup or security reasons.

Since both people have access to a Linux system, I figured I might as well find
a Linux client that allows them to generate TOTPs. But all tools or scripts I
could find seemed bloated. Until `Emma Delescolle pointed
<https://twitter.com/EmmaDelescolle/status/1027498473590018049>`_ me to
`oath-toolkit <https://www.nongnu.org/oath-toolkit/>`_. Thanks!

With the included ``oathtool`` one can generate a TOTP:

.. code-block:: shell

   $ oathtool --base32 --totp ONSWG4TFOQYTEMZUGU3DOOBZ
   785263

Great. Now I only needed a way to securely store the secret. I figured a
symmetrically encrypted file using GnuPG would probably do just fine:

.. code-block:: shell

   $ echo ONSWG4TFOQYTEMZUGU3DOOBZ | gpg --symmetric --out ~/.secret-file

And loading that file isn't hard either:

.. code-block:: shell

   $ secret="$(gpg < ~/.secret-file)"
   $ oathtool --base32 --totp "$secret"
   785263

Great. Now I only needed to tie those things together in a small script that
lets me add new secrets for various services and gives me a TOTP back when I
need one:

.. code-block:: bash

   #!/bin/bash

   # Copyright (c) 2018, info AT markusholtermann DOT eu
   # All rights reserved.
   #
   # Redistribution and use in source and binary forms, with or without
   # modification, are permitted provided that the following conditions are met:
   #     * Redistributions of source code must retain the above copyright
   #       notice, this list of conditions and the following disclaimer.
   #     * Redistributions in binary form must reproduce the above copyright
   #       notice, this list of conditions and the following disclaimer in the
   #       documentation and/or other materials provided with the distribution.
   #     * Neither the name of the <organization> nor the
   #       names of its contributors may be used to endorse or promote products
   #       derived from this software without specific prior written permission.
   #
   # THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
   # ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
   # WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
   # DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
   # DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
   # (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
   # LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
   # ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
   # (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
   # SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

   set -e
   set -o pipefail

   SOURCE_DIR=~/.config/2fa

   function init() {
       mkdir -p $SOURCE_DIR
       chmod 0700 $SOURCE_DIR

       if ! hash gpg 2>/dev/null ; then
           echo "Please ensure that GnuPG is installed!"
           exit 1
       fi
       if ! hash oathtool 2>/dev/null ; then
           echo "Please ensure that oathtool is installed!"
           exit 2
       fi
   }

   function add_key() {
       echo "Adding a new key"
       if [ "x$1" != "x" ] ; then
           identifier=$1
       else
           echo "What's the identifier?"
           read -r identifier
       fi
       echo "What's the secret?"
       read -r secret
       echo "$secret" | gpg --quiet --symmetric --out "$SOURCE_DIR/$identifier"
   }

   function get_totp() {
       if [ "x$1" != "x" ] ; then
           identifier=$1
       else
           echo "What's the identifier?"
           read -r identifier
       fi
       secret="$(gpg --quiet < "$SOURCE_DIR/$identifier")"
       oathtool --base32 --totp "$secret"
   }

   function list() {
       ls -1 "$SOURCE_DIR"
   }

   function help() {
       echo "Setup a new TOTP account or generate a new TOTP token from an existing account."
       echo
       echo "Usage: totp.sh [--add|--list|--totp] [IDENTIFIER]"
       echo
       echo -e "--add     Will ask for an identifier (i.e. 'google', 'slack', ...) and\\n" \
               "         then for the secret provided by the service provider."
       echo -e "--list    Will list all available identifiers."
       echo -e "--totp    Will ask for an identifier (i.e. 'google', 'slack', ...) and\\n" \
               "         then return the TOTP token."
   }

   init

   case $1 in
       --add)
           add_key "$2"
           ;;
       --list)
           list
           ;;
       --totp)
           get_totp "$2"
           ;;
       *)
           help
   esac

How do I use the tool? Let's say we want to add 2FA to our Google account. You
copy the 2FA key from Google's website and add it:

.. code-block:: shell

   $ totp.sh --add google
   Adding a new key
   What's the secret?
   abcd efgh 1234 ijkl mnop 5678 90qr stuv

At this point you'll be asked for a password and confirmation to secure the
secret. Repeat the above with different identifiers for various services you
want.

You can then list all available services / identifiers:

.. code-block:: shell

   $ totp.sh --list
   google

And lastly, you can get the TOTP back:

.. code-block:: shell

   $ totp.sh --totp google
   612027
