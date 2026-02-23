"""Servicio de reportes: utilidad y más vendido."""
from datetime import datetime, timedelta
from app.database import get_database


class ReportsService:
    """Reportes de negocio."""

    @staticmethod
    async def get_reporte_utilidad(
        fecha_inicio: datetime | None = None,
        fecha_fin: datetime | None = None,
    ) -> dict:
        """
        Calcula: Precio de Venta - (Costo Dosis + Costo Extras + Costo Envase)
        """
        db = get_database()
        sales_col = db["sales"]

        if not fecha_inicio:
            fecha_inicio = datetime.utcnow() - timedelta(days=30)
        if not fecha_fin:
            fecha_fin = datetime.utcnow()

        query = {"fecha": {"$gte": fecha_inicio, "$lte": fecha_fin}}
        cursor = sales_col.find(query)
        ventas = []
        total_ventas = 0.0
        total_costos = 0.0

        async for doc in cursor:
            total_venta = doc.get("total_venta", 0)
            costo_total = doc.get("costo_total_venta", 0)
            ganancia = total_venta - costo_total

            ventas.append({
                "venta_id": str(doc["_id"]),
                "fecha": doc["fecha"],
                "total_venta": total_venta,
                "costo_total": costo_total,
                "ganancia_neta": ganancia,
            })
            total_ventas += total_venta
            total_costos += costo_total

        return {
            "periodo_inicio": fecha_inicio,
            "periodo_fin": fecha_fin,
            "ventas": ventas,
            "total_ventas": total_ventas,
            "total_costos": total_costos,
            "ganancia_neta_total": total_ventas - total_costos,
        }

    @staticmethod
    async def get_mas_vendidos(limite: int = 10) -> list[dict]:
        """Batidos más vendidos por cantidad."""
        db = get_database()
        sales_col = db["sales"]

        pipeline = [
            {"$unwind": "$items"},
            {"$group": {
                "_id": "$items.recipe_id",
                "nombre_batido": {"$first": "$items.nombre_batido"},
                "cantidad_vendida": {"$sum": "$items.cantidad"},
                "total_ventas": {"$sum": {"$multiply": ["$items.precio_unitario", "$items.cantidad"]}},
            }},
            {"$sort": {"cantidad_vendida": -1}},
            {"$limit": limite},
        ]
        cursor = sales_col.aggregate(pipeline)
        return [doc async for doc in cursor]

    @staticmethod
    async def get_mayor_margen(limite: int = 10) -> list[dict]:
        """Batidos con mayor margen de ganancia (requiere costo en items)."""
        db = get_database()
        sales_col = db["sales"]

        pipeline = [
            {"$unwind": "$items"},
            {"$group": {
                "_id": "$items.recipe_id",
                "nombre_batido": {"$first": "$items.nombre_batido"},
                "total_ventas": {"$sum": {"$multiply": ["$items.precio_unitario", "$items.cantidad"]}},
                "total_costos": {"$sum": "$costo_total_venta"},  # Aproximado por venta
            }},
            {"$sort": {"total_ventas": -1}},
            {"$limit": limite},
        ]
        cursor = sales_col.aggregate(pipeline)
        return [doc async for doc in cursor]
