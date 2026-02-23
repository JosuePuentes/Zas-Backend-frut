"""12.1 Inventario Materia Prima - ProductoMateriaPrima, CompraMateriaPrima."""
from datetime import datetime
from typing import Literal
from fastapi import APIRouter, HTTPException, UploadFile
from bson import ObjectId
import csv
import io

from app.database import get_database
from pydantic import BaseModel

router = APIRouter(prefix="/inventario/materia-prima", tags=["Inventario Materia Prima"])


class ProductoMateriaPrimaCreate(BaseModel):
    codigo: str
    descripcion: str
    categoria: Literal["fruta", "adicionales"]
    unidad: Literal["kg", "unidad"]


class ProductoMateriaPrimaUpdate(BaseModel):
    codigo: str | None = None
    descripcion: str | None = None
    categoria: Literal["fruta", "adicionales"] | None = None
    unidad: Literal["kg", "unidad"] | None = None


class CompraMateriaPrimaCreate(BaseModel):
    productoId: str
    cantidad: float
    precioUnitario: float
    fecha: datetime | None = None


def producto_to_response(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "codigo": doc.get("codigo", ""),
        "descripcion": doc.get("descripcion", ""),
        "categoria": doc.get("categoria", "fruta"),
        "unidad": doc.get("unidad", "kg"),
    }


def compra_to_response(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "productoId": doc.get("productoId", ""),
        "cantidad": doc.get("cantidad", 0),
        "precioUnitario": doc.get("precioUnitario", 0),
        "fecha": doc.get("fecha", datetime.utcnow()),
    }


# --- Productos ---
@router.get("/productos")
async def listar_productos():
    """Listar productos de materia prima."""
    db = get_database()
    cursor = db["materia_prima_productos"].find({})
    return [producto_to_response(d) async for d in cursor]


@router.post("/productos")
async def crear_producto(data: ProductoMateriaPrimaCreate):
    """Crear producto de materia prima."""
    db = get_database()
    doc = data.model_dump()
    result = await db["materia_prima_productos"].insert_one(doc)
    doc["_id"] = result.inserted_id
    return producto_to_response(doc)


@router.put("/productos/{id}")
async def actualizar_producto(id: str, data: ProductoMateriaPrimaUpdate):
    """Actualizar producto."""
    db = get_database()
    update = data.model_dump(exclude_none=True)
    if not update:
        raise HTTPException(400, "Sin campos para actualizar")
    doc = await db["materia_prima_productos"].find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": update}, return_document=True
    )
    if not doc:
        raise HTTPException(404, "Producto no encontrado")
    return producto_to_response(doc)


@router.delete("/productos/{id}")
async def eliminar_producto(id: str):
    """Eliminar producto."""
    db = get_database()
    result = await db["materia_prima_productos"].delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(404, "Producto no encontrado")
    return {"message": "Eliminado correctamente"}


# --- Compras ---
@router.post("/compras")
async def registrar_compra(data: CompraMateriaPrimaCreate):
    """Registrar compra de materia prima."""
    db = get_database()
    producto = await db["materia_prima_productos"].find_one({"_id": ObjectId(data.productoId)})
    if not producto:
        raise HTTPException(404, "Producto no encontrado")
    doc = {
        "productoId": data.productoId,
        "cantidad": data.cantidad,
        "precioUnitario": data.precioUnitario,
        "fecha": data.fecha or datetime.utcnow(),
    }
    result = await db["materia_prima_compras"].insert_one(doc)
    doc["_id"] = result.inserted_id
    return compra_to_response(doc)


# --- Import Excel/CSV ---
@router.post("/import-excel")
async def importar_csv(file: UploadFile):
    """Importar productos desde CSV. Columnas: codigo, descripcion, categoria."""
    if not file.filename or not file.filename.lower().endswith((".csv", ".xlsx")):
        raise HTTPException(400, "Archivo debe ser CSV")
    content = await file.read()
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = content.decode("latin-1")
    reader = csv.DictReader(io.StringIO(text))
    db = get_database()
    col = db["materia_prima_productos"]
    creados = 0
    for row in reader:
        codigo = (row.get("codigo") or "").strip()
        descripcion = (row.get("descripcion") or "").strip()
        categoria = (row.get("categoria") or "fruta").strip().lower()
        if categoria not in ("fruta", "adicionales"):
            categoria = "fruta"
        unidad = "kg" if categoria == "fruta" else "unidad"
        if not codigo or not descripcion:
            continue
        existing = await col.find_one({"codigo": codigo})
        if existing:
            continue
        await col.insert_one({
            "codigo": codigo,
            "descripcion": descripcion,
            "categoria": categoria,
            "unidad": unidad,
        })
        creados += 1
    return {"message": f"Importados {creados} productos"}
