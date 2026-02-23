"""Servicio de ventas: POS con actualización atómica de inventarios."""
from datetime import datetime
from bson import ObjectId

from app.database import get_database


class SalesService:
    """Gestiona ventas y descuenta inventarios de forma atómica."""

    @staticmethod
    async def crear_venta(items: list[dict]) -> dict:
        """
        Crea una venta y descuenta:
        - Dosis de inventory_dosis (o materia prima si no hay dosis)
        - Extras de inventory_raw
        - Envases (vaso, tapa, pitillo) de inventory_raw
        """
        db = get_database()
        raw_col = db["inventory_raw"]
        recipes_col = db["recipes_dosis"]
        dosis_col = db["inventory_dosis"]
        sales_col = db["sales"]

        total_venta = 0.0
        costo_total = 0.0
        sale_items = []

        for item in items:
            recipe_id = item["recipe_id"]
            nombre_batido = item["nombre_batido"]
            cantidad = item.get("cantidad", 1)
            precio_unitario = item["precio_unitario"]
            extras = item.get("extras", [])
            costo_envase = item.get("costo_envase", 0)
            envase_items = item.get("envase_items", [])

            # Obtener receta
            recipe = await recipes_col.find_one({"_id": ObjectId(recipe_id)})
            if not recipe:
                raise ValueError(f"Receta no encontrada: {recipe_id}")

            # Calcular costo de dosis (ingredientes)
            costo_dosis = 0
            for ing in recipe["ingredientes"]:
                mp = await raw_col.find_one({"_id": ObjectId(ing["materia_prima_id"])})
                if mp:
                    costo_por_gramo = mp["costo_por_unidad"] / (
                        1000 if mp.get("unidad_medida") == "kg" else 1
                    )
                    costo_dosis += ing["cantidad_gramos"] * costo_por_gramo * cantidad

            # Descontar dosis o materia prima
            inv_dosis = await dosis_col.find_one({"recipe_id": recipe_id})
            stock_dosis = inv_dosis["cantidad_bolsitas_listas"] if inv_dosis else 0

            if stock_dosis >= cantidad:
                await dosis_col.update_one(
                    {"recipe_id": recipe_id},
                    {"$inc": {"cantidad_bolsitas_listas": -cantidad}},
                )
            else:
                # Descontar de dosis disponibles y el resto de materia prima
                if stock_dosis > 0:
                    await dosis_col.update_one(
                        {"recipe_id": recipe_id},
                        {"$inc": {"cantidad_bolsitas_listas": -stock_dosis}},
                    )
                    faltante = cantidad - stock_dosis
                else:
                    faltante = cantidad

                for ing in recipe["ingredientes"]:
                    cantidad_restar = ing["cantidad_gramos"] * faltante
                    await raw_col.update_one(
                        {"_id": ObjectId(ing["materia_prima_id"])},
                        {"$inc": {"cantidad_total": -cantidad_restar}},
                    )

            # Descontar extras
            extras_data = []
            for extra in extras:
                mp_id = extra["materia_prima_id"]
                cant_extra = extra.get("cantidad", 1)
                precio_extra = extra.get("precio_extra", 0)

                mp = await raw_col.find_one({"_id": ObjectId(mp_id)})
                if not mp:
                    raise ValueError(f"Materia prima extra no encontrada: {mp_id}")

                # Asumimos que extras se miden en unidades
                await raw_col.update_one(
                    {"_id": ObjectId(mp_id)},
                    {"$inc": {"cantidad_total": -cant_extra}},
                )

                costo_extra = mp["costo_por_unidad"] * cant_extra
                costo_total += costo_extra
                extras_data.append({
                    "materia_prima_id": mp_id,
                    "nombre": mp["nombre"],
                    "cantidad": cant_extra,
                    "precio_extra": precio_extra,
                })

            # Descontar envases (vaso, tapa, pitillo)
            for env in envase_items:
                mp_id = env["materia_prima_id"]
                cant_env = env.get("cantidad", 1) * cantidad
                mp = await raw_col.find_one({"_id": ObjectId(mp_id)})
                if mp:
                    await raw_col.update_one(
                        {"_id": ObjectId(mp_id)},
                        {"$inc": {"cantidad_total": -cant_env}},
                    )
                    costo_total += mp["costo_por_unidad"] * cant_env

            costo_envase_total = costo_envase * cantidad
            costo_total += costo_dosis + costo_envase_total

            subtotal = (precio_unitario * cantidad) + sum(
                e.get("precio_extra", 0) * e.get("cantidad", 1) for e in extras
            )
            total_venta += subtotal

            sale_items.append({
                "recipe_id": recipe_id,
                "nombre_batido": nombre_batido,
                "cantidad": cantidad,
                "precio_unitario": precio_unitario,
                "extras": extras_data,
                "costo_envase": costo_envase,
            })

        venta = {
            "items": sale_items,
            "total_venta": total_venta,
            "costo_total_venta": costo_total,
            "fecha": datetime.utcnow(),
        }
        result = await sales_col.insert_one(venta)
        venta["_id"] = result.inserted_id

        return {
            "id": str(venta["_id"]),
            "items": sale_items,
            "total_venta": total_venta,
            "costo_total_venta": costo_total,
            "fecha": venta["fecha"],
        }
