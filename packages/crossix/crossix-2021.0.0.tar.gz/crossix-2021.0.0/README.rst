=======
crossix
=======

crossix is a private Django project to handle registration to www.crosstriangulaire.com.


Installation
============

You may install this software from your distribution packages, or through pip:

.. code-block:: sh

    $ pip install crossix

Once installed, you must configure it.
The minimal set of settings is the ``[db]`` section of the ``/etc/crossix/config.ini`` file (see below for details).

Once this is configured, you must prepare the database:

.. code-block:: sh

    $ crossixctl migrate

This will create the database; the last step is to point your WSGI server to ``crossix.wsgi``.


Configuration
=============

Crossix will read all configuration files matching ``/etc/crossix/*.ini``.
Those are ini-style files, defining the following parameters:


Application (``[app]``)
-----------------------

General behavior of the application.

Options:

``mode``
    ``str``, the application mode.
    Use ``dev`` for local development and ``prod`` otherwise.

``debug``
    ``bool``, whether to enable debug.
    Valid values: ``on``, ``off``

``secret_key``
    ``str``, **REQUIRED** in ``prod`` mode.
    A secret key for Django security hooks


Site (``[site]``)
-----------------

Hosting and URLs.

Options:

``name``
    ``str``, the name of your site (``crossix``, ``mypaster``, ...).

``base_url``
    ``str``, where your site is hosted.
    A trailing slash is **required**.

``assets_url``
    ``str``, the URL where assets (CSS, JS, ...) are served.
    May be a relative URL.

``admin_mail``
    ``str``, the email where the admin should be notified.

``allowed_hosts``
    ``str list``, comma-separated list of valid ``Host:`` HTTP headers.
    See Django docs for details.


Database (``[db]``)
-------------------

Required; these define where snippets will be stored.
Valid options are:

``engine``
    ``str``, the engine to choose.
    Must be one of ``sqlite``, ``mysql``, ``postgresql``; default is ``sqlite``.

``name``
    ``str``, the name of the database, or its path for sqlite.
    Defaults to ``/var/lib/crossix/db.sqlite``.

``host``
    ``str``, the host of the database server.

``port``
    ``int``, the port of the database server.

``user``
    ``str``, the login to use to connect to the database server.

``password``
    ``str``, the password for the database


Examples:

.. code-block:: ini

    ; A Postgresql configuration; uses default psql port.
    [db]
    engine = postgresql
    name = crossix
    host = psql42.local

.. code-block:: ini

    ; A sample sqlite configuration.
    [db]
    engine = sqlite
    name = /data/replicated/crossix/db.sqlite


Uploads (``[uploads]``)
-----------------------

Options related to private file uploads.

``dir``
    ``path``, storage folder for uploads.
    Must be writable by the WSGI process.

    Example: ``/var/www/crossix/uploads``

``serve``
    ``str``, the file serving mode.
    ``crossix`` relies on `django-sendfile <https://github.com/johnsensible/django-sendfile>`_
    to enhance performance and protection.

    Valid options: ``simple``, ``nginx``, ``xsendfile``, ``mod_wsgi``.

``internal_url``
    ``str``, the internal URL used by django-sendfile to serve the files.
