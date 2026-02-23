"""Endpoints para inventario de dosis."""
from fastapi import APIRouter, HTTPException
from bson import ObjectId

from app.database import get_database
from app.schemas.inventory_dosis import InventoryDosisCreate, InventoryDosisResponse

router = APIRouter(prefix="/inventory-dosis", tags=["Inventario Dosis"])


def doc_to_response(doc) -> dict:
    """Convertir documento MongoDB a respuesta."""
    return {
        "id": str(doc["_id"]),
        "recipe_id": doc["recipe_id"],
        "cantidad_bolsitas_listas": doc["cantidad_bolsitas_listas"],
    }


@router.get("", response_model=list[InventoryDosisResponse])
async def listar_inventario_dosis():
    """Listar inventario de dosis por receta."""
    db = get_database()
    cursor = db["inventory_dosis"].find({})
    return [doc_to_response(doc) async for doc in cursor]


@router.post("", response_model=InventoryDosisResponse)
async def crear_inventario_dosis(data: InventoryDosisCreate):
    """Crear o inicializar inventario de dosis para una receta."""
    db = get_database()
    existing = await db["inventory_dosis"].find_one({"recipe_id": data.recipe_id})
    if existing:
        raise HTTPException(400, "Ya existe inventario para esta receta")
    doc = data.model_dump()
    result = await db["inventory_dosis"].insert_one(doc)
    doc["_id"] = result.inserted_id
    return doc_to_response(doc)
