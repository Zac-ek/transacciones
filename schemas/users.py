"""
Módulo de modelos para usuarios.

Define las clases Pydantic para la validación de datos de usuarios en la API.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    """Modelo base para los usuarios."""
    id: int
    name: str
    last_name: str
    type_user: str
    user_name: str
    email: str
    password: str
    phone_number: str
    status: str
    registration_date: datetime
    update_date: datetime

class userCreate(UserBase):
    """Modelo para la creación de usuarios."""
    pass

class userUpdate(UserBase):
    """Modelo para la actualización de usuarios."""
    pass

class user(UserBase):
    """Modelo que representa un usuario con ID incluido."""

    id: int

    class Config:
        """Configuración para permitir el uso con ORM."""
        orm_mode = True

class user_login(BaseModel):
    user_name: Optional[str] = None,
    email: Optional[str] = None,
    phone_number: Optional[str] = None,
    password: str
