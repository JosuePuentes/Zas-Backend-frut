"""12.6 Gastos."""
from datetime import datetime
from fastapi import APIRouter, HTTPException
from bson import ObjectId

from app.database import get_database
from pydantic import BaseModel

router = APIRouter(prefix="/gastos", tags=["Gastos"])


class GastoCreate(BaseModel):
    descripcion: str
    monto: float
    fecha: datetime | None = None


def gasto_to_response(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "descripcion": doc.get("descripcion", ""),
        "monto": doc.get("monto", 0),
        "fecha": doc.get("fecha", datetime.utcnow()),
    }


@router.get("")
async def listar_gastos():
    """Listar gastos."""
    db = get_database()
    cursor = db["gastos"].find({}).sort("fecha", -1)
    return [gasto_to_response(d) async for d in cursor]


@router.post("")
async def registrar_gasto(data: GastoCreate):
    """Registrar gasto."""
    db = get_database()
    doc = {
        "descripcion": data.descripcion,
        "monto": data.monto,
        "fecha": data.fecha or datetime.utcnow(),
    }
    result = await db["gastos"].insert_one(doc)
    doc["_id"] = result.inserted_id
    return gasto_to_response(doc)
