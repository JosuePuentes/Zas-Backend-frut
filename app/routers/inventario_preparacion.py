"""12.3 Inventario Preparación - calculado: stock materia prima + recetas → bolsitas."""
from fastapi import APIRouter
from bson import ObjectId

from app.database import get_database

router = APIRouter(prefix="/inventario/preparacion", tags=["Inventario Preparación"])


@router.get("")
async def listar_preparacion():
    """
    Lista código, descripción, cantidad (bolsitas disponibles), costoUnitario.
    Calculado: stock materia prima + recetas inventario venta → bolsitas por producto.
    """
    db = get_database()
    productos_venta = db["inventario_venta"]
    compras_col = db["materia_prima_compras"]
    productos_mp = db["materia_prima_productos"]

    # Stock por materia prima (suma de compras)
    pipeline_stock = [
        {"$group": {"_id": "$productoId", "total": {"$sum": "$cantidad"}}}
    ]
    cursor = compras_col.aggregate(pipeline_stock)
    stock_mp = {r["_id"]: r["total"] for r in await cursor.to_list(length=1000)}

    # Unidad por producto MP (para convertir kg a gramos si aplica)
    productos_mp_map = {}
    async for p in productos_mp.find({}):
        productos_mp_map[str(p["_id"])] = p

    resultado = []
    async for pv in productos_venta.find({}):
        ingredientes = pv.get("ingredientes", [])
        if not ingredientes:
            cantidad = pv.get("cantidad", 0)
            costo_unit = 0
        else:
            cantidad = float("inf")
            costo_unit = 0
            for ing in ingredientes:
                mp_id = ing.get("materiaPrimaId")
                gramos = ing.get("gramos", 0)
                prod_mp = productos_mp_map.get(mp_id, {})
                stock = stock_mp.get(mp_id, 0)
                unidad = prod_mp.get("unidad", "kg")
                if unidad == "kg":
                    stock_gramos = stock * 1000
                else:
                    stock_gramos = stock
                bolsitas_posibles = stock_gramos / gramos if gramos else 0
                cantidad = min(cantidad, bolsitas_posibles)
                # Costo: precio unitario de compras recientes (simplificado)
                compra = await compras_col.find_one(
                    {"productoId": mp_id},
                    sort=[("fecha", -1)]
                )
                precio_unit = compra.get("precioUnitario", 0) if compra else 0
                if unidad == "kg":
                    costo_por_gramo = precio_unit / 1000
                else:
                    costo_por_gramo = precio_unit
                costo_unit += gramos * costo_por_gramo

            cantidad = int(cantidad) if cantidad != float("inf") else 0

        resultado.append({
            "codigo": pv.get("codigo", ""),
            "descripcion": pv.get("descripcion", ""),
            "cantidad": cantidad,
            "costoUnitario": round(costo_unit, 2),
        })

    return resultado
