"""Esquemas para usuarios."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UserCreateRequest(BaseModel):
    """Crear usuario."""
    email: str
    password: str
    nombre: str
    telefono: str = ""
    rol: str = "cliente"
    permisos: list[str] = []


class UserResponse(BaseModel):
    """Respuesta de usuario."""
    id: str
    email: str
    nombre: str
    telefono: str
    rol: str
    permisos: list[str]
    createdAt: datetime
