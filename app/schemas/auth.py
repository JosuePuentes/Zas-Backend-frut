"""Esquemas para autenticación."""
from typing import Literal
from pydantic import BaseModel


class UbicacionSchema(BaseModel):
    lat: float = 0
    lng: float = 0
    direccion: str = ""


class RegisterRequest(BaseModel):
    """Registro de usuario (cliente). ubicacion para delivery."""
    email: str
    password: str
    nombre: str
    telefono: str = ""
    rol: str = "cliente"
    ubicacion: UbicacionSchema | None = None


class LoginRequest(BaseModel):
    """Login. tipo distingue el flujo: admin (usuario o email) vs cliente (email)."""
    email: str  # Para cliente. Para admin puede ser email o usuario
    password: str
    tipo: Literal["admin", "cliente"] = "cliente"


class TokenResponse(BaseModel):
    """Respuesta con token."""
    access_token: str
    token_type: str = "bearer"
    user: dict
