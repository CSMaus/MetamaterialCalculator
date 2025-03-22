# here will be definitions for tables

def create_materials_table():
    """Creates the materials table if it does not exist"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS materials (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            density FLOAT NOT NULL,
            elasticity FLOAT NOT NULL,
            conductivity FLOAT NOT NULL
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

# python -c "from backend.models import create_materials_table; create_materials_table()"
