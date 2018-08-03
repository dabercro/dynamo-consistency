Operations
==========

Moving Sites To and From Debugged Tab
+++++++++++++++++++++++++++++++++++++

To mark sites as ready to be acted on,
change the ``isgood`` value in the ``sites`` table in the summary database to ``1``.
For example, if you are in the directory of your webpage,
and want to mark ``T2_US_MIT`` as good, you could do the following::

    echo "UPDATE sites SET isgood = 1 WHERE site = 'T2_US_MIT';" | sqlite3 stats.db

To mark a site as bad, set ``isgood`` to ``0``::

    echo "UPDATE sites SET isgood = 0 WHERE site = 'T2_US_MIT';" | sqlite3 stats.db
