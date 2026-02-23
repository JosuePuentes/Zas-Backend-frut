"""Modelo de notificación."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class NotificationBase(BaseModel):
    """Base de notificación."""
    tipo: str
    mensaje: str


class NotificationCreate(NotificationBase):
    """Crear notificación."""
    pass


class NotificationResponse(NotificationBase):
    """Respuesta de notificación."""
    id: str
    leida: bool = False
    createdAt: datetime
