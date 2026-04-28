#!/usr/bin/env python3
"""Limpiar base de datos completamente - respetar foreign keys"""
import sys
sys.path.insert(0, '/app')

from app.utils.db import SessionLocal
from app.models import Junta, Recinto, Zona, Parroquia, Delegado

db = SessionLocal()

try:
    # Borrar en orden: Juntas primero (referencia Recintos), luego Recintos, Zonas, Parroquias
    print("🗑️  Limpiando juntas...")
    db.query(Junta).delete()
    db.commit()
    
    print("🗑️  Limpiando recintos...")
    db.query(Recinto).delete()
    db.commit()
    
    print("🗑️  Limpiando zonas...")
    db.query(Zona).delete()
    db.commit()
    
    print("🗑️  Limpiando parroquias...")
    db.query(Parroquia).delete()
    db.commit()
    
    # Crear parroquias
    print("✅ Creando parroquias...")
    parroquias = [
        Parroquia(codigo="1", nombre="JAMBELI"),
        Parroquia(codigo="2", nombre="EL CAMBIO"),
        Parroquia(codigo="3", nombre="PUERTO BOLIVAR"),
        Parroquia(codigo="4", nombre="EL RETIRO"),
        Parroquia(codigo="5", nombre="MACHALA"),
        Parroquia(codigo="6", nombre="LA PROVIDENCIA"),
        Parroquia(codigo="7", nombre="JUBONES"),
        Parroquia(codigo="8", nombre="9 DE MAYO"),
        Parroquia(codigo="9", nombre="FIN"),
    ]
    db.add_all(parroquias)
    db.commit()
    
    # Crear zonas
    print("✅ Creando zonas...")
    zonas = [
        Zona(codigo="1", nombre="Zona 1", parroquia_id=db.query(Parroquia).filter_by(codigo="1").first().id),
        Zona(codigo="2", nombre="Zona 2", parroquia_id=db.query(Parroquia).filter_by(codigo="2").first().id),
        Zona(codigo="3", nombre="Zona 3", parroquia_id=db.query(Parroquia).filter_by(codigo="3").first().id),
        Zona(codigo="4", nombre="Zona 4", parroquia_id=db.query(Parroquia).filter_by(codigo="4").first().id),
        Zona(codigo="5", nombre="Zona 5", parroquia_id=db.query(Parroquia).filter_by(codigo="5").first().id),
        Zona(codigo="6", nombre="Zona 6", parroquia_id=db.query(Parroquia).filter_by(codigo="6").first().id),
    ]
    db.add_all(zonas)
    db.commit()
    
    # Crear recintos
    print("✅ Creando recintos...")
    zona_6_id = db.query(Zona).filter_by(codigo="6").first().id
    recintos = [Recinto(codigo=str(i), nombre=f"Recinto {i}", zona_id=zona_6_id) for i in range(2, 70)]
    db.add_all(recintos)
    db.commit()
    
    print("✅ Base de datos limpiada y restaurada")
    
except Exception as e:
    print(f"❌ Error: {e}")
    db.close()
finally:
    db.close()
