#!/usr/bin/env python
"""Asignar juntas a delegados de prueba"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.models.territorial import Junta
from app.models.delegado import Delegado

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://elector:passwd@db:5432/elector_db")
engine = create_engine(DATABASE_URL)

def asignar_juntas():
    with Session(engine) as db:
        # Obtener delegados (excluir admin)
        delegados = db.query(Delegado).filter(Delegado.rol == "delegado").all()
        
        if not delegados:
            print("❌ No hay delegados disponibles")
            return
        
        juntas = db.query(Junta).all()
        total = len(juntas)
        
        print(f"Delegados encontrados: {len(delegados)}")
        for d in delegados:
            print(f"  - ID: {d.id}, Nombre: {d.nombre}")
        
        # Asignar de forma distribuida
        for idx, junta in enumerate(juntas):
            delegado_idx = idx % len(delegados)
            delegado = delegados[delegado_idx]
            junta.delegado_id = delegado.id
        
        db.commit()
        print(f"✅ Asignadas {total} juntas a {len(delegados)} delegados")

if __name__ == "__main__":
    asignar_juntas()
