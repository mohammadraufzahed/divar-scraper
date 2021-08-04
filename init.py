import sys

import psycopg2
from stdiomask import getpass


def init() -> None:
    """
    Initialize the required files and database
    """
    # Initial the database variable
    conn = None
    # Take the database information from the user
    DB_HOST = str(input("Database Host: "))
    DB_USER = str(input("Database User: "))
    DB_PASSWORD = getpass(prompt="Database Password: ")
    DB_NAME = input("Database Name: ")
    # Try to connect to the database
    try:
        conn = psycopg2.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname="postgres")
        conn.autocommit = True
    # If an exception is thrown print the error
    except Exception:
        print("Database information was wrong")
        sys.exit()
    # Create database cursor
    cur = conn.cursor()
    # Try to create a database and initialize it
    cur.execute("SET client_min_messages TO WARNING")
    cur.execute("DROP DATABASE IF EXISTS {}".format(DB_NAME))
    cur.execute("CREATE DATABASE {} ENCODING 'UTF8'".format(DB_NAME))
    conn.commit()
    cur.close()
    conn.close()
    newConn = psycopg2.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME
    )
    newCur = newConn.cursor()
    newCur.execute("SET client_min_messages TO WARNING")
    with open('db.sql', 'r', encoding="utf8") as dbQuery:
        newCur.execute(dbQuery.read())
    newConn.commit()
    newCur.close()
    newConn.close()
    # Write the database information into the file
    with open('config.py', 'w+', encoding="utf8") as configFile:
        data = f"""
\"\"\"
This file contains the database information
\"\"\"
DB_HOST = str("{DB_HOST}")
DB_USER = str("{DB_USER}")
DB_PASSWORD = str("{DB_PASSWORD}")
DB_NAME = str("{DB_NAME}")
                """
        configFile.write(data)
        configFile.close()
    print("Database and required files initialized")
