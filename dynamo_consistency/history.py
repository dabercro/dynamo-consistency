"""
Handles the invalidation of files through a separate read-write process
"""

import os
import sqlite3

from . import config


class NotRunning(Exception):
    """
    An exception to throw when inserting results, but no run has been started
    """
    pass


RUN = 0


def _connect(running=False):
    """
    :param bool running: This connection should only be done if running.
    :returns: A connection to the consistency database, along with a cursor.
              It creates the invalid table, if needed.

              .. note::

                 This connection needs to be closed by the caller

    :rtype: sqlite3.Connection, sqlite3.Cursor
    :raises NotRunning: If `running` is `True`
                        and the global `RUN` hasn't been set.
    """

    if running and not RUN:
        raise NotRunning('Not running. Bad call to update DB.')

    dbname = os.path.join(config.vardir('db'), 'consistency.db')

    new = not os.path.exists(dbname)

    conn = sqlite3.connect(dbname)
    curs = conn.cursor()

    if new:
        with open(os.path.join(
                os.path.dirname(__file__),
                'report_schema.sql'), 'r') as script_file:
            script_text = ''.join(script_file)

        curs.executescript(script_text)

    return conn, curs


def start_run():
    """
    Called in :py:func:dynamo_consistency.main.main`
    to register the start of a consistency run
    """

    global RUN # pylint: disable=global-statement

    conn, curs = _connect()

    curs.execute('INSERT OR IGNORE INTO sites (`name`) VALUES (?)',
                 (config.SITE, ))
    curs.execute("""
                 INSERT INTO runs (`site`)
                 SELECT rowid FROM sites WHERE name = ?
                 """, (config.SITE, ))

    curs.execute("""
                 SELECT runs.rowid FROM runs
                 LEFT JOIN sites ON sites.rowid = runs.site
                 WHERE sites.name = ?
                 ORDER BY runs.rowid DESC
                 LIMIT 1
                 """, (config.SITE, ))

    RUN = curs.fetchone()[0]

    conn.commit()
    conn.close()


def finish_run():
    """
    Called in :py:func:dynamo_consistency.main.main`
    to register the end of a consistency run
    """
    
    global RUN # pylint: disable=global-statement
    conn, curs = _connect(True)

    curs.execute("""
                 UPDATE runs SET finished = DATETIME('NOW', 'LOCALTIME')
                 WHERE rowid = ?
                 """, (RUN, ))

    RUN = None

    conn.commit()
    conn.close()


def report_missing(missing):
    conn, curs = _connect(True)

    curs.executemany(
        """
        INSERT INTO invalid (site, run, name, size)
        VALUES ((SELECT rowid FROM sites WHERE name = ?), ?, ?, ?)
        """,
        [(config.SITE, RUN, miss, size) for miss, size in missing])

    conn.commit()
    conn.close()


def missing_files(site, acting=False):
    conn, curs = _connect()

    curs.execute(
        """
        SELECT invalid.name FROM invalid
        LEFT JOIN sites ON sites.rowid = invalid.site
        WHERE sites.name = ?
        ORDER BY invalid.name
        """, (site, ))

    output = list([out[0] for out in curs.fetchall()])

    if acting:
        curs.execute(
            """
            INSERT INTO invalid_history
            (site, run, name, size, entered, acted)
            SELECT site, run, invalid.name, size, entered, 1
            FROM invalid
            LEFT JOIN sites ON sites.rowid = invalid.site
            WHERE sites.name = ?
            """, (site, )
            )
        curs.execute(
            """
            DELETE FROM invalid
            WHERE site IN (
              SELECT rowid FROM sites
              WHERE sites.name = ?
            )
            """, (site, ))

    conn.commit()
    conn.close()

    return output
