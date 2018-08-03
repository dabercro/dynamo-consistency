Running Over CMS Sites
======================

.. _consistency-config-ref:

Configuration
+++++++++++++

A configuration file should be created before pointing to it, like above.
The configuration file for Site Consistency is a JSON or YAML file with the following keys

.. autoanysrc:: phony
   :src: ../test/config.yml
   :analyzer: shell-script

Configuration parameters can also be quickly overwritten for a given run by
setting an environment variable of the same name.

Production Settings
-------------------

The configuration in production is the following.

.. program-output:: cat ../prod/consistency_config.json

.. _compare-ref:

Comparison Script
+++++++++++++++++

.. Note::
   The following script description was last updated on April 11, 2018.

The production script,
located at ``dynamo_consistency/prod/compare.py`` at the time of writing,
goes through the following steps for each site.

  #. Points :ref:`config-ref` to the local ``consistency_config.json`` file
  #. Notes the time, and if it's daylight savings time for entry into the summary database
  #. Reads the list of previous missing files, since it requires a file to be missing on multiple
     runs before registering it to be copied
  #. It gathers the inventory tree by calling
     :py:func:`dynamo_consistency.getinventorycontents.get_db_listing()`.
  #. Creates a list of datasets to not report missing files in.
     This list consists of the following.

     - Deletion requests fetched from PhEDEx by
       :py:func:`dynamo_consistency.checkphedex.set_of_deletions()`

  #. It creates a list of datasets to not report orphans in.
     This list consists of the following.

     - Datasets that have any files on the site, as listed by the dynamo MySQL database
     - Deletion requests fetched from PhEDEx (same list as datasets to skip in missing)
     - Any datasets that have the status flag set to ``'IGNORED'`` in the dynamo database
     - Merging datasets that are
       `protected by Unified <https://cmst2.web.cern.ch/cmst2/unified/listProtectedLFN.txt>`_

  #. It gathers the site tree by calling
     :py:func:`dynamo_consistency.getsitecontents.get_site_tree()`.
     The list of orphans is used during the running to filter out empty directories that are
     reported to the registry during the run.
  #. Does the comparison between the two trees made,
     using the configuration options listed under
     :ref:`consistency-config-ref` concerning file age.
  #. If the number of missing files is less than **MaxMissing**,
     the number of orphans is less than **MaxOrphan**,
     and the site is under the webpage's "Debugged sites" tab,
     connects to a dynamo registry to report the following errors:

     - Every orphan file and every empty directory that is not too new
       nor should contain missing files is entered in the deletion queue.
     - For each missing file, every possible source site as listed by the dynamo database,
       (not counting the site where missing), is entered in the transfer queue.
       Creates a text file full of files that only exist elsewhere on tape.

  #. Creates a text file that contains the missing blocks and groups.
  #. ``.txt`` file lists and details of orphan and missing files are moved to the web space
  #. If the site is listed in the configuration under the **Unmerged** list,
     the unmerged cleaner is run over the site:

     - :py:func:`dynamo_consistency.getsitecontents.get_site_tree()` is run again,
       this time only over ``/store/unmerged``
     - Empty directories that are not too new nor
       `protected by Unified <https://cmst2.web.cern.ch/cmst2/unified/listProtectedLFN.txt>`_
       are entered into the deletion queue
     - The list of files is passed through the `Unmerged Cleaner
       <http://cms-comp-ops-tools.readthedocs.io/en/latest/siteadmintoolkit.html#unmerged-cleaner>`_
     - The list of files to delete from `Unmerged Cleaner
       <http://cms-comp-ops-tools.readthedocs.io/en/latest/siteadmintoolkit.html#unmerged-cleaner>`_
       are entered in the deletion queue

  #. The summary database is updated to show the last update on the website


Automatic Site Selection
------------------------

To automatically run ``prod/compare.py`` over a few well-deserving sites, use ``prod/run_checks.sh``.

.. autoanysrc:: phony
   :src: ../prod/run_checks.sh
   :analyzer: perl-script

Manually Setting XRootD Doors
+++++++++++++++++++++++++++++

In addition to the **Redirectors** key in the configuration file, which sets the redirector for a site,
there is also a mechanism for setting all the doors for a site.
A list of possible doors can be found at ``<CacheLocation>/<SiteName>_redirector_list.txt``.
Any url in that list that matches the domain of the site will be used to make ``xrootd`` calls.
To add or remove urls from this list, just add or remove lines from this file.

.. Note::
   If the **RedirectorAge** configuration parameter is not set to ``0``,
   then this redirector list will be overwritten once it becomes too old.
   To force the generation of a new list when the **RedirectorAge** is set to ``0``,
   simply delete the redirector list file for that site.

A list of redirectors found by the global redirectors is stored in ``<CacheLocation>/redirector_list.txt``.
