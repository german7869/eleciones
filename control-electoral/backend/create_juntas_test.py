#!/usr/bin/env python
"""Crear juntas de prueba"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.models.territorial import Junta, TipoJuntaEnum

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://elector:passwd@db:5432/elector_db")
engine = create_engine(DATABASE_URL)

def crear_juntas_test():
    with Session(engine) as db:
        # Obtener todos los recintos
        from app.models import Recinto
        recintos = db.query(Recinto).all()
        print(f"Found {len(recintos)} recintos")
        
        contador = 0
        for idx, recinto in enumerate(recintos[:20]):  # Crear 20 juntas
            junta = Junta(
                codigo=f"J-{recinto.codigo}-{idx+1}",
                nombre=f"Junta {idx+1} - {recinto.nombre}",
                recinto_id=recinto.id,
                numero=idx + 1,
                tipo=TipoJuntaEnum.masculino if idx % 2 == 0 else TipoJuntaEnum.femenino,
                delegado_id=None
            )
            db.add(junta)
            contador += 1
        
        db.commit()
        print(f"✅ Creadas {contador} juntas de prueba")

if __name__ == "__main__":
    crear_juntas_test()
