#!/usr/bin/env python
"""Script para inicializar la BD y crear usuario administrador"""
import os
import sys
import bcrypt
from app.utils.db import engine, Base, SessionLocal
from app.utils.init_db import init_db
from app.models.delegado import Delegado

def hash_password_bcrypt(password: str) -> str:
    """Hash una contraseña usando bcrypt directamente (compatible con passlib)"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12)).decode()

def create_admin_user(email: str, password: str):
    """Crear usuario administrador"""
    # Crear tablas
    print("Creando tablas...")
    init_db()
    print("✓ Tablas creadas correctamente")
    
    # Crear sesión
    db = SessionLocal()
    
    try:
        # Verificar si el usuario ya existe
        existing_user = db.query(Delegado).filter(Delegado.cedula == email).first()
        if existing_user:
            print(f"✗ El usuario {email} ya existe, eliminando...")
            db.delete(existing_user)
            db.commit()
        
        # Crear usuario con bcrypt
        hashed_password = hash_password_bcrypt(password)
        print(f"Debug - Hash generado: {hashed_password[:50]}...")
        
        admin_user = Delegado(
            nombre="Administrador",
            cedula=email,
            telefono="",
            password=hashed_password,
            rol="admin"
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print(f"✓ Usuario administrador creado:")
        print(f"  - Cédula/Email: {email}")
        print(f"  - Contraseña: {password}")
        print(f"  - Rol: admin")
        print(f"  - ID: {admin_user.id}")
        
        return True
    
    except Exception as e:
        db.rollback()
        print(f"✗ Error al crear usuario: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    # Esperar a que la BD esté lista
    import time
    from sqlalchemy import text
    
    max_retries = 30
    for attempt in range(max_retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("✓ Base de datos conectada")
            break
        except Exception as e:
            print(f"Esperando a la BD... ({attempt+1}/{max_retries})")
            time.sleep(1)
    else:
        print("✗ No se pudo conectar a la base de datos")
        sys.exit(1)
    
    # Leer credenciales desde variables de entorno
    admin_email = os.getenv("ADMIN_EMAIL", "germandase@gmail.com")
    admin_password = os.getenv("ADMIN_PASSWORD", "jedase7869")
    
    # Crear usuario administrador
    success = create_admin_user(admin_email, admin_password)
    sys.exit(0 if success else 1)
