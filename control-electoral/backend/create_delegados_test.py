#!/usr/bin/env python3
"""Script para crear delegados de prueba"""
import sys
sys.path.insert(0, '/app')

from app.utils.db import SessionLocal
from app.models.delegado import Delegado
from app.api.delegado import hash_password

db = SessionLocal()

try:
    # Verificar si ya existen delegados
    delegados_existentes = db.query(Delegado).all()
    if delegados_existentes:
        print(f"✓ Ya existen {len(delegados_existentes)} delegados en la BD")
        for d in delegados_existentes:
            print(f"  - {d.nombre} ({d.cedula}) - Juntas: {len(d.juntas)}")
        db.close()
        exit(0)
    
    # Crear delegados de prueba
    delegados_crear = [
        Delegado(
            nombre="Juan Pérez García",
            cedula="1234567890",
            telefono="0987654321",
            password=hash_password("delegado123"),
            rol="delegado"
        ),
        Delegado(
            nombre="María López Martínez",
            cedula="0987654321",
            telefono="0912345678",
            password=hash_password("delegado123"),
            rol="delegado"
        ),
        Delegado(
            nombre="Carlos Rodríguez Sánchez",
            cedula="1122334455",
            telefono="0921234567",
            password=hash_password("delegado123"),
            rol="delegado"
        ),
        Delegado(
            nombre="Ana González López",
            cedula="5544332211",
            telefono="0934567890",
            password=hash_password("delegado123"),
            rol="delegado"
        ),
        Delegado(
            nombre="Pedro Fernández Díaz",
            cedula="6677889900",
            telefono="0945678901",
            password=hash_password("delegado123"),
            rol="delegado"
        ),
    ]
    
    db.add_all(delegados_crear)
    db.commit()
    
    print(f"✓ {len(delegados_crear)} delegados creados exitosamente:")
    for d in delegados_crear:
        print(f"  - {d.nombre} ({d.cedula})")
    
    print("\n📝 Credenciales para los delegados:")
    print("   Contraseña: delegado123")
    
except Exception as e:
    print(f"❌ Error: {e}")
    db.close()
finally:
    db.close()
