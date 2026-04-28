#!/usr/bin/env python
"""Script para probar la importación de juntas"""
import sys
sys.path.insert(0, '/app')

from app.utils.db import SessionLocal
from app.api.import_csv import _read_csv
from app.models.territorial import Junta, TipoJuntaEnum, Recinto

db = SessionLocal()

# Simular la lectura del CSV
with open('/app/juntas_prueba.csv', 'rb') as f:
    import io
    df = _read_csv(type('obj', (object,), {'file': io.BytesIO(f.read()), 'filename': 'juntas_prueba.csv'})())

print("Columnas del CSV:", df.columns.tolist())
print("\nContenido:")
print(df.to_string())

insertados = 0
errores = []

for i, row in df.iterrows():
    try:
        print(f"\nProcesando fila {i+2}: {row['codigo']}")
        
        # Buscar recinto
        recinto = db.query(Recinto).filter(Recinto.codigo == str(row["recinto_codigo"])).first()
        if not recinto:
            print(f"  ✗ Recinto '{row['recinto_codigo']}' no existe")
            errores.append({"fila": i + 2, "error": f"Recinto '{row['recinto_codigo']}' no existe"})
            continue
        
        print(f"  ✓ Recinto encontrado: {recinto.nombre} (ID: {recinto.id})")
        
        # Convertir tipo a enum
        tipo_valor = str(row["tipo"]).lower().strip()
        if tipo_valor not in ["m", "f"]:
            print(f"  ✗ Tipo inválido: '{tipo_valor}'")
            errores.append({"fila": i + 2, "error": f"Tipo inválido: '{tipo_valor}'"})
            continue
        
        tipo_enum = TipoJuntaEnum.masculino if tipo_valor == "m" else TipoJuntaEnum.femenino
        print(f"  ✓ Tipo convertido: {tipo_valor} → {tipo_enum}")
        
        # Crear junta
        nueva_junta = Junta(
            codigo=str(row["codigo"]),
            nombre=str(row["nombre"]),
            recinto_id=recinto.id,
            numero=str(row["numero"]),
            tipo=tipo_enum,
            nro_votantes=int(row.get("nro_votantes", 0) or 0),
        )
        
        db.add(nueva_junta)
        print(f"  ✓ Junta agregada: {row['codigo']} - {row['nombre']}")
        insertados += 1
        
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        errores.append({"fila": i + 2, "error": str(e)})

db.commit()
print(f"\n\n✅ Resultado:")
print(f"  Insertados: {insertados}")
print(f"  Errores: {len(errores)}")
if errores:
    print(f"  Detalles: {errores}")

db.close()
