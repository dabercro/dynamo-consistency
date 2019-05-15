Generating File Lists
=====================

Two listings must be done to compare.
One is the :ref:`inventory-listing-ref`,
and the other is the :ref:`remote-listing-ref`.

.. _inventory-listing-ref:

Inventory Listing
-----------------

Dynamo Consistency only interacts with Dynamo at two points during a check.
First, it gets a listing of what should be at a site.
The next time it interacts with Dynamo is at the end when it reports results.

The inventory is queried before the site is listed remotely due to possible race conditions.
It is not uncommon for a site listing to take multiple days.
In the meanwhile, two things can change in the inventory.
A file can be deleted from a site or it can be added to a site.
An added file is ignored by setting **IgnoreAge** in the :ref:`consistency-config-ref` to a large enough value.
Files that are deleted during the remote listing are filtered out by checking deletion requests.

There are currently multiple ways to get the site contents from Dynamo.
One is to access the MySQL database use for Dynamo storage directly.
This will work as long as the schema does not change.
A more reliable way to keep up with major changes in Dyanmo is to use the Dynamo inventory object.
This method is less optimized when working with the MySQL storage plugin,
but will work for different schemas and any different storage types that are added in the future.

The type of inventory lister is selected via command line options,
or by setting ``dynamo_consistency.opt.V1`` to ``True`` or ``False`` before importing any modules that rely on the backend.
By implementing the three modules ``inventory``, ``registry``, and ``siteinfo``, described in :ref:`backend-ref`,
any other method of communicating with an inventory can be added.

After selecting the backend, the inventory can be listed transparently using the method shown in :ref:`intro-ref`::

  from dynamo_consistency import inventorylister

  listing = inventorylister.listing(sitename)

Here, ``listing`` is a :py:class:`dynamo_consistency.datatypes.DirectoryInfo` object.
:py:class:`DirectoryInfo` contains meta data about a directory, such as its modification timestamp and name.
It also holds a list of sub-directories, in the form of :py:class:`DirectoryInfo` objects, and a list of files.
The files are represented as dictionaries containing the name, size, and modification time of the file.
Each file and :py:class:`DirectoryInfo` also stores a hash of the meta data.
The :py:class:`DirectoryInfo` hash includes information from the object's files and subdirectories too.
This is to speed up the file tree comparison, described in :ref:`compare-algo-ref`.

.. _remote-listing-ref:

Remote Listing
--------------

The remote listing is equally flexible.
The factory function :py:func:`dynamo_consistency.backend.get_listers` reads the :ref:`consistency-config-ref`
file to determine the type of lister for a site.
There are currently three different classes implemented,
and more can be added by extending the :py:class:`dynamo_consistency.backend.listers.Lister` class and
implementing its `ls_directory` method.
The three current listers are the following:

* :py:class:`dynamo_consistency.backend.listers.XRootDLister` -
  This listing object uses the ``XRootD`` Python module to connect to and query each site.
* :py:class:`dynamo_consistency.backend.listers.GFalLister` -
  This listing object uses the ``gfal-ls`` command line tool to list remote sites.
* :py:class:`dynamo_consistency.backend.listers.XRootDLister` -
  This listing object opens a subshell using the ``xrdfs`` command line tool and queries the remote site.

Once the type of lister is set in the :ref:`consistency-config-ref`,
the contents of the remote site can be listed transparently::

  from dynamo_consistency import remotelister

  listing = remotelister.listing(sitename)

This takes much longer than the :ref:`inventory-listing-ref`, since every directory of the site needs to be queried.
The layer between the listing class and the final output creates multiple connections and works on two queues with multiple threads.
There is the input queue, which is a list of directories that still need to be listed, and
an output queue which holds the result of each directory listed so far.
The workflow of each queue is shown below.

.. tikz:: Listing algorithm. TODO: Make better colors and words and stuff
  :libs: arrows, positioning, intersections
  :include: listing.tikz
