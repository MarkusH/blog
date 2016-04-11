===================================
Reference variables in Ansible YAML
===================================

:tags: Ansible, YAML
:author: Markus Holtermann
:image: ansible-logo.png
:summary: Mostly unknown, but the YAML syntax used by e.g. Ansible allows
   convenient references to other variables.

Today I found myself in a typical DRY situation when working on an Ansible
role. I was defining a slightly more complex variable to later be used in an
Ansible template. The variable looked a bit like this:

.. code-block:: yaml

    backups:
      - name: primary
        output: /mnt/data/extern
        includes:
          - /etc/
          - /home/
          - /var/lib/
      - name: secondary
        output: /mnt/data/intern
        includes:
          - /etc/
          - /home/
          - /var/lib/
      - name: remote
        output: "ssh://user@host:/mnt/data/backup/client1"
        includes:
          - /etc/
          - /home/
          - /var/lib/
      - name: grab-n-go
        output: /mnt/usb-drive
        includes:
          - /home/markus/documents/important

As you can easily see, the ``includes`` item always contains the same values
for the first 3 items. I looked into the possibility to define the list of
directories only once and use a variable in those places.

I started off with this approach:

.. code-block:: yaml

    backup_includes:
      - /etc/
      - /home/
      - /var/lib/

    backups:
      - name: primary
        output: /mnt/data/extern
        includes: backup_includes
      - name: secondary
        output: /mnt/data/intern
        includes: backup_includes
      - name: remote
        output: "ssh://user@host:/mnt/data/backup/client1"
        includes: backup_includes
      - name: grab-n-go
        output: /mnt/usb-drive
        includes:
          - /home/markus/documents/important

Turns out, that does not work. Instead, when iterating over
``backups.X.includes`` Jinja2 is iterating over the string ``backup_includes``.
That's of course not what I want.

But YAML does provide a solution to reference other variables, which I found on
`StackOverflow <http://stackoverflow.com/a/18877077>`_. It's also shown on
`Wikipedia <https://en.wikipedia.org/wiki/YAML#Repeated_nodes>`_. Using ``&``
to define an **anchor** and ``*`` to dereference it.

.. code-block:: yaml

    backup_includes: &backup_includes
      - /etc/
      - /home/
      - /var/lib/

    backups:
      - name: primary
        output: /mnt/data/extern
        includes: *backup_includes
      - name: secondary
        output: /mnt/data/intern
        includes: *backup_includes
      - name: remote
        output: "ssh://user@host:/mnt/data/backup/client1"
        includes: *backup_includes
      - name: grab-n-go
        output: /mnt/usb-drive
        includes:
          - /home/markus/documents/important

Apart from ``&`` and ``*`` there's also the ``<<:`` operator to clone an item
and allow overriding of its child attributes:

.. code-block:: yaml

    backup_item: &backup_item
      includes:
        - /etc/
        - /home/
        - /var/lib/
      excludes: []

    backups:
      - <<: *backup_item
        name: primary
        output: /mnt/data/extern
      - <<: *backup_item
        name: secondary
        output: /mnt/data/intern
      - <<: *backup_item
        name: remote
        output: "ssh://user@host:/mnt/data/backup/client1"
        excludes:
          - /var/lib/
