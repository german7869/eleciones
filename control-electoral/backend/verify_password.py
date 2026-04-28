from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.models.delegado import Delegado
import bcrypt
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://elector:passwd@db:5432/elector_db')
engine = create_engine(DATABASE_URL)

with Session(engine) as db:
    d = db.query(Delegado).filter(Delegado.cedula == 'delegado1@example.com').first()
    if d:
        print(f"✓ Delegado encontrado: {d.nombre}")
        print(f"  Cedula: {d.cedula}")
        print(f"  Rol: {d.rol}")
        print(f"  Password type: {type(d.password)}")
        print(f"  Password hash: {d.password[:50] if d.password else 'NULL'}...")
        
        # Verificar contraseña
        if d.password:
            try:
                is_correct = bcrypt.checkpw('delegado123'.encode(), d.password.encode())
                print(f"  ✓ Contraseña correcta: {is_correct}")
            except Exception as e:
                print(f"  ✗ Error verificando: {e}")
        else:
            print(f"  ✗ No hay contraseña almacenada")
    else:
        print("✗ Delegado no encontrado")
        
        # Listar todos
        print("\nDelegados en BD:")
        all_d = db.query(Delegado).all()
        for d in all_d:
            print(f"  - {d.nombre} ({d.cedula})")
