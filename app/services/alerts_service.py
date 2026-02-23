"""Servicio de alertas: caducidad de materia prima."""
from datetime import datetime, timedelta
from app.database import get_database


class AlertsService:
    """Alertas de caducidad para frutas y materia prima."""

    @staticmethod
    async def get_alertas_caducidad(dias_antiguedad: int = 3) -> list[dict]:
        """
        Retorna materia prima ordenada por fecha_ingreso (más antigua primero).
        Las que tienen fecha_ingreso más antigua deberían usarse primero.
        """
        db = get_database()
        raw_col = db["inventory_raw"]

        cursor = raw_col.find({"fecha_ingreso": {"$exists": True, "$ne": None}})
        items = []

        async for doc in cursor:
            fecha = doc.get("fecha_ingreso")
            if fecha:
                dias_transcurridos = (datetime.utcnow() - fecha).days
                items.append({
                    "materia_prima_id": str(doc["_id"]),
                    "nombre": doc["nombre"],
                    "cantidad_total": doc.get("cantidad_total", 0),
                    "fecha_ingreso": fecha,
                    "dias_desde_ingreso": dias_transcurridos,
                    "prioridad": "alta" if dias_transcurridos >= dias_antiguedad else "normal",
                })

        # Ordenar por más antigua primero (usar primero)
        items.sort(key=lambda x: x["fecha_ingreso"])
        return items
