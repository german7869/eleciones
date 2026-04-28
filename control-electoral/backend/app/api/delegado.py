from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import DelegadoCreate, DelegadoRead
from app.schemas.delegado import CambiarClaveRequest
from app.models import Delegado, Junta
from app.utils.db import get_db
from app.utils.auth import get_current_user, require_admin
import bcrypt

def hash_password(password: str) -> str:
    """Hash una contraseña usando bcrypt"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12)).decode()

router = APIRouter(prefix="/delegados", tags=["Delegados"])


@router.post("/setup-admin", response_model=DelegadoRead, tags=["Setup"])
def create_first_admin(delegado: DelegadoCreate, db: Session = Depends(get_db)):
    """Crea el primer admin. Solo funciona si no existe ningún admin aún."""
    if db.query(Delegado).filter(Delegado.rol == "admin").first():
        raise HTTPException(status_code=403, detail="Ya existe un administrador. Use el endpoint protegido.")
    if db.query(Delegado).filter(Delegado.cedula == delegado.cedula).first():
        raise HTTPException(status_code=422, detail="Cédula ya registrada")
    data = delegado.dict()
    data["password"] = hash_password(data["password"])
    data["rol"] = "admin"
    db_d = Delegado(**data)
    db.add(db_d)
    db.commit()
    db.refresh(db_d)
    return db_d


@router.post("/", response_model=DelegadoRead)
def create_delegado(delegado: DelegadoCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    if db.query(Delegado).filter(Delegado.cedula == delegado.cedula).first():
        raise HTTPException(status_code=422, detail="Cédula ya registrada")
    data = delegado.dict()
    data["password"] = hash_password(data["password"])
    db_d = Delegado(**data)
    db.add(db_d)
    db.commit()
    db.refresh(db_d)
    return db_d


@router.get("/", response_model=list[DelegadoRead])
def list_delegados(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(Delegado).all()


@router.get("/{delegado_id}", response_model=DelegadoRead)
def get_delegado(delegado_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    d = db.query(Delegado).filter(Delegado.id == delegado_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Delegado no encontrado")
    return d


@router.put("/{delegado_id}", response_model=DelegadoRead)
def update_delegado(delegado_id: int, data: DelegadoCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    d = db.query(Delegado).filter(Delegado.id == delegado_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Delegado no encontrado")
    update = data.dict()
    update["password"] = hash_password(update["password"])
    for k, v in update.items():
        setattr(d, k, v)
    db.commit()
    db.refresh(d)
    return d


@router.delete("/{delegado_id}")
def delete_delegado(delegado_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    d = db.query(Delegado).filter(Delegado.id == delegado_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Delegado no encontrado")
    if db.query(Junta).filter(Junta.delegado_id == delegado_id).first():
        raise HTTPException(status_code=409, detail="No se puede eliminar: tiene juntas asignadas")
    db.delete(d)
    db.commit()
    return {"ok": True}


@router.post("/{delegado_id}/cambiar-clave", response_model=DelegadoRead)
def cambiar_clave_delegado(delegado_id: int, request: CambiarClaveRequest, db: Session = Depends(get_db), _=Depends(require_admin)):
    """Endpoint para que el admin cambie la contraseña de un delegado"""
    d = db.query(Delegado).filter(Delegado.id == delegado_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Delegado no encontrado")
    
    if not request.nueva_clave or len(request.nueva_clave.strip()) == 0:
        raise HTTPException(status_code=422, detail="La contraseña no puede estar vacía")
    
    # Hash la nueva contraseña
    d.password = hash_password(request.nueva_clave)
    db.commit()
    db.refresh(d)
    
    return d
