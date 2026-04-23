from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Delegado
from app.utils.db import get_db
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import os

SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/auth", tags=["Autenticación"])

class LoginRequest(BaseModel):
    cedula: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    delegado = db.query(Delegado).filter(Delegado.cedula == data.cedula).first()
    if not delegado or not pwd_context.verify(data.password, getattr(delegado, "password", "")):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    token = jwt.encode({"sub": delegado.cedula}, SECRET_KEY, algorithm=ALGORITHM)
    return TokenResponse(access_token=token)
