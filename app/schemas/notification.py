"""Esquemas para notificaciones."""
from datetime import datetime
from pydantic import BaseModel


class NotificationResponse(BaseModel):
    """Respuesta de notificación."""
    id: str
    tipo: str
    mensaje: str
    leida: bool
    createdAt: datetime
