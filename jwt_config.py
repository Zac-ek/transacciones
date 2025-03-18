from jwt import encode, decode
import jwt
import os
from datetime import datetime, timedelta
from fastapi import HTTPException

SECRET_KEY = os.getenv("SECRET_KEY", "clavesita")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def solicita_token(dato: dict) -> str:
    """
    Genera un token JWT con expiración.
    """
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dato["exp"] = expire  # Agregar tiempo de expiración al payload
    token = jwt.encode(payload=dato, key=SECRET_KEY, algorithm=ALGORITHM)
    return token

def valida_token(token: str) -> dict:
    """
    Valida y decodifica el token JWT. Si el token es inválido o expiró, lanza una excepción.
    """
    try:
        dato = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        return dato
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")