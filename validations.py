from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jwt_config import valida_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
    
def get_current_user(token: str = Security(oauth2_scheme)):
    """"Función que valida el token"""
    try:
        user_data = valida_token(token)
        if not user_data:
            raise HTTPException(status_code=403, detail="Invalid credentials")
        return user_data
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
