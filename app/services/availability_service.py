"""Servicio de disponibilidad: cuántos batidos se pueden vender."""
from app.database import get_database


class AvailabilityService:
    """Calcula disponibilidad de batidos."""

    @staticmethod
    async def get_disponibilidad_batidos() -> list[dict]:
        """
        Para cada receta, calcula:
        - Stock de dosis listas
        - Cuántos se pueden producir con materia prima actual
        - Total disponible = stock + producibles
        """
        db = get_database()
        recipes_col = db["recipes_dosis"]
        raw_col = db["inventory_raw"]
        dosis_col = db["inventory_dosis"]

        recipes = await recipes_col.find().to_list(length=1000)
        resultado = []

        for recipe in recipes:
            recipe_id = str(recipe["_id"])
            nombre = recipe["nombre_batido"]
            ingredientes = recipe["ingredientes"]

            # Stock de dosis
            inv_dosis = await dosis_col.find_one({"recipe_id": recipe_id})
            stock_dosis = inv_dosis["cantidad_bolsitas_listas"] if inv_dosis else 0

            # Cuántos se pueden producir con materia prima
            producibles = float("inf")
            for ing in ingredientes:
                mp_id = ing["materia_prima_id"]
                gramos_por_dosis = ing["cantidad_gramos"]

                raw = await raw_col.find_one({"_id": mp_id})
                stock_mp = raw["cantidad_total"] if raw else 0
                producibles_ing = int(stock_mp / gramos_por_dosis) if gramos_por_dosis > 0 else 0
                producibles = min(producibles, producibles_ing)

            if producibles == float("inf"):
                producibles = 0

            total_disponible = stock_dosis + producibles

            resultado.append({
                "recipe_id": recipe_id,
                "nombre_batido": nombre,
                "stock_dosis": stock_dosis,
                "producibles_con_materia_prima": producibles,
                "total_disponible": total_disponible,
                "precio_sugerido": recipe["precio_sugerido"],
            })

        return resultado
