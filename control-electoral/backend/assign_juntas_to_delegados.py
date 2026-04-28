#!/usr/bin/env python
"""Script para asignar juntas a delegados de prueba"""
from sqlalchemy import text
from app.models.delegado import Delegado
from app.models.territorial import Junta
from app.utils.db import SessionLocal

db = SessionLocal()

try:
    print("\nAsignando juntas a delegados...\n")
    
    # Obtener delegados
    delegados = db.query(Delegado).filter(Delegado.rol == "delegado").order_by(Delegado.id).all()
    print(f"Delegados encontrados: {len(delegados)}")
    
    # Obtener juntas sin asignar
    juntas_sin_asignar = db.query(Junta).filter(Junta.delegado_id == None).all()
    print(f"Juntas sin asignar: {len(juntas_sin_asignar)}\n")
    
    if not delegados or not juntas_sin_asignar:
        print("✗ No hay delegados o juntas disponibles")
        exit(1)
    
    # Distribuir juntas entre delegados
    juntas_por_delegado = len(juntas_sin_asignar) // len(delegados)
    juntas_restantes = len(juntas_sin_asignar) % len(delegados)
    
    print(f"Juntas por delegado: {juntas_por_delegado}")
    print(f"Juntas restantes para distribuir: {juntas_restantes}\n")
    
    idx = 0
    for i, delegado in enumerate(delegados):
        # Calcular cuántas juntas asignar a este delegado
        cantidad = juntas_por_delegado + (1 if i < juntas_restantes else 0)
        
        # Asignar juntas
        for j in range(cantidad):
            if idx < len(juntas_sin_asignar):
                junta = juntas_sin_asignar[idx]
                junta.delegado_id = delegado.id
                db.add(junta)
                idx += 1
        
        db.commit()
        print(f"✓ {delegado.nombre}: {cantidad} juntas asignadas")
    
    print(f"\n✅ Total de juntas asignadas: {idx}")
    
finally:
    db.close()
