from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.utils.db import get_db
from app.utils.auth import require_admin
from app.models import Parroquia, Zona, Recinto, Junta
from app.models.territorial import TipoJuntaEnum
from app.models.delegado import Delegado
import pandas as pd
import io

router = APIRouter(prefix="/import", tags=["Importación CSV"])


def _read_csv(file: UploadFile) -> pd.DataFrame:
    try:
        content = file.file.read()
        return pd.read_csv(io.BytesIO(content))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al leer CSV: {str(e)}")


def _check_cols(df: pd.DataFrame, required: list[str]):
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise HTTPException(status_code=422, detail=f"Columnas faltantes en CSV: {', '.join(missing)}")


@router.post("/parroquias")
def import_parroquias(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db), 
    current_user: Delegado = Depends(require_admin)
):
    """Importar parroquias desde CSV - continúa aunque haya errores en algunas filas"""
    if not file.filename or not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="El archivo debe ser CSV")
    
    df = _read_csv(file)
    _check_cols(df, ["codigo", "nombre"])
    insertados, actualizados, errores = 0, 0, []
    
    for i, row in df.iterrows():
        fila_num = i + 2
        codigo = str(row.get("codigo", "")).strip()
        nombre = str(row.get("nombre", "")).strip()
        
        try:
            if not codigo:
                errores.append({"fila": fila_num, "codigo": "vacío", "nombre": nombre, "error": "Código vacío"})
                continue
            if not nombre:
                errores.append({"fila": fila_num, "codigo": codigo, "nombre": "vacío", "error": "Nombre vacío"})
                continue
            
            existing = db.query(Parroquia).filter(Parroquia.codigo == codigo).first()
            if existing:
                existing.nombre = nombre
                existing.nro_juntas_masculino = int(row.get("nro_juntas_masculino", 0) or 0)
                existing.nro_juntas_femenino = int(row.get("nro_juntas_femenino", 0) or 0)
                existing.nro_votantes = int(row.get("nro_votantes", 0) or 0)
                actualizados += 1
            else:
                db.add(Parroquia(
                    codigo=codigo,
                    nombre=nombre,
                    nro_juntas_masculino=int(row.get("nro_juntas_masculino", 0) or 0),
                    nro_juntas_femenino=int(row.get("nro_juntas_femenino", 0) or 0),
                    nro_votantes=int(row.get("nro_votantes", 0) or 0),
                ))
                insertados += 1
            db.commit()
        except Exception as e:
            db.rollback()
            errores.append({"fila": fila_num, "codigo": codigo, "nombre": nombre, "error": str(e)})
    
    return {"insertados": insertados, "actualizados": actualizados, "errores": errores, "total_procesadas": len(df), "exitosas": insertados + actualizados}


@router.post("/zonas")
def import_zonas(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db), 
    current_user: Delegado = Depends(require_admin)
):
    """Importar zonas desde CSV - continúa aunque haya errores en algunas filas"""
    if not file.filename or not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="El archivo debe ser CSV")
    
    df = _read_csv(file)
    _check_cols(df, ["codigo", "nombre", "parroquia_codigo"])
    insertados, actualizados, errores = 0, 0, []
    
    for i, row in df.iterrows():
        fila_num = i + 2
        codigo = str(row.get("codigo", "")).strip()
        nombre = str(row.get("nombre", "")).strip()
        parroquia_codigo = str(row.get("parroquia_codigo", "")).strip()
        
        try:
            if not codigo:
                errores.append({"fila": fila_num, "codigo": "vacío", "nombre": nombre, "parroquia_codigo": parroquia_codigo, "error": "Código vacío"})
                continue
            if not nombre:
                errores.append({"fila": fila_num, "codigo": codigo, "nombre": "vacío", "parroquia_codigo": parroquia_codigo, "error": "Nombre vacío"})
                continue
            if not parroquia_codigo:
                errores.append({"fila": fila_num, "codigo": codigo, "nombre": nombre, "parroquia_codigo": "vacío", "error": "Parroquia código vacío"})
                continue
            
            parroquia = db.query(Parroquia).filter(Parroquia.codigo == parroquia_codigo).first()
            if not parroquia:
                errores.append({"fila": fila_num, "codigo": codigo, "nombre": nombre, "parroquia_codigo": parroquia_codigo, "error": f"Parroquia '{parroquia_codigo}' no existe"})
                continue
            
            existing = db.query(Zona).filter(Zona.codigo == codigo).first()
            if existing:
                existing.nombre = nombre
                existing.parroquia_id = parroquia.id
                actualizados += 1
            else:
                db.add(Zona(codigo=codigo, nombre=nombre, parroquia_id=parroquia.id))
                insertados += 1
            db.commit()
        except Exception as e:
            db.rollback()
            errores.append({"fila": fila_num, "codigo": codigo, "nombre": nombre, "parroquia_codigo": parroquia_codigo, "error": str(e)})
    
    return {"insertados": insertados, "actualizados": actualizados, "errores": errores, "total_procesadas": len(df), "exitosas": insertados + actualizados}


@router.post("/recintos")
def import_recintos(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db), 
    current_user: Delegado = Depends(require_admin)
):
    """Importar recintos desde CSV - continúa aunque haya errores en algunas filas"""
    if not file.filename or not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="El archivo debe ser CSV")
    
    df = _read_csv(file)
    _check_cols(df, ["codigo", "nombre", "zona_codigo"])
    insertados, actualizados, errores = 0, 0, []
    
    for i, row in df.iterrows():
        fila_num = i + 2
        codigo = str(row.get("codigo", "")).strip()
        nombre = str(row.get("nombre", "")).strip()
        zona_codigo = str(row.get("zona_codigo", "")).strip()
        
        try:
            if not codigo:
                errores.append({"fila": fila_num, "codigo": "vacío", "nombre": nombre, "zona_codigo": zona_codigo, "error": "Código vacío"})
                continue
            if not nombre:
                errores.append({"fila": fila_num, "codigo": codigo, "nombre": "vacío", "zona_codigo": zona_codigo, "error": "Nombre vacío"})
                continue
            if not zona_codigo:
                errores.append({"fila": fila_num, "codigo": codigo, "nombre": nombre, "zona_codigo": "vacío", "error": "Zona código vacío"})
                continue
            
            zona = db.query(Zona).filter(Zona.codigo == zona_codigo).first()
            if not zona:
                errores.append({"fila": fila_num, "codigo": codigo, "nombre": nombre, "zona_codigo": zona_codigo, "error": f"Zona '{zona_codigo}' no existe"})
                continue
            
            existing = db.query(Recinto).filter(Recinto.codigo == codigo).first()
            if existing:
                existing.nombre = nombre
                existing.zona_id = zona.id
                existing.direccion = str(row.get("direccion", "") or "")
                existing.nro_votantes = int(row.get("nro_votantes", 0) or 0)
                actualizados += 1
            else:
                db.add(Recinto(
                    codigo=codigo,
                    nombre=nombre,
                    zona_id=zona.id,
                    direccion=str(row.get("direccion", "") or ""),
                    nro_votantes=int(row.get("nro_votantes", 0) or 0),
                ))
                insertados += 1
            db.commit()
        except Exception as e:
            db.rollback()
            errores.append({"fila": fila_num, "codigo": codigo, "nombre": nombre, "zona_codigo": zona_codigo, "error": str(e)})
    
    return {"insertados": insertados, "actualizados": actualizados, "errores": errores, "total_procesadas": len(df), "exitosas": insertados + actualizados}


@router.post("/juntas")
def import_juntas(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db), 
    current_user: Delegado = Depends(require_admin)
):
    """Importar juntas desde CSV
    Columnas requeridas: codigo, nombre, nro_votantes, tipo, recinto_codigo, numero
    Tipo: 'm'/'M' para masculino, 'f'/'F' para femenino
    
    Retorna:
    - insertados: cantidad de nuevas juntas agregadas
    - actualizados: cantidad de juntas actualizadas
    - errores: lista detallada de filas con error (fila, codigo, nombre, recinto_codigo, error)
    """
    if not file.filename or not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="El archivo debe ser CSV")
    
    df = _read_csv(file)
    _check_cols(df, ["codigo", "nombre", "nro_votantes", "tipo", "recinto_codigo", "numero"])
    insertados, actualizados, errores = 0, 0, []
    
    for i, row in df.iterrows():
        fila_num = i + 2
        codigo = str(row.get("codigo", "")).strip()
        nombre = str(row.get("nombre", "")).strip()
        recinto_codigo = str(row.get("recinto_codigo", "")).strip()
        
        try:
            # Validar que valores requeridos no estén vacíos
            if not codigo:
                errores.append({
                    "fila": fila_num,
                    "codigo": codigo or "vacío",
                    "nombre": nombre,
                    "recinto_codigo": recinto_codigo,
                    "error": "Código vacío o faltante"
                })
                continue
            if not nombre:
                errores.append({
                    "fila": fila_num,
                    "codigo": codigo,
                    "nombre": nombre or "vacío",
                    "recinto_codigo": recinto_codigo,
                    "error": "Nombre vacío o faltante"
                })
                continue
            if not recinto_codigo:
                errores.append({
                    "fila": fila_num,
                    "codigo": codigo,
                    "nombre": nombre,
                    "recinto_codigo": recinto_codigo or "vacío",
                    "error": "Recinto código vacío o faltante"
                })
                continue
            
            # Validar que el recinto exista
            recinto = db.query(Recinto).filter(Recinto.codigo == recinto_codigo).first()
            if not recinto:
                errores.append({
                    "fila": fila_num,
                    "codigo": codigo,
                    "nombre": nombre,
                    "recinto_codigo": recinto_codigo,
                    "error": f"Recinto '{recinto_codigo}' no existe en el sistema"
                })
                continue
            
            # Validar y convertir tipo a enum
            tipo_valor = str(row.get("tipo", "")).lower().strip()
            if not tipo_valor:
                errores.append({
                    "fila": fila_num,
                    "codigo": codigo,
                    "nombre": nombre,
                    "recinto_codigo": recinto_codigo,
                    "error": "Tipo vacío (debe ser 'M' para masculino o 'F' para femenino)"
                })
                continue
            if tipo_valor not in ["m", "f"]:
                errores.append({
                    "fila": fila_num,
                    "codigo": codigo,
                    "nombre": nombre,
                    "recinto_codigo": recinto_codigo,
                    "error": f"Tipo inválido: '{row['tipo']}' (debe ser 'M' para masculino o 'F' para femenino)"
                })
                continue
            tipo_enum = TipoJuntaEnum.masculino if tipo_valor == "m" else TipoJuntaEnum.femenino
            
            # Validar y convertir numero a INTEGER (pandas lee como float: 1.0, 2.0)
            try:
                numero_val = row.get("numero", "")
                if str(numero_val).strip() == "" or str(numero_val) == "nan":
                    errores.append({
                        "fila": fila_num,
                        "codigo": codigo,
                        "nombre": nombre,
                        "recinto_codigo": recinto_codigo,
                        "error": "Número de junta vacío o faltante"
                    })
                    continue
                numero = int(float(numero_val))  # Convierte 1.0 -> 1
            except (ValueError, TypeError):
                errores.append({
                    "fila": fila_num,
                    "codigo": codigo,
                    "nombre": nombre,
                    "recinto_codigo": recinto_codigo,
                    "error": f"Número de junta inválido: '{numero_val}' (debe ser un número entero)"
                })
                continue
            
            # Validar nro_votantes
            try:
                nro_votantes = int(float(row.get("nro_votantes", 0) or 0))
            except ValueError:
                errores.append({
                    "fila": fila_num,
                    "codigo": codigo,
                    "nombre": nombre,
                    "recinto_codigo": recinto_codigo,
                    "error": f"Número de votantes inválido: '{row.get('nro_votantes')}' (debe ser un número)"
                })
                continue
            
            # Insertar o actualizar (delegado_id se deja NULL en importación)
            existing = db.query(Junta).filter(Junta.codigo == codigo).first()
            if existing:
                existing.nombre = nombre
                existing.recinto_id = recinto.id
                existing.numero = numero
                existing.tipo = tipo_enum
                existing.nro_votantes = nro_votantes
                actualizados += 1
            else:
                db.add(Junta(
                    codigo=codigo,
                    nombre=nombre,
                    recinto_id=recinto.id,
                    numero=numero,
                    tipo=tipo_enum,
                    nro_votantes=nro_votantes,
                    # delegado_id se deja NULL (asignado luego por otros sistemas)
                ))
                insertados += 1
            
            # Commit cada fila exitosa para que se guarde aunque fallen otras
            db.commit()
            
        except Exception as e:
            # Rollback en caso de error de base de datos
            db.rollback()
            errores.append({
                "fila": fila_num,
                "codigo": codigo,
                "nombre": nombre,
                "recinto_codigo": recinto_codigo,
                "error": f"Error en base de datos: {str(e)}"
            })
    
    return {
        "insertados": insertados,
        "actualizados": actualizados,
        "errores": errores,
        "total_procesadas": len(df),
        "exitosas": insertados + actualizados
    }
