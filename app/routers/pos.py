"""12.5 POS - ClientePOS, Venta."""
from datetime import datetime
from typing import Literal, Optional
from fastapi import APIRouter, HTTPException, Query
from bson import ObjectId

from app.database import get_database
from pydantic import BaseModel

router = APIRouter(prefix="/pos", tags=["POS"])


class ClientePOSCreate(BaseModel):
    cedula: str
    nombre: str
    apellido: str = ""
    direccion: str = ""
    telefono: str = ""
    esPuntoVenta: bool = False


class ItemVenta(BaseModel):
    productoId: str
    nombre: str
    cantidad: int = 1
    precioUnitario: float
    total: float | None = None


class VentaPOSCreate(BaseModel):
    numeroFactura: str
    clienteId: str | None = None
    clienteNombre: str = ""
    items: list[ItemVenta]
    subtotal: float
    metodoPago: Literal["efectivo_bs", "efectivo_usd", "zelle", "pago_movil", "transferencia", "binance"]
    montoRecibido: float | None = None
    vuelto: float | None = None
    comprobanteUrl: str | None = None


def cliente_to_response(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "cedula": doc.get("cedula", ""),
        "nombre": doc.get("nombre", ""),
        "apellido": doc.get("apellido", ""),
        "direccion": doc.get("direccion", ""),
        "telefono": doc.get("telefono", ""),
        "esPuntoVenta": doc.get("esPuntoVenta", False),
        "vecesComprado": doc.get("vecesComprado", 0),
        "createdAt": doc.get("createdAt", datetime.utcnow()),
    }


def venta_to_response(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "numeroFactura": doc.get("numeroFactura", ""),
        "clienteId": doc.get("clienteId"),
        "clienteNombre": doc.get("clienteNombre", ""),
        "items": doc.get("items", []),
        "subtotal": doc.get("subtotal", 0),
        "metodoPago": doc.get("metodoPago", ""),
        "montoRecibido": doc.get("montoRecibido"),
        "vuelto": doc.get("vuelto"),
        "comprobanteUrl": doc.get("comprobanteUrl"),
        "fecha": doc.get("fecha", datetime.utcnow()),
    }


# --- Clientes ---
@router.post("/clientes")
async def registrar_cliente(data: ClientePOSCreate):
    """Registrar o actualizar cliente POS (por cédula)."""
    db = get_database()
    existing = await db["clientes_pos"].find_one({"cedula": data.cedula})
    doc = {
        "cedula": data.cedula,
        "nombre": data.nombre,
        "apellido": data.apellido,
        "direccion": data.direccion,
        "telefono": data.telefono,
        "esPuntoVenta": data.esPuntoVenta,
    }
    if existing:
        doc["vecesComprado"] = existing.get("vecesComprado", 0)
        doc["createdAt"] = existing.get("createdAt", datetime.utcnow())
        await db["clientes_pos"].update_one(
            {"_id": existing["_id"]}, {"$set": doc}
        )
        doc["_id"] = existing["_id"]
    else:
        doc["vecesComprado"] = 0
        doc["createdAt"] = datetime.utcnow()
        result = await db["clientes_pos"].insert_one(doc)
        doc["_id"] = result.inserted_id
    return cliente_to_response(doc)


@router.get("/clientes")
async def listar_clientes(esPuntoVenta: Optional[bool] = Query(None)):
    """Listar clientes POS. Filtro esPuntoVenta opcional."""
    db = get_database()
    query = {}
    if esPuntoVenta is not None:
        query["esPuntoVenta"] = esPuntoVenta
    cursor = db["clientes_pos"].find(query).sort("createdAt", -1)
    return [cliente_to_response(d) async for d in cursor]


# --- Ventas ---
@router.post("/ventas")
async def registrar_venta(data: VentaPOSCreate):
    """Registrar venta POS."""
    db = get_database()
    items = [i.model_dump() for i in data.items]
    for it in items:
        if it.get("total") is None:
            it["total"] = it.get("cantidad", 1) * it.get("precioUnitario", 0)
    doc = {
        "numeroFactura": data.numeroFactura,
        "clienteId": data.clienteId,
        "clienteNombre": data.clienteNombre,
        "items": items,
        "subtotal": data.subtotal,
        "metodoPago": data.metodoPago,
        "montoRecibido": data.montoRecibido,
        "vuelto": data.vuelto,
        "comprobanteUrl": data.comprobanteUrl,
        "fecha": datetime.utcnow(),
    }
    result = await db["ventas_pos"].insert_one(doc)
    doc["_id"] = result.inserted_id
    return venta_to_response(doc)


@router.get("/ventas")
async def listar_ventas(
    fechaInicio: Optional[str] = Query(None),
    fechaFin: Optional[str] = Query(None),
):
    """Listar ventas POS. Filtros fechaInicio, fechaFin (ISO)."""
    db = get_database()
    query = {}
    if fechaInicio or fechaFin:
        query["fecha"] = {}
        if fechaInicio:
            try:
                query["fecha"]["$gte"] = datetime.fromisoformat(fechaInicio.replace("Z", "+00:00"))
            except ValueError:
                query["fecha"]["$gte"] = datetime.fromisoformat(fechaInicio + "T00:00:00")
        if fechaFin:
            try:
                query["fecha"]["$lte"] = datetime.fromisoformat(fechaFin.replace("Z", "+00:00"))
            except ValueError:
                query["fecha"]["$lte"] = datetime.fromisoformat(fechaFin + "T23:59:59")
    cursor = db["ventas_pos"].find(query).sort("fecha", -1)
    return [venta_to_response(d) async for d in cursor]
