=======================================
My own Git server - installing gitolite
=======================================

:tags: Debian, Git, Linux, Server
:author: Markus Holtermann


Yesterday I wanted to share some code with some friends, but I didn't want to
create a repository on `GitHub`_, so I decided to install
my own git server. After some minutes googleing I found `gitosis`_ and
`gitolite`_. Both programs seem to be popular, but the last commit to *gitosis*
was two yeas ago. So I chose *gitolite*.

I had two options on how to install *gitolite*: either through the package
manager (``sudo apt-get install gitolite``) or by directly cloning the
repository from Github. I used the latter one to be up to date.

I wanted *gitolite* to run under its own user account, lets say ``gitolite``.
So I had to add this user:

.. code-block:: bash

    markus@server:~$ sudo adduser --system \
    --shell /bin/bash \
    --group \
    --disabled-password \
    --home /home/gitolite \
    gitolite


The installation was quite easy. For initial configuration I needed my SSH-key.
So I copied my local ``~/.ssh/id_rsa.pub`` to ``/tmp/markus.pub`` on the
server. Then I switched to the newly created user and cloned the code from
Github:

.. code-block:: bash

    markus@server:~$ sudo su gitolite -
    gitolite@server:/home/markus$ cd
    gitolite@server:~$ git clone https://github.com/sitaramc/gitolite.git


After these steps I could install *gitolite*. Therefor I ran those commands:

.. code-block:: bash

    gitolite@server:~$ cd gitolite
    gitolite@server:~$ src/gl-system-install
    gitolite@server:~$ gl-setup /tmp/markus.pub


Now I was able to clone the repository to my local machine:

.. code-block:: bash

    git clone gitolite@server:gitolite-admin


A new folder ``gitolite-admin`` was created that contains a configuration file
and an directory for SSH-keys. To add my other computers and my friends to the
repositories, I changed the configuration file as follows:

.. code-block:: ini

    @markus = markus markus2 markus3
    @user = user1 user2
    @otheruser = otheruser1 otheruser2 otheruser3

    repo gitolite-admin
         RW = @markus

    repo project1
         RW = @markus @user otheruser2

    repo project2
         RW = @markus @user
         R  = @otheruser

    repo project3
         RW = @markus
         R  = @all


The first three lines declare some groups, so if one gets a new client, I can
add that to the group and he will directly have access to all repositories that
his other clients can access as well.

The repository *gitolite-admin* is only readable (``R``) and writabel (``W``)
by myself. The *project1* has read/write permissions for all my clients, all
clients of *user* but only the second client of *otheruser*. In the second
project repository, (*project2*) all clients of *otheruser* can only read, but
not write. Finally, repository *project3* is only writable for all my clients
but readable for **all** users.

The next step was to add the changes and all new SSH-keys to the repository:

.. code-block:: bash

    $ git add conf/gitolite.conf keydir/markus2.pub keydir/markus3.pub \
    keydir/user1.pub keydir/user2.pub \
    keydir/otheruser1.pub keydir/otheruser2.pub keydir/otheruser3.pub
    $ git commit -m 'add first projects and users'
    $ git push


Ready.

If you are now trying to connect via SSH and user ``gitolite`` to the server,
you will get a nice information:

.. code-block:: bash

    $ ssh git@server
    hello markus, this is gitolite running on git
    the gitolite config gives you the following access:
         R   W      gitolite-admin 
         R   W      project1
         R   W      project2
         R   W      project3
    Connection to server closed.


Thanks for reading :)

Markus


.. _GitHub: https://github.com
.. _gitosis: http://eagain.net/gitweb/?p=gitosis.git
.. _gitolite: https://github.com/sitaramc/gitolite
