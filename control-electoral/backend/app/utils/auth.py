from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from app.utils.db import get_db
from app.models import Delegado
import os

SECRET_KEY = os.getenv("SECRET_KEY", "secret-change-in-production")
ALGORITHM = "HS256"

bearer_scheme = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
) -> Delegado:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        cedula: str = payload.get("sub")
        if not cedula:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    delegado = db.query(Delegado).filter(Delegado.cedula == cedula).first()
    if not delegado:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return delegado

def require_admin(current_user: Delegado = Depends(get_current_user)) -> Delegado:
    if current_user.rol != "admin":
        raise HTTPException(status_code=403, detail="Se requiere rol de administrador")
    return current_user
