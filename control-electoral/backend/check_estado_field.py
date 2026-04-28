#!/usr/bin/env python
"""Verificar si el campo estado existe en juntas"""
from app.utils.db import SessionLocal
from sqlalchemy import text, inspect

db = SessionLocal()
try:
    # Ver estructura tabla juntas
    inspector = inspect(db.get_bind())
    columns = inspector.get_columns('juntas')
    print('Columnas en tabla juntas:')
    for col in columns:
        print(f'  {col["name"]}: {col["type"]}')
    
    # Ver valores estado
    print('\nValores de estado en juntas:')
    result = db.execute(text('SELECT DISTINCT estado FROM juntas')).fetchall()
    for row in result:
        print(f'  estado: {row[0]}')
    
    # Contar por estado
    print('\nConteo por estado:')
    result = db.execute(text('SELECT estado, COUNT(*) FROM juntas GROUP BY estado')).fetchall()
    for row in result:
        print(f'  {row[0]}: {row[1]}')
        
finally:
    db.close()
