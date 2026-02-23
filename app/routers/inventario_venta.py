"""12.2 Inventario de Venta - ProductoInventarioVenta."""
from datetime import datetime
from fastapi import APIRouter, HTTPException
from bson import ObjectId

from app.database import get_database
from pydantic import BaseModel, Field

router = APIRouter(prefix="/inventario/venta", tags=["Inventario Venta"])


class IngredienteVenta(BaseModel):
    materiaPrimaId: str = Field(..., alias="materiaPrimaId")
    nombre: str
    gramos: float

    model_config = {"populate_by_name": True}


class ProductoInventarioVentaCreate(BaseModel):
    codigo: str
    descripcion: str
    precio: float
    tamanioVaso: str = ""
    tieneEtiqueta: bool = False
    ingredientes: list[IngredienteVenta] = []
    vasoId: str | None = None
    etiquetaId: str | None = None
    costoVaso: float | None = None
    costoEtiqueta: float | None = None
    cantidad: int = 0


class ProductoInventarioVentaUpdate(BaseModel):
    codigo: str | None = None
    descripcion: str | None = None
    precio: float | None = None
    tamanioVaso: str | None = None
    tieneEtiqueta: bool | None = None
    ingredientes: list[IngredienteVenta] | None = None
    vasoId: str | None = None
    etiquetaId: str | None = None
    costoVaso: float | None = None
    costoEtiqueta: float | None = None
    cantidad: int | None = None


def producto_venta_to_response(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "codigo": doc.get("codigo", ""),
        "descripcion": doc.get("descripcion", ""),
        "precio": doc.get("precio", 0),
        "tamanioVaso": doc.get("tamanioVaso", ""),
        "tieneEtiqueta": doc.get("tieneEtiqueta", False),
        "ingredientes": doc.get("ingredientes", []),
        "vasoId": doc.get("vasoId"),
        "etiquetaId": doc.get("etiquetaId"),
        "costoVaso": doc.get("costoVaso"),
        "costoEtiqueta": doc.get("costoEtiqueta"),
        "cantidad": doc.get("cantidad", 0),
    }


@router.get("")
async def listar_productos_venta():
    """Listar productos de inventario venta."""
    db = get_database()
    cursor = db["inventario_venta"].find({})
    return [producto_venta_to_response(d) async for d in cursor]


@router.post("")
async def crear_producto_venta(data: ProductoInventarioVentaCreate):
    """Crear producto de inventario venta."""
    db = get_database()
    doc = data.model_dump()
    result = await db["inventario_venta"].insert_one(doc)
    doc["_id"] = result.inserted_id
    return producto_venta_to_response(doc)


@router.put("/{id}")
async def actualizar_producto_venta(id: str, data: ProductoInventarioVentaUpdate):
    """Actualizar producto de inventario venta."""
    db = get_database()
    update = data.model_dump(exclude_none=True)
    if not update:
        raise HTTPException(400, "Sin campos para actualizar")
    doc = await db["inventario_venta"].find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": update}, return_document=True
    )
    if not doc:
        raise HTTPException(404, "Producto no encontrado")
    return producto_venta_to_response(doc)


@router.delete("/{id}")
async def eliminar_producto_venta(id: str):
    """Eliminar producto de inventario venta."""
    db = get_database()
    result = await db["inventario_venta"].delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(404, "Producto no encontrado")
    return {"message": "Eliminado correctamente"}
