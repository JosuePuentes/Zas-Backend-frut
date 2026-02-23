"""Esquemas para autenticación."""
from typing import Literal
from pydantic import BaseModel


class RegisterRequest(BaseModel):
    """Registro de usuario (cliente)."""
    email: str
    password: str
    nombre: str
    telefono: str = ""
    rol: str = "cliente"


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
