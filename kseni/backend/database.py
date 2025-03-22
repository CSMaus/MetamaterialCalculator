import psycopg2

import psycopg2

# read and set all parameters from txt from gitignore
DB_NAME = "metamaterial_db"
DB_USER = ""
DB_PASS = ""
DB_HOST = "localhost" # it will be changed for web
DB_PORT = "5432"

def get_connection():
    """Establish a database connection"""
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )

# start sql manually: pg_ctl -D /opt/homebrew/var/postgres start
# start each time when turn on: brew services start postgresql@14
# to stop - just change to stop
# check status: pg_ctl -D /opt/homebrew/var/postgresql@14 status
# to check if it's started: brew services list
# running processes: ps aux | grep postgres
# to check where is log: ls /opt/homebrew/var/
# connect to PostgreSQL: psql postgres


# Now, after connecting to it, let's create database:
# CREATE DATABASE metamaterial_db;
# \c metamaterial_db
