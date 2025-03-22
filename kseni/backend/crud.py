# reading/writing materials data

import pandas as pd
from database import get_connection

def insert_material(name, density, elasticity, conductivity):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO materials (name, density, elasticity, conductivity) 
        VALUES (%s, %s, %s, %s);
    """, (name, density, elasticity, conductivity))
    conn.commit()
    cursor.close()
    conn.close()


def get_materials():
    """Fetches materials and loads them into a pandas DataFrame"""
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM materials;", conn)
    conn.close()
    return df

