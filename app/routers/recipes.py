"""Endpoints para recetas (recipes_dosis)."""
from fastapi import APIRouter, HTTPException
from bson import ObjectId

from app.database import get_database
from app.schemas.recipes import RecipeCreate, RecipeUpdate, RecipeResponse

router = APIRouter(prefix="/recipes", tags=["Recetas"])


def doc_to_response(doc) -> dict:
    """Convertir documento MongoDB a respuesta."""
    return {
        "id": str(doc["_id"]),
        "nombre_batido": doc["nombre_batido"],
        "ingredientes": doc["ingredientes"],
        "precio_sugerido": doc["precio_sugerido"],
    }


@router.get("", response_model=list[RecipeResponse])
async def listar_recetas():
    """Listar todas las recetas."""
    db = get_database()
    cursor = db["recipes_dosis"].find({})
    return [doc_to_response(doc) async for doc in cursor]


@router.post("", response_model=RecipeResponse)
async def crear_receta(data: RecipeCreate):
    """Crear receta de batido."""
    db = get_database()
    doc = data.model_dump()
    result = await db["recipes_dosis"].insert_one(doc)
    doc["_id"] = result.inserted_id
    return doc_to_response(doc)


@router.get("/{recipe_id}", response_model=RecipeResponse)
async def obtener_receta(recipe_id: str):
    """Obtener receta por ID."""
    db = get_database()
    doc = await db["recipes_dosis"].find_one({"_id": ObjectId(recipe_id)})
    if not doc:
        raise HTTPException(404, "Receta no encontrada")
    return doc_to_response(doc)


@router.patch("/{recipe_id}", response_model=RecipeResponse)
async def actualizar_receta(recipe_id: str, data: RecipeUpdate):
    """Actualizar receta."""
    db = get_database()
    update = data.model_dump(exclude_none=True)
    result = await db["recipes_dosis"].find_one_and_update(
        {"_id": ObjectId(recipe_id)},
        {"$set": update},
        return_document=True,
    )
    if not result:
        raise HTTPException(404, "Receta no encontrada")
    return doc_to_response(result)


@router.delete("/{recipe_id}")
async def eliminar_receta(recipe_id: str):
    """Eliminar receta."""
    db = get_database()
    result = await db["recipes_dosis"].delete_one({"_id": ObjectId(recipe_id)})
    if result.deleted_count == 0:
        raise HTTPException(404, "Receta no encontrada")
    return {"message": "Eliminado correctamente"}
