from kseni.backend.crud import insert_material

insert_material(
    name="Test Material",
    material_type="Porous",
    user_added="admin",
    producer="Test Inc",
    properties={"density": 0.3, "stiffness": 7.2}
)




