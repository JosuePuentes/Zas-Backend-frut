"""Esquemas para usuarios."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UserCreateRequest(BaseModel):
    """Crear usuario. Admins requieren campo usuario."""
    email: str
    password: str
    nombre: str
    telefono: str = ""
    usuario: str = ""  # Para admins: nombre de usuario para login
    rol: str = "cliente"
    permisos: list[str] = []


class UserResponse(BaseModel):
    """Respuesta de usuario."""
    id: str
    email: str
    nombre: str
    telefono: str
    usuario: str  # Para admins
    rol: str
    permisos: list[str]
    createdAt: datetime
