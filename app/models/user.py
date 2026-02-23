"""Modelo de usuario."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    """Base de usuario."""
    email: str
    nombre: str
    telefono: str = ""
    rol: str = "cliente"  # cliente, admin, etc.
    permisos: list[str] = []


class UserCreate(UserBase):
    """Crear usuario."""
    password: str


class UserResponse(UserBase):
    """Respuesta de usuario (sin password)."""
    id: str
    createdAt: datetime


class UserInDB(UserBase):
    """Usuario en BD (con password hasheado)."""
    id: Optional[str] = None
    password_hash: str
    createdAt: datetime
