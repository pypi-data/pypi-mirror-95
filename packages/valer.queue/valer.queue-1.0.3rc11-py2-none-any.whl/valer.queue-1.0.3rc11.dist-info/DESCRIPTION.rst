Queue of asynchronous tasks for SENAITE LIMS
============================================

.. image:: https://img.shields.io/pypi/v/senaite.queue.svg?style=flat-square
    :target: https://pypi.python.org/pypi/senaite.queue

.. image:: https://img.shields.io/travis/senaite/senaite.queue/master.svg?style=flat-square
    :target: https://travis-ci.org/senaite/senaite.queue

.. image:: https://readthedocs.org/projects/pip/badge/
    :target: https://senaitequeue.readthedocs.org

.. image:: https://img.shields.io/github/issues-pr/senaite/senaite.queue.svg?style=flat-square
    :target: https://github.com/senaite/senaite.queue/pulls

.. image:: https://img.shields.io/github/issues/senaite/senaite.queue.svg?style=flat-square
    :target: https://github.com/senaite/senaite.queue/issues

.. image:: https://img.shields.io/badge/Made%20for%20SENAITE-%E2%AC%A1-lightgrey.svg
   :target: https://www.senaite.com


About
-----

This add-on enables asynchronous tasks for `SENAITE LIMS`_, that allows to
better handle concurrent actions and processes when the workload is high. Is
specially indicated for high-demand instances and for when there are custom
processes that take long to complete. Essentially, `senaite.queue` reduces the
chance of transaction commits by handling tasks asynchronously, in an
unattended and sequential manner.

Once installed, this add-on enables asynchronous processing of those tasks that
usually have a heavier footprint regarding performance, and with highest chance
of transaction conflicts:

* Assignment of analyses to worksheets
* Assignment of worksheet template to a worksheet
* Creation of a worksheet by using a worksheet template
* Workflow actions (submit, verify, etc.) for analyses assigned to worksheets
* Recursive permissions assignment on client contacts creation

This add-on neither provides support for workflow transitions/actions at Sample
level nor for Sample creation. However, this add-on can be extended easily to
match additional requirements.


Documentation
-------------

* https://senaitequeue.readthedocs.io


Contribute
----------

We want contributing to SENAITE.QUEUE to be fun, enjoyable, and educational
for anyone, and everyone. This project adheres to the `Contributor Covenant`_.

By participating, you are expected to uphold this code. Please report
unacceptable behavior.

Contributions go far beyond pull requests and commits. Although we love giving
you the opportunity to put your stamp on SENAITE.QUEUE, we also are thrilled
to receive a variety of other contributions.

Please, read `Contributing to senaite.queue document`_.

If you wish to contribute with translations, check the project site on `Transifex`_.


Feedback and support
--------------------

* `Community site`_
* `Gitter channel`_
* `Users list`_


License
-------

**SENAITE.QUEUE** Copyright (C) 2019-2020 RIDING BYTES & NARALABS

This program is free software; you can redistribute it and/or modify it under
the terms of the `GNU General Public License version 2`_ as published
by the Free Software Foundation.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

.. Links

.. _SENAITE LIMS: https://www.senaite.com
.. _Contributor Covenant: https://github.com/senaite/senaite.queue/blob/master/CODE_OF_CONDUCT.md
.. _Contributing to senaite.queue document: https://github.com/senaite/senaite.queue/blob/master/CONTRIBUTING.md
.. _Transifex: https://www.transifex.com/senaite/senaite-queue
.. _Community site: https://community.senaite.org/
.. _Gitter channel: https://gitter.im/senaite/Lobby
.. _Users list: https://sourceforge.net/projects/senaite/lists/senaite-users
.. _GNU General Public License version 2: https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

Release notes
=============

Update from 1.0.1 to 1.0.2
--------------------------

With version 1.0.2, the legacy storage for queued tasks has changed and helper
storages (e.g. for Worksheets) are no longer required. ``IQueued`` marker
interface is no longer used neither. Most of the base code has been refactored
keeping in mind the following objectives:

* Less complexity: less code, better code
* Less chance of transaction commit conflicts
* Boost performance: better experience, with no delays

All these changes also makes the add-on easier to extend and maintain. The
downside is that old legacy storage is no longer used and therefore, tasks that
were queued before the upgrade will be discarded.

* Be sure there are no remaining tasks in the queue before the upgrade
* If you have your own add-on extending ``senaite.queue``, please review the changes
  and check if some parts of your add-on require modifications

A queue server has been introduced. Therefore, two zeo clients are recommended:
one that acts as the server and at least another one in charge of consuming
tasks. Also, this version now depends on three additional packages: ``requests``,
``senaite.jsonapi`` and ``cryptography``. Please read the installation
instructions and run buildout to download the dependencies.

Installation
============

Is strongly recommended to have a SENAITE instance setup in ZEO mode, because
this add-on is especially useful when a reserved zeo client is used to act as
a queue server and at least one additional zeo client for tasks consumption.

In standalone installation, only one CPU / CPU core can be used for processing
requests, with a limited number of threads (usually 2). With a ZEO mode setup,
the database can be used by multiple zeo clients at the same time, each one
using it's own CPU. See `Scalability and ZEO`_ for further information.

Create a new reserved user in SENAITE instance (under */senaite/acl_users*). The
recommended username is *queue_consumer*.

This user will be used by the consumer to pop tasks from the queue server in a
sequential manner. The consumer will eventually process the task, but acting as
the user who initially triggered the process. However, the reserved user
responsible of dispatching must have enough privileges. Assign this user to
the group "Site Administrator" and/or "Manager".

First, add this add-on in the `eggs` section of your buildout configuration file:

.. code-block:: ini

    [buildout]

    ...

    [instance]
    ...
    eggs =
        ...
        senaite.queue


Then, add a two clients (a consumer and the server) in your buildout
configuration:

.. code-block:: ini

    # Reserved user for dispatching queued tasks
    # See https://pypi.org/project/senaite.queue
    queue-user-name=queue_consumer
    queue-user-password=queue_consumer_password

    parts =
        ....
        queue_consumer
        queue_server


and configure two reserved clients:

.. code-block:: ini

    [queue_consumer]
    # ZEO Client reserved for the consumption of queued tasks
    <= client_base
    recipe = plone.recipe.zope2instance
    http-address = 127.0.0.1:8089
    zope-conf-additional =
        <clock-server>
            method /senaite/queue_consume
            period 5
            user ${buildout:queue-user-name}
            password ${buildout:queue-user-password}
            host localhost:8089
        </clock-server>

    [queue_server]
    # ZEO Client reserved to act as the server of the queue
    <= client_base
    recipe = plone.recipe.zope2instance
    http-address = 127.0.0.1:8090

.. note:: These clients will listen to ports 8089 and 8090. They should not be
          accessible to regular users. Thus, if you use a load-balancer
          (e.g HAProxy), is strongly recommended to not add these clients in
          the backend pool.

In most scenarios, this configuration is enough. However, senaite.queue supports
multi consumers, that can be quite useful for those SENAITE installations that
have a very high overload. To add more consumers, add as many zeo client
sections as you need with the additional `clock-server` zope configuration. Do
not forget to set the value `host` correctly to all them, because this value is
used by the queue server to identify the consumers when tasks are requested.

The maximum number of concurrent consumers supported by the queue server is 4.

Run `bin/buildout` afterwards. With this configuration, buildout will download
and install the latest published release of `senaite.queue from Pypi`_.

.. note:: If the buildout fails with a ``ImportError: cannot import name aead``,
          please update OpenSSL to v1.1.1 or above. OpenSSL v1.0.2 is no longer
          supported by ``cryptography`` starting from v3.2. Please, read the
          `changelog from cryptography`_ for further information. Although not
          recommended, you can alternatively stick to version 3.1.1 by adding
          ``cryptography=3.1.1`` in ``[versions]`` section from your buildout.

Once buildout finishes, start the clients:

.. code-block:: shell

    $ sudo -u plone_daemon bin/client1 start
    $ sudo -u plone_daemon bin/queue_server start
    $ sudo -u plone_daemon bin/queue_client start

.. note:: ``plone_daemon`` is the default user created by the quick-installer
          when installing Plone in ZEO cluster mode. Please check
          `Installation of Plone`_ for further information. You might need to
          change this user name depending on how you installed SENAITE.

Then visit your SENAITE site and login with a user with "Site Administrator"
privileges to activate the add-on:

http://localhost:8080/senaite/prefs_install_products_form

.. note:: It assumes you have a SENAITE zeo client listening to port 8080

Once activated, go to `Site Setup > Queue Settings` and, in field "Queue Server",
type the url of the zeo client that will act as the server of the queue.

http://localhost:8090/senaite

.. note:: Do not forget to specify the site id in the url (usually "senaite")


.. Links

.. _senaite.queue from Pypi: https://pypi.org/project/senaite.queue
.. _Scalability and ZEO: https://zope.readthedocs.io/en/latest/zopebook/ZEO.html
.. _changelog from cryptography: https://cryptography.io/en/latest/changelog.html#v3-2
.. _Installation of Plone: https://docs.plone.org/4/en/manage/installing/installation.html#how-to-install-plone

Changelog
=========

1.0.3 (unreleased)
------------------

- Fix client's queue tasks in "queued" status are not updated when "running"


1.0.2 (2020-11-15)
------------------

- Support for multiple consumers (up to 4 concurrent processes)
- Added JSON API endpoints for both queue server and clients
- Queue server-client implementation, without the need of annotations
- Added PAS plugin for authentication, with symmetric encryption
- Delegate the reindex object security to queue when linking contacts to users
- #7 Allow to queue generic worflow actions without specific adapter
- #7 Redux and better performance
- #6 Allow the prioritization of tasks
- #5 No actions can be done to worksheets with queued jobs


1.0.1 (2020-02-09)
------------------

- Allow to manually assign the username to the task to be queued
- Support for failed tasks
- Notify when the value for max_seconds_unlock is too low
- #3 New `queue_tasks` view with the list of tasks and statistics
- #2 Add max_retries setting for failing tasks
- #1 Add sample guard to prevent transitions when queued analyses


1.0.0 (2019-11-10)
------------------

First version



