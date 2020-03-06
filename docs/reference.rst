.. _frontend-ref:

Front End Reference
===================

A simple consistency check on a site can be done by doing the following
with the Python API when an instance of ``dynamo`` is installed::

  from dynamo_consistency import config, datatypes, remotelister, inventorylister

  config.LOCATION = '/path/to/config.json'
  site = 'T2_US_MIT'                        # For example

  inventory_listing = inventorylister.listing(site)
  remote_listing = remotelister.listing(site)

  datatypes.compare(inventory_listing, remote_listing, 'results')

In this example,
the list of file LFNs in the inventory and not at the site will be in ``results_missing.txt``.
The list of file LFNs at the site and not in the inventory will be in ``results_orphan.txt``.
The ``listing`` functions can be re-implemented to perform the check desired.
This is detailed more in :ref:`backend-ref`.

The following is a full reference to the submodules
directly inside of the :py:mod:`dynamo_consistency` module.
These are the modules indended to be interacted with by a typical user.
To see more details about the backend connections to dynamo
and remote sites, see :ref:`backend-ref`.

.. contents::
   :local:

cache.py
--------

.. automodule:: dynamo_consistency.cache
   :members:

.. _config-ref:

config.py
---------

.. automodule:: dynamo_consistency.config
   :members:

create.py
---------

.. automodule:: dynamo_consistency.create
   :members:

datatypes.py
------------

.. automodule:: dynamo_consistency.datatypes
   :members:

emptyremover.py
---------------

.. automodule:: dynamo_consistency.emptyremover
   :members:

filters.py
----------

.. automodule:: dynamo_consistency.filters
   :members:

history.py
----------

.. automodule:: dynamo_consistency.history
   :members:

inventorylister.py
------------------

.. automodule:: dynamo_consistency.inventorylister
   :members:

logsetup.py
-----------

.. automodule:: dynamo_consistency.logsetup
   :members:

main.py
-------

.. automodule:: dynamo_consistency.main
   :members:

messaging.py
------------

.. automodule:: dynamo_consistency.messaging
   :members:

parser.py
---------

.. automodule:: dynamo_consistency.parser
   :members:

picker.py
---------

.. automodule:: dynamo_consistency.picker
   :members:

remotelister.py
---------------

.. automodule:: dynamo_consistency.remotelister
   :members:

signaling.py
------------

.. automodule:: dynamo_consistency.signaling
   :members:

summary.py
----------

.. automodule:: dynamo_consistency.summary
   :members:
