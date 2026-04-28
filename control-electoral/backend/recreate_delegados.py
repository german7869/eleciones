from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.models.delegado import Delegado
from app.api.delegado import hash_password
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://elector:passwd@db:5432/elector_db')
engine = create_engine(DATABASE_URL)

# Limpiar delegados existentes
with Session(engine) as db:
    db.query(Delegado).delete()
    db.commit()
    print("✓ Delegados eliminados")

# Crear nuevos con contraseñas
test_data = [
    {"nombre": "Delegado 1", "cedula": "delegado1@example.com", "password": "delegado123", "rol": "delegado"},
    {"nombre": "Delegado 2", "cedula": "delegado2@example.com", "password": "delegado123", "rol": "delegado"},
    {"nombre": "Delegado 3", "cedula": "delegado3@example.com", "password": "delegado123", "rol": "delegado"},
    {"nombre": "Administrador", "cedula": "germandase@gmail.com", "password": "jedase7869", "rol": "admin"},
]

with Session(engine) as db:
    for data in test_data:
        plaintext = data.pop("password")
        d = Delegado(**data, password=hash_password(plaintext))
        db.add(d)
    db.commit()
    print("✓ Delegados creados")
    
    # Verificar que fueron creados
    delegados = db.query(Delegado).all()
    for d in delegados:
        print(f"  - {d.nombre} ({d.cedula})")
