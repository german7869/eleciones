#!/usr/bin/env python
"""Script para agregar el campo estado a las juntas"""
from sqlalchemy import text
from app.utils.db import SessionLocal

db = SessionLocal()

try:
    print("\nAgregando campo 'estado' a tabla juntas...\n")
    
    # Agregar columna estado si no existe
    db.execute(text("""
        ALTER TABLE juntas 
        ADD COLUMN IF NOT EXISTS estado VARCHAR(20) DEFAULT 'pendiente';
    """))
    db.commit()
    
    print("✓ Columna 'estado' agregada exitosamente")
    print("\n✅ Migración completada")
    
except Exception as e:
    db.rollback()
    print(f"❌ Error: {str(e)}")
finally:
    db.close()
