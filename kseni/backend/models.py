# here will be definitions for DataBase tables
from database import get_connection


def create_materials_table():
    """Creates the materials table if it does not exist"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS materials (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            material_type TEXT NOT NULL,
            user_added TEXT NOT NULL,
            producer TEXT NOT NULL,
            properties JSONB NOT NULL
        );
    """)

    conn.commit()
    cursor.close()
    conn.close()

# to create table via cmd:
# python -c "from backend.models import create_materials_table; create_materials_table()"
