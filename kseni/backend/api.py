# FasAPI based for remaking into webApp
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from calculator import calculate_properties
from crud import get_materials, insert_material

app = FastAPI()

@app.get("/calculate/")
def get_calculation(param1: float, param2: float):
    result = calculate_properties(param1, param2)
    return {"result": result}

@app.get("/materials/")
def fetch_materials():
    """Fetch all materials as JSON"""
    return get_materials().to_dict(orient="records")

@app.post("/materials/")
def add_material(name: str, density: float, elasticity: float, conductivity: float):
    """Add a new material to the database"""
    insert_material(name, density, elasticity, conductivity)
    return {"message": "Material added successfully"}

# @app.post("/")
# uvicorn backend.api:app --reload
# http://127.0.0.1:8000/materials/ - Fetch materials
# http://127.0.0.1:8000/docs - Test API in Swagger UI

