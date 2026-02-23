"""Esquemas para autenticación."""
from pydantic import BaseModel


class RegisterRequest(BaseModel):
    """Registro de usuario (cliente)."""
    email: str
    password: str
    nombre: str
    telefono: str = ""
    rol: str = "cliente"


class LoginRequest(BaseModel):
    """Login."""
    email: str
    password: str


class TokenResponse(BaseModel):
    """Respuesta con token."""
    access_token: str
    token_type: str = "bearer"
    user: dict
