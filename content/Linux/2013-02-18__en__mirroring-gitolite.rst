==================
Mirroring gitolite
==================

:tags: Bash, Git, Network, Server
:author: Markus Holtermann
:summary: A long time ago I wrote an article about how to install gitolite.
   Yesterday an article popped up in my feed reader that shows a short script
   on how to mirroring gitolite servers.


A long time ago I wrote an article about `how to install gitolite`_. Yesterday
an article popped up in my feed reader that shows a short script on how to
`mirroring gitolite`_ servers.

Since I wrote my custom script once I had set up gitolite, I was a bit curious
about the differences to my script today. So I checked the referred script and
noticed some problems that probably occur over the time:

* New branches on the remote are not fetched
* New tags on the remote are not fetched
* Using working copies results in way larger mirrors

As one can see, the script lacks some major features.

.. code-block:: bash

    #!/bin/bash
    # Copyright (c) 2011-2013 Markus Holtermann
    # MIT License: http://download.markusholtermann.eu/MIT.txt

    BACKUP_DIR=/data/git-mirror/
    REMOTE=git@git.example.com

    if [ ! -d "${BACKUP_DIR}" ] ; then
        mkdir -p "${BACKUP_DIR}"
    fi

    cd "${BACKUP_DIR}"

    for repo in $(ssh ${REMOTE} 2> /dev/null | grep -e "^\s\+R" | sed -e 's/\r//g' | awk '{print $3}')
    do
        if [[ -d ${repo}.git ]] ; then
            cd ${repo}.git
            echo "Updating ${REMOTE}:${repo} ..."
            git fetch --all
            echo " ... done"
            cd -
        else
            echo "Cloning ${REMOTE}:${repo} ..."
            git clone --mirror ${REMOTE}:${repo}.git
            echo " ... done"
        fi
    done

The magic to prevent working directories lies in the ``--mirror`` parameter
while cloning a repository. To get notified about new branches and tags on the
remote side, I use ``git fetch --all``. The `man (1) page to git-fetch`_
describes it as

    Fetches named heads or tags from one or more other repositories, along with
    the objects necessary to complete them. [...]

However, the script above does not remove branches/tags that don't exist on the
remote any more. Since I use the script only for backup purposes, I don't need
that feature. But I would just remove all branches (local and remote) from the
local mirror and would run git-fetch afterwards.

Enjoy the script.


.. _how to install gitolite:
   {filename}/Linux/2011-09-16__en__my-own-git-server-installing-gitolite.rst
.. _mirroring gitolite: http://noqqe.de/blog/2013/02/17/mirroring-gitolite/
.. _man (1) page to git-fetch: http://linux.die.net/man/1/git-fetch
