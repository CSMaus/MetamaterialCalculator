import psycopg2
import json
import os

config_path = os.path.join(os.path.dirname(__file__), "config.json")
with open(config_path) as config_file:
    config = json.load(config_file)

DB_NAME = config["DB_NAME"] # materials_db
DB_USER = config["DB_USER"]
DB_PASS = config["DB_PASS"]
DB_HOST = config["DB_HOST"] # now localhost, bcs with local docker container
DB_PORT = config["DB_PORT"] # 5432

# to connect to DB in docker container
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
DEFAULT_DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/postgres"


def create_database_if_not_exists():
    conn = psycopg2.connect(DEFAULT_DB_URL)
    conn.autocommit = True  # to not call commit after each sql command
    cursor = conn.cursor()

    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}';")
    exists = cursor.fetchone()
    if not exists:
        cursor.execute(f"CREATE DATABASE {DB_NAME};")
        print(f"Database '{DB_NAME}' created successfully.")
    else:
        print(f"Database '{DB_NAME}' already exists.")
    cursor.close()
    conn.close()

def create_materials_table():
    """Creates the materials table if it does not exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS materials (
            id SERIAL PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            material_type TEXT NOT NULL,
            user_added TEXT NOT NULL,
            producer TEXT NOT NULL,
            properties JSONB NOT NULL
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()
    print("Materials table is ready.")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def initialize_database():
    create_database_if_not_exists()
    create_materials_table()


# Database Schema for materials Table
# 	•	id → Unique identifier (Primary Key)
# 	•	name → Material name
# 	•	type → Porous or Solid
# 	•	user_added → Username who added the material
# 	•	producer → Name of the material producer
# 	•	Material Properties (columns depend on type)


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
