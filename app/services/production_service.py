"""Servicio de producción: procesar materia prima en dosis."""
from bson import ObjectId

from app.database import get_database


class ProductionService:
    """Procesa materia prima en dosis (bolsitas)."""

    @staticmethod
    async def procesar_dosis(recipe_id: str, cantidad_dosis: int) -> dict:
        """
        Procesar N dosis de un batido:
        - Resta materia prima de inventory_raw
        - Suma dosis a inventory_dosis
        """
        db = get_database()
        recipes_col = db["recipes_dosis"]
        raw_col = db["inventory_raw"]
        dosis_col = db["inventory_dosis"]

        recipe = await recipes_col.find_one({"_id": ObjectId(recipe_id)})
        if not recipe:
            raise ValueError(f"Receta no encontrada: {recipe_id}")

        # Verificar que hay suficiente materia prima
        for ing in recipe["ingredientes"]:
            mp_id = ing["materia_prima_id"]
            cantidad_necesaria = ing["cantidad_gramos"] * cantidad_dosis

            raw = await raw_col.find_one({"_id": ObjectId(mp_id)})
            if not raw:
                raise ValueError(f"Materia prima no encontrada: {mp_id}")
            if raw["cantidad_total"] < cantidad_necesaria:
                raise ValueError(
                    f"Stock insuficiente de {raw['nombre']}: "
                    f"necesitas {cantidad_necesaria}g, tienes {raw['cantidad_total']}g"
                )

        # Transacción: restar materia prima y sumar dosis
        for ing in recipe["ingredientes"]:
            mp_id = ing["materia_prima_id"]
            cantidad_necesaria = ing["cantidad_gramos"] * cantidad_dosis
            await raw_col.update_one(
                {"_id": ObjectId(mp_id)},
                {"$inc": {"cantidad_total": -cantidad_necesaria}},
            )

        # Sumar dosis al inventario
        result = await dosis_col.find_one_and_update(
            {"recipe_id": recipe_id},
            {"$inc": {"cantidad_bolsitas_listas": cantidad_dosis}},
            return_document=True,
        )

        if not result:
            # Crear registro si no existe
            await dosis_col.insert_one({
                "recipe_id": recipe_id,
                "cantidad_bolsitas_listas": cantidad_dosis,
            })
            result = await dosis_col.find_one({"recipe_id": recipe_id})

        return {
            "recipe_id": recipe_id,
            "nombre_batido": recipe["nombre_batido"],
            "cantidad_procesada": cantidad_dosis,
            "stock_actual": result.get("cantidad_bolsitas_listas", cantidad_dosis),
        }
