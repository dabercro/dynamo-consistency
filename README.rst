ConsistencyCheck
================

Compares files on site to files on the PhEDEx database.
Requires Python 2.6 or higher (for the json module).

The basic syntax is::

    python ConsistencyCheck.py -T [SITE NAME]

e.g.::

    python ConsistencyCheck.py -T T2_US_MIT

To list the actions of other options do::

    python ConsistencyCheck.py -h

For the most part, these options control whether or not you use 
cached files, which you won't have at the beginning anyway.

Alternatively, you can use the configuration file::

    python ConsistencyCheck.py -c example.cfg

The example.cfg file given though will only work on the 
T2_US_MIT site though. Chances are you will have to edit 
the SiteName field. (Unless you are Max.)
The configuration file is pretty heavily commented, so 
hopefully it makes sense.

Also, the configuration file can be used to clear the site
after the ConsistencyCheck.py has been run. Again, those fields
have plenty of comments::

    python ClearSite.py -c example.cfg

Without using the configuration file
though, you would use the following syntax::

    python ClearSite.py -T [SITE NAME]

e.g.::

    python ClearSite.py -T T2_US_MIT

Run the following command to not pause for every directory::

    python ClearSite.py --fast -T [SITE NAME]

Run the following command to just give output of what will be deleted, 
witout actually removing anything::

    python ClearSite.py --safe -T [SITE NAME]

or::

    python ClearSite.py --safe --fast -T [SITE NAME]