#!/usr/bin/env python
"""
Script para limpiar todos los delegados y sus asignaciones de juntas.
Mantiene los datos territoriales (parroquias, zonas, recintos, juntas).
"""

import sys
from sqlalchemy import text
from app.utils.db import get_db

def clean_delegados_and_assignments():
    """Elimina todos los delegados y libera las juntas (delegado_id = NULL)"""
    
    db = next(get_db())
    
    try:
        # 1. Poner delegado_id = NULL en todas las juntas
        print("\n1. Liberando todas las juntas (delegado_id = NULL)...")
        result = db.execute(text("UPDATE juntas SET delegado_id = NULL"))
        db.commit()
        print(f"   ✓ {result.rowcount} juntas liberadas")
        
        # 2. Eliminar todos los delegados
        print("\n2. Eliminando todos los delegados...")
        result = db.execute(text("DELETE FROM delegados"))
        db.commit()
        print(f"   ✓ {result.rowcount} delegados eliminados")
        
        # 3. Verificar datos territoriales
        print("\n3. Verificando datos territoriales...")
        parroquias = db.execute(text("SELECT COUNT(*) FROM parroquias")).scalar()
        zonas = db.execute(text("SELECT COUNT(*) FROM zonas")).scalar()
        recintos = db.execute(text("SELECT COUNT(*) FROM recintos")).scalar()
        juntas = db.execute(text("SELECT COUNT(*) FROM juntas")).scalar()
        delegados = db.execute(text("SELECT COUNT(*) FROM delegados")).scalar()
        
        print(f"   ✓ Parroquias: {parroquias}")
        print(f"   ✓ Zonas: {zonas}")
        print(f"   ✓ Recintos: {recintos}")
        print(f"   ✓ Juntas: {juntas}")
        print(f"   ✓ Delegados: {delegados}")
        
        print("\n✅ Limpieza completada exitosamente")
        print("   → Todos los delegados eliminados")
        print("   → Todas las juntas han sido liberadas")
        print("   → Datos territoriales se mantienen intactos")
        
        return True
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error durante la limpieza: {str(e)}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    clean_delegados_and_assignments()
