"""Esquemas para usuarios."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UbicacionSchema(BaseModel):
    lat: float = 0
    lng: float = 0
    direccion: str = ""


class UserCreateRequest(BaseModel):
    """Crear usuario. Admins requieren campo usuario."""
    email: str
    password: str
    nombre: str
    telefono: str = ""
    usuario: str = ""  # Para admins: nombre de usuario para login
    rol: str = "cliente"
    permisos: list[str] = []
    sucursalId: str = ""  # Para admins no master
    ubicacion: UbicacionSchema | None = None


class UserResponse(BaseModel):
    """Respuesta de usuario."""
    id: str
    email: str
    nombre: str
    telefono: str
    usuario: str
    rol: str
    permisos: list[str]
    sucursalId: str
    ubicacion: dict
    createdAt: datetime
