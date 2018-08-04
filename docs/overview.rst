Python Overview
===============

A simple consistency check on a site can be done by doing the following
when an instance of ``dynamo`` is installed::

    from dynamo_consistency import config, datatypes, remotelister, inventorylister

    config.CONFIG_FILE = '/path/to/config.json'
    site = 'T2_US_MIT'     # For example

    inventory_listing = inventorylister.listing(site)
    remote_listing = remotelister.listing(site)

    datatypes.compare(inventory_listing, remote_listing, 'results')

In this example,
the list of file LFNs in the inventory and not at the site will be in ``results_missing.txt``.
The list of file LFNs at the site and not in the inventory will be in ``results_orphan.txt``.

The actual comparison done by the production instance of ``dynamo`` has a few more filters and steps,
as outlined under :ref:`compare-ref`.
