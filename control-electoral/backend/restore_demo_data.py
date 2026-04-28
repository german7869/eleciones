#!/usr/bin/env python
"""Script para restaurar datos de ejemplo después de limpiar la BD"""
import bcrypt
from app.utils.db import SessionLocal
from app.models.territorial import Parroquia, Zona, Recinto, Junta
from app.models.delegado import Delegado
from app.models.partido_candidato import Partido, Candidato

def hash_password(password: str) -> str:
    """Hash de contraseña con bcrypt"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12)).decode()

def restore_data():
    """Restaurar datos de ejemplo"""
    db = SessionLocal()
    
    try:
        # 1. Crear Partidos
        print("📋 Creando partidos...")
        partidos = [
            Partido(codigo="AD", nombre="Acción Democrática"),
            Partido(codigo="COPEI", nombre="COPEI"),
            Partido(codigo="MUD", nombre="Mesa de la Unidad"),
            Partido(codigo="PCV", nombre="Partido Comunista"),
            Partido(codigo="LCR", nombre="Lapso de Cambio Radical"),
        ]
        db.add_all(partidos)
        db.commit()
        print(f"✓ {len(partidos)} partidos creados")
        
        # 2. Crear Candidatos
        print("📋 Creando candidatos...")
        candidatos = [
            Candidato(nombre="Juan Pérez", partido_id=1, orden_papeleta=1),
            Candidato(nombre="María García", partido_id=1, orden_papeleta=2),
            Candidato(nombre="Carlos López", partido_id=2, orden_papeleta=3),
            Candidato(nombre="Ana Martínez", partido_id=2, orden_papeleta=4),
            Candidato(nombre="Diego Rodríguez", partido_id=3, orden_papeleta=5),
        ]
        db.add_all(candidatos)
        db.commit()
        print(f"✓ {len(candidatos)} candidatos creados")
        
        # 3. Crear Delegados (usuarios de delegado)
        print("👤 Creando delegados...")
        delegados = [
            Delegado(
                nombre="Delegado 1",
                cedula="delegado1@example.com",
                telefono="0414-1111111",
                password=hash_password("passwd123"),
                rol="delegado"
            ),
            Delegado(
                nombre="Delegado 2",
                cedula="delegado2@example.com",
                telefono="0414-2222222",
                password=hash_password("passwd123"),
                rol="delegado"
            ),
            Delegado(
                nombre="Delegado 3",
                cedula="delegado3@example.com",
                telefono="0414-3333333",
                password=hash_password("passwd123"),
                rol="delegado"
            ),
        ]
        db.add_all(delegados)
        db.commit()
        print(f"✓ {len(delegados)} delegados creados (contraseña: passwd123)")
        
        # 4. Crear Territorios
        print("🗺️ Creando territorios...")
        
        # Parroquias
        parroquias = [
            Parroquia(codigo="001", nombre="Parroquia Centro", nro_juntas_masculino=3, nro_juntas_femenino=2, nro_votantes=5000),
            Parroquia(codigo="002", nombre="Parroquia Norte", nro_juntas_masculino=2, nro_juntas_femenino=2, nro_votantes=4500),
            Parroquia(codigo="003", nombre="Parroquia Sur", nro_juntas_masculino=2, nro_juntas_femenino=3, nro_votantes=4000),
        ]
        db.add_all(parroquias)
        db.commit()
        print(f"✓ {len(parroquias)} parroquias creadas")
        
        # Zonas
        zonas = [
            Zona(codigo="Z001", nombre="Zona A", parroquia_id=1),
            Zona(codigo="Z002", nombre="Zona B", parroquia_id=1),
            Zona(codigo="Z003", nombre="Zona C", parroquia_id=2),
            Zona(codigo="Z004", nombre="Zona D", parroquia_id=3),
        ]
        db.add_all(zonas)
        db.commit()
        print(f"✓ {len(zonas)} zonas creadas")
        
        # Recintos
        recintos = [
            Recinto(codigo="R001", nombre="Recinto 1", zona_id=1, direccion="Calle 1 #123", nro_votantes=1000),
            Recinto(codigo="R002", nombre="Recinto 2", zona_id=1, direccion="Calle 2 #456", nro_votantes=1100),
            Recinto(codigo="R003", nombre="Recinto 3", zona_id=2, direccion="Calle 3 #789", nro_votantes=950),
            Recinto(codigo="R004", nombre="Recinto 4", zona_id=3, direccion="Calle 4 #234", nro_votantes=1050),
        ]
        db.add_all(recintos)
        db.commit()
        print(f"✓ {len(recintos)} recintos creados")
        
        # Juntas
        juntas = [
            Junta(codigo="J001", nombre="Junta 1", recinto_id=1, numero="001", tipo="m", nro_votantes=100),
            Junta(codigo="J002", nombre="Junta 2", recinto_id=1, numero="002", tipo="f", nro_votantes=110),
            Junta(codigo="J003", nombre="Junta 3", recinto_id=2, numero="001", tipo="m", nro_votantes=120),
            Junta(codigo="J004", nombre="Junta 4", recinto_id=3, numero="001", tipo="f", nro_votantes=95),
            Junta(codigo="J005", nombre="Junta 5", recinto_id=4, numero="001", tipo="m", nro_votantes=105),
        ]
        db.add_all(juntas)
        db.commit()
        print(f"✓ {len(juntas)} juntas creadas")
        
        print("\n✅ Datos de ejemplo restaurados correctamente")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error al restaurar datos: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    restore_data()
