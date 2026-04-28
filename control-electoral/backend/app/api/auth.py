from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Delegado
from app.utils.db import get_db
from jose import jwt
import bcrypt
from pydantic import BaseModel
import os

SECRET_KEY = os.getenv("SECRET_KEY", "secret-change-in-production")
ALGORITHM = "HS256"

router = APIRouter(prefix="/auth", tags=["Autenticación"])

class LoginRequest(BaseModel):
    cedula: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    rol: str

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar contraseña usando bcrypt"""
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    delegado = db.query(Delegado).filter(Delegado.cedula == data.cedula).first()
    if not delegado or not verify_password(data.password, delegado.password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    token = jwt.encode(
        {"sub": delegado.cedula, "rol": delegado.rol, "id": delegado.id},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return TokenResponse(access_token=token, rol=delegado.rol)
