.. _intro-ref:

Introduction
============

|build-status|

Dynamo Consistency is the consistency plugin for Dynamo Dynamic Data Management System.
Even though Dynamo controls and tracks the history of file transfers between computing sites,
a separate check is needed to ensure files are not lost or accumulated during user or system errors.
Sites that can no longer access files after a power outage, for example,
can cause other problems for the entire data management system.
Transfers requested from the site to another site will fail for missing files.
Sites are chosen incorrectly for production jobs that assume the presence of a local file.
Last disk copies may also be missing, causing a delay for user requests for data.
Another type of inconsistency is caused when files thought to be deleted are still on disk.
This leads to wasted disk space for files that are not accessed, except by accident.
Dynamo Consistency does its check by regularly listing each remote site and
comparing the listed contents to Dynamo's inventory database.

A single executable ``dynamo-consistency`` is provided to run the consistency check.
This executable can be used directly in Dynamo's scheduling system.
Most of the behaviour is controlled via a simple JSON configuration file,
with options for site selection, passed via command line arguments.
This allows Dynamo to run separate schedules for differing site architectures
in a heterogenous computing environment.
Advanced users can also directly use the Python API to run a custom consistency check.

These options allow multiple methods of listing a site's physical contents.
The following methods are currently implemented:

* Listing over XRootD Python bindings
* Listing over the ``gfal-ls`` CLI
* Listing through a ``xrdfs`` subshell

These listers are easily extensible in Python,
allowing for new site architectures to be checked by Dynamo Consistency as well.

The default executable performs the check as expected,
listing files that are not tracked by Dynamo as orphans
and listing files that are not found at sites as missing,
with the exception of some configurable filters.
Dynamo Consistency avoids listing orphan files that have a modifcation time that is recent.
Path patterns to avoid deleting can also be set.
Deletion and transfer requests that are queued by Dynamo provide another filter to the reporting.

In addition to tracking the consistency between Dynamo's inventory and physical site storage,
Dynamo Consistency can remotely list all files older than a certain age in general directories.
These files can also be filtered with path patterns.
This allows for cleaning of directories that are written to with a high frequency that Dynamo does not try to track.

A summary of results, as well as the run status, of the consistency check are displayed in a webpage.
The page consists of a table that includes links to logs and lists of orphan and missing files.
Cells are color coded to allow operators to quickly catch problematic sites.
Historic data for each site is also accessible through this page.

For more details on the Dynamo Consistency package, see https://dynamo-consistency.readthedocs.io.

.. |build-status| image:: https://travis-ci.org/SmartDataProjects/dynamo-consistency.svg?branch=master
   :target: https://travis-ci.org/SmartDataProjects/dynamo-consistency
