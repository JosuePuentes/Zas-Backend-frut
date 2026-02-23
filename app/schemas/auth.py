"""Esquemas para autenticación."""
from typing import Literal
from pydantic import BaseModel


class UbicacionSchema(BaseModel):
    lat: float = 0
    lng: float = 0
    direccion: str = ""


class RegisterRequest(BaseModel):
    """Registro público solo para clientes. No aceptar rol ni usuario. ubicacion obligatorio."""
    email: str
    password: str
    nombre: str
    telefono: str = ""
    ubicacion: UbicacionSchema


class RegisterResponse(BaseModel):
    """Respuesta de registro: user y token."""
    user: dict
    token: str


class LoginRequest(BaseModel):
    """Login. identificador: email (cliente) o usuario/email (admin). Detección por @."""
    identificador: str
    password: str


class LoginResponse(BaseModel):
    """Respuesta login: user y token."""
    user: dict
    token: str
