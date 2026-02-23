"""Servicio de planificación: lista de compras."""
from app.database import get_database


class PlanningService:
    """Genera lista de compras según stock mínimo."""

    @staticmethod
    async def get_lista_compras() -> list[dict]:
        """
        Compara stock actual vs stock mínimo.
        Retorna items que necesitan reabastecimiento.
        """
        db = get_database()
        raw_col = db["inventory_raw"]

        cursor = raw_col.find({})
        items = []

        async for doc in cursor:
            stock_actual = doc.get("cantidad_total", 0)
            stock_minimo = doc.get("stock_minimo", 0)

            if stock_actual < stock_minimo:
                cantidad_comprar = stock_minimo - stock_actual
                items.append({
                    "materia_prima_id": str(doc["_id"]),
                    "nombre": doc["nombre"],
                    "stock_actual": stock_actual,
                    "stock_minimo": stock_minimo,
                    "cantidad_a_comprar": cantidad_comprar,
                    "unidad_medida": doc.get("unidad_medida", "g"),
                })

        return items
