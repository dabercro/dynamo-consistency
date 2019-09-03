.. _intro-ref:

Introduction
============

|build-status|

Dynamo Consistency is a plugin for Dynamo Dynamic Data Management System that checks
consistency between Dynamo's inventory and files actually located at managed sites.
Even though Dynamo controls and tracks the history of file transfers between computing sites,
a separate check is needed to ensure files are not lost or accumulated due to user or system errors.
For example, sites that can no longer access some files after a power outage
can cause problems for many related activities.
File transfers requested from a inconsistent site to another site will fail when files are missing.
Sites will be chosen incorrectly for production jobs that assume the presence of a local file.
Last disk copies may also be missing, causing a delay when a user requests data.
Another type of inconsistency arises when files thought to be deleted are still on disk.
This leads to wasted disk space for files that are not accessed, except by accident.
Dynamo Consistency regularly checks consistency by listing each remote site and
comparing the listed contents to Dynamo's inventory database.
The results are reported back to Dynamo, which can then take corrective measures.

A single executable ``dynamo-consistency`` is provided to run the consistency check.
This executable can be used directly in Dynamo's scheduling system.
Most of the behaviour is controlled via a simple JSON configuration file,
with options for site selection, passed via command line arguments.
This allows Dynamo to run separate schedules for differing site architectures.

Because Dynamo runs in a heterogenous computing environment,
different sites need to be listed remotely using different methods.
Currently implemented are listings using XRootD Python bindings, the ``gfal-ls`` CLI, and a ``xrdfs`` subshell.
These listers are easily extensible in Python,
allowing for new site architectures to be checked by Dynamo Consistency as well.

The default executable performs the check as expected,
listing files that are not tracked by Dynamo as orphans
and listing files that are not found at sites as missing,
with the exception of a few configurable filters.
Dynamo Consistency avoids listing orphan files that have a modification time that is recent.
Paths to avoid deleting can also be set.
Deletion and transfer requests that are queued are also used to filter the final report
to avoid redundant actions from Dynamo.

In addition to tracking the consistency between Dynamo's inventory and physical site storage,
Dynamo Consistency can report all remote files older than a certain age in general directories.
These files can also be filtered with path patterns, just as the regular consistency check.
The time-based only reporting allows for cleaning of directories that Dynamo does not track.
This is a setting recommended for large file systems that are written to with a high frequency.

Summaries of check results, as well as the statuses of running checks, are displayed in a webpage.
The page consists of a table that includes links to logs and lists of orphan and missing files.
Cells are color coded to allow operators to quickly identify problematic sites.
Historic summary data for each site is also accessible through this page.

If the available configuration options and listers are not enough,
advanced users can also directly use the Python API to run a custom consistency check.
For more details on the Dynamo Consistency package, see https://dynamo-consistency.readthedocs.io.

.. |build-status| image:: https://travis-ci.org/SmartDataProjects/dynamo-consistency.svg?branch=master
   :target: https://travis-ci.org/SmartDataProjects/dynamo-consistency
