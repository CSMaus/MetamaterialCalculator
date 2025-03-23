# reading/writing materials data
import pandas as pd
from .database import get_connection, DB_USER
import json

user_name = DB_USER

def material_exists(material_name):
    """Check if material already exists in the database"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM materials WHERE name = %s;", (material_name,))
    exists = cursor.fetchone()[0] > 0
    cursor.close()
    conn.close()
    return exists


def insert_material(name, material_type, user_added, producer, properties):
    if material_exists(name):
        print(f"Material '{name}' already exists in the database. Skipping insertion.")
        return

    conn = get_connection()
    cursor = conn.cursor()
    properties_json = json.dumps(properties)

    cursor.execute("""
        INSERT INTO materials (name, material_type, user_added, producer, properties) 
        VALUES (%s, %s, %s, %s, %s);
    """, (name, material_type, user_added, producer, properties_json))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Material '{name}' added to the database.")

# insert_material("Porous Foam", "Porous", "admin", "FoamCorp", {"density": 100, "porosity": 0.9})

def get_materials():
    """Fetch all materials and load into a pandas DataFrame"""
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM materials;", conn)
    # pd.set_option("display.max_colwidth", None)
    # df["properties"] = df["properties"].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
    conn.close()
    return df

