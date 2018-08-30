"""
Handles the invalidation of files through a separate read-write process
"""

import sqlite3

from . import config

# Never change these. Will break database.
NEW = 0
OLD = 1

def _connect():
    """
    :returns: A connection to the consistency database, along with a cursor.
              It creates the invalid table, if needed.

              .. note::

                 This connection needs to be closed by the caller

    :rtype: sqlite3.Connection, sqlite3.Cursor
    """

    dbname = os.path.join(config.vardir('db'), 'consistency.db')

    conn = sqlite3.connect(dbname)

    curs = conn.cursor()
    curs.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="invalid"')

    if not curs.fetchone():
        curs.execute(
            """
            CREATE TABLE invalid (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              site VARCHAR (128),
              file VARCHAR (1024),
              entered DATETIME DEFAULT NOW(),
              status INT DEFAULT 0
            );
            """)

    return conn, curs


def report_missing(site, missing):
    conn, curs = _connect()

    curs.execute_many('INSERT INTO invalid (site, missing) VALUES (?, ?)',
                      [(site, miss) for miss in missing])

    conn.commit()
    conn.close()


def missing_files(site, acting):
    conn, curs = _connect()



    conn.commit()
    conn.close()
