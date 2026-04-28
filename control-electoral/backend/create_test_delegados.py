#!/usr/bin/env python
"""Script para crear delegados de prueba"""
import bcrypt
from app.models.delegado import Delegado
from app.utils.db import SessionLocal

def hash_password(password: str) -> str:
    """Hash una contraseña usando bcrypt"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12)).decode()

delegados_data = [
    {"nombre": "Delegado 1", "cedula": "delegado1@gmail.com", "password": "delegado123"},
    {"nombre": "Delegado 2", "cedula": "delegado2@gmail.com", "password": "delegado123"},
    {"nombre": "Delegado 3", "cedula": "delegado3@gmail.com", "password": "delegado123"},
]

db = SessionLocal()

try:
    print("\nCreando delegados de prueba...\n")
    
    for data in delegados_data:
        # Verificar si existe
        existing = db.query(Delegado).filter(Delegado.cedula == data["cedula"]).first()
        if existing:
            db.delete(existing)
            db.commit()
        
        # Crear nuevo delegado
        hashed_password = hash_password(data["password"])
        delegado = Delegado(
            nombre=data["nombre"],
            cedula=data["cedula"],
            telefono="",
            password=hashed_password,
            rol="delegado"
        )
        db.add(delegado)
        db.commit()
        db.refresh(delegado)
        
        print(f"✓ {data['nombre']}")
        print(f"  Email: {data['cedula']}")
        print(f"  Contraseña: {data['password']}")
        print(f"  ID: {delegado.id}\n")
    
    print("✅ Delegados creados exitosamente")
    
finally:
    db.close()
