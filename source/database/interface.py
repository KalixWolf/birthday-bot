"""SQLite Database Interface

Functions for connecting to and interacting with the database.
"""

import sqlite3
from pathlib import Path

class Connect():
    """Context Manager for database connections. Optionally pass in database name to use.
    
    The context manager automatically commits and closes the connection. The returned object is a
    SQLite3 cursor object.
    """

    def __init__(self, db_name="store.db"):
        self.db_path = Path(Path(__file__).parent.absolute() / db_name)
        self.connection = None

    def __enter__(self) -> sqlite3.Cursor:
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.connection.commit()
        self.connection.close()


def initialize():
    """Create the database and initialize table structure"""

    with Connect() as con:
        con.execute(  # create Users table
            '''CREATE TABLE "Users" (
                "ID"	INTEGER NOT NULL UNIQUE,
                "BIRTHDATE"	TEXT NOT NULL,
                "SERVERS"	TEXT,
                PRIMARY KEY("ID")
            )'''
        )

        con.execute(
            '''CREATE TABLE "Servers" (
                "ID"	INTEGER NOT NULL UNIQUE,
                "CHANNEL"	INTEGER NOT NULL,
                PRIMARY KEY("ID")
            )'''
        )


def set_user(discord_id: int, server, birthdate: str):
    """Create or update a user record

    This function should really only be triggered by a discord command to set user birth date.

    Args:
        discord_id (int): Discord user id number
        server ([type]): Discord server id where request was sent from
        birthdate (str): Request parameter, should be in the format 'mm/dd'
    """

    with Connect() as con:
        con.execute("SELECT 1 FROM Users WHERE ID=:id", {"id": discord_id})
        if con.fetchall():  # modify existing record
            con.execute("SELECT SERVERS FROM Users WHERE ID=:id", {"id": discord_id})
            server_list = con.fetchall()[0][0].split(',')  # list of servers (server value in db should be comma-separated)
            if str(server) not in server_list:  # append this server if necessary
                server_list.append(str(server))

            con.execute(
                '''UPDATE Users
                    SET BIRTHDATE = ?, SERVERS = ?
                    WHERE ID = ?''',
                (birthdate, ','.join(server_list), discord_id)
            )
        else:  # new record
            con.execute('INSERT INTO Users VALUES (?, ?, ?)', (discord_id, birthdate, str(server)))


def rem_user(discord_id: int):
    """Remove a record for a discord user

    Args:
        discord_id (int): Discord user id number
    """

    with Connect() as con:
        con.execute('DELETE FROM Users WHERE ID=:id', {"id": discord_id})


def query_user(discord_id: int) -> tuple:
    """Query database and return user data

    Returns None if the record doesn't exist

    Args:
        discord_id (int): Discord user id number

    Returns:
        tuple: Database record
    """

    with Connect() as con:
        con.execute('SELECT * FROM Users WHERE ID=:id', {"id": discord_id})
        try:
            record = con.fetchall()[0]
        except IndexError:  # no record
            record = None

    return record


def set_server(server_id: int, channel_id: int):
    """Create or update server channel record

    Args:
        server_id (int): Discord server id number
        channel_id (int): Discord server channel id number. Must belong to server_id
    """

    with Connect() as con:
        con.execute('SELECT 1 FROM Servers WHERE ID=:id', {"id": server_id})
        if con.fetchall():
            con.execute('UPDATE Servers SET CHANNEL = ? WHERE ID = ?', (channel_id, server_id))
        else:
            con.execute('INSERT INTO Servers VALUES (?, ?)', (server_id, channel_id))


def query_server(server_id: int) -> tuple:
    """Query database and return record for server

    Args:
        server_id (int): Discord server id number

    Returns:
        tuple: Server record
    """

    with Connect() as con:
        con.execute('SELECT * FROM Servers WHERE ID=:id', {"id": server_id})
        try:
            record = con.fetchall()[0]
        except IndexError:
            record = None

    return record
