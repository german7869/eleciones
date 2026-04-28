#!/usr/bin/env python3
"""Restaurar recintos necesarios antes de importar juntas"""
import sys
sys.path.insert(0, '/app')

from app.utils.db import SessionLocal
from app.models import Parroquia, Zona, Recinto

db = SessionLocal()

try:
    # Limpiar datos existentes
    db.query(Recinto).delete()
    db.query(Zona).delete()
    db.query(Parroquia).delete()
    db.commit()
    print("✓ Base de datos limpia")
    
    # Crear parroquias
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
    print(f"✓ {len(parroquias)} parroquias creadas")
    
    # Crear zonas
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
    print(f"✓ {len(zonas)} zonas creadas")
    
    # Crear recintos (los necesarios para el archivo de 642 juntas)
    recintos = [
        Recinto(codigo="2", nombre="Recinto 2", zona_id=db.query(Zona).filter_by(codigo="1").first().id),
        Recinto(codigo="4", nombre="Recinto 4", zona_id=db.query(Zona).filter_by(codigo="1").first().id),
        Recinto(codigo="5", nombre="Recinto 5", zona_id=db.query(Zona).filter_by(codigo="1").first().id),
        Recinto(codigo="6", nombre="Recinto 6", zona_id=db.query(Zona).filter_by(codigo="1").first().id),
        Recinto(codigo="7", nombre="Recinto 7", zona_id=db.query(Zona).filter_by(codigo="2").first().id),
        Recinto(codigo="8", nombre="Recinto 8", zona_id=db.query(Zona).filter_by(codigo="2").first().id),
        Recinto(codigo="9", nombre="Recinto 9", zona_id=db.query(Zona).filter_by(codigo="2").first().id),
        Recinto(codigo="10", nombre="Recinto 10", zona_id=db.query(Zona).filter_by(codigo="2").first().id),
        Recinto(codigo="11", nombre="Recinto 11", zona_id=db.query(Zona).filter_by(codigo="3").first().id),
        Recinto(codigo="12", nombre="Recinto 12", zona_id=db.query(Zona).filter_by(codigo="3").first().id),
        Recinto(codigo="13", nombre="Recinto 13", zona_id=db.query(Zona).filter_by(codigo="3").first().id),
        Recinto(codigo="14", nombre="Recinto 14", zona_id=db.query(Zona).filter_by(codigo="3").first().id),
        Recinto(codigo="15", nombre="Recinto 15", zona_id=db.query(Zona).filter_by(codigo="4").first().id),
        Recinto(codigo="16", nombre="Recinto 16", zona_id=db.query(Zona).filter_by(codigo="4").first().id),
        Recinto(codigo="17", nombre="Recinto 17", zona_id=db.query(Zona).filter_by(codigo="4").first().id),
        Recinto(codigo="18", nombre="Recinto 18", zona_id=db.query(Zona).filter_by(codigo="5").first().id),
        Recinto(codigo="19", nombre="Recinto 19", zona_id=db.query(Zona).filter_by(codigo="5").first().id),
        Recinto(codigo="20", nombre="Recinto 20", zona_id=db.query(Zona).filter_by(codigo="5").first().id),
        Recinto(codigo="21", nombre="Recinto 21", zona_id=db.query(Zona).filter_by(codigo="5").first().id),
        Recinto(codigo="22", nombre="Recinto 22", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="23", nombre="Recinto 23", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="24", nombre="Recinto 24", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="25", nombre="Recinto 25", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="26", nombre="Recinto 26", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="27", nombre="Recinto 27", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="28", nombre="Recinto 28", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="29", nombre="Recinto 29", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="30", nombre="Recinto 30", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="31", nombre="Recinto 31", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="32", nombre="Recinto 32", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="33", nombre="Recinto 33", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="34", nombre="Recinto 34", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="35", nombre="Recinto 35", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="36", nombre="Recinto 36", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="37", nombre="Recinto 37", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="38", nombre="Recinto 38", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="39", nombre="Recinto 39", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="40", nombre="Recinto 40", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="41", nombre="Recinto 41", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="42", nombre="Recinto 42", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="43", nombre="Recinto 43", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="44", nombre="Recinto 44", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="45", nombre="Recinto 45", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="46", nombre="Recinto 46", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="47", nombre="Recinto 47", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="48", nombre="Recinto 48", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="49", nombre="Recinto 49", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="50", nombre="Recinto 50", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="51", nombre="Recinto 51", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="52", nombre="Recinto 52", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="53", nombre="Recinto 53", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="54", nombre="Recinto 54", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="55", nombre="Recinto 55", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="56", nombre="Recinto 56", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="57", nombre="Recinto 57", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="58", nombre="Recinto 58", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="59", nombre="Recinto 59", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="60", nombre="Recinto 60", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="61", nombre="Recinto 61", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="62", nombre="Recinto 62", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="63", nombre="Recinto 63", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="64", nombre="Recinto 64", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="65", nombre="Recinto 65", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="66", nombre="Recinto 66", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="67", nombre="Recinto 67", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="68", nombre="Recinto 68", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
        Recinto(codigo="69", nombre="Recinto 69", zona_id=db.query(Zona).filter_by(codigo="6").first().id),
    ]
    db.add_all(recintos)
    db.commit()
    print(f"✓ {len(recintos)} recintos creados")
    
    print("\n✅ Base de datos restaurada correctamente")
    
except Exception as e:
    print(f"❌ Error: {e}")
    db.close()
finally:
    db.close()
