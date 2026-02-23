"""Endpoints de pedidos online."""
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId

from app.database import get_database
from app.auth import require_auth
from app.utils.haversine import sucursal_mas_cercana
from pydantic import BaseModel

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


class ItemPedido(BaseModel):
    recipe_id: str
    nombre_batido: str
    cantidad: int = 1
    precio_unitario: float
    extras: list[dict] = []


class PedidoCreate(BaseModel):
    cliente_id: str
    items: list[ItemPedido]
    total: float
    ubicacion_lat: float = 0
    ubicacion_lng: float = 0
    direccion_entrega: str = ""
    notas: str = ""


class PedidoEstadoUpdate(BaseModel):
    estado: str  # pendiente, preparando, listo, enviado, entregado, cancelado


class PedidoSucursalUpdate(BaseModel):
    sucursal_id: str


def _require_master_or_admin(current_user: dict = Depends(require_auth)):
    """Requerir admin o master."""
    rol = current_user.get("rol")
    if rol not in ("admin", "master"):
        raise HTTPException(403, "Acceso denegado")
    return current_user


def pedido_to_response(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "clienteId": doc.get("clienteId", ""),
        "sucursalId": doc.get("sucursalId", ""),
        "items": doc.get("items", []),
        "total": doc.get("total", 0),
        "estado": doc.get("estado", "pendiente"),
        "ubicacion": doc.get("ubicacion", {}),
        "direccionEntrega": doc.get("direccionEntrega", ""),
        "notas": doc.get("notas", ""),
        "createdAt": doc.get("createdAt", datetime.utcnow()),
    }


@router.post("/pedidos")
async def crear_pedido(data: PedidoCreate):
    """Crear pedido. Asigna sucursal más cercana por Haversine si hay ubicación."""
    db = get_database()
    sucursal_id = ""

    if data.ubicacion_lat and data.ubicacion_lng:
        cursor = db["sucursales"].find({"activa": True})
        sucursales = [s async for s in cursor]
        sucursal = sucursal_mas_cercana(data.ubicacion_lat, data.ubicacion_lng, sucursales)
        if sucursal:
            sucursal_id = str(sucursal["_id"])

    doc = {
        "clienteId": data.cliente_id,
        "sucursalId": sucursal_id,
        "items": [i.model_dump() for i in data.items],
        "total": data.total,
        "estado": "pendiente",
        "ubicacion": {"lat": data.ubicacion_lat, "lng": data.ubicacion_lng},
        "direccionEntrega": data.direccion_entrega,
        "notas": data.notas,
        "createdAt": datetime.utcnow(),
    }
    result = await db["pedidos"].insert_one(doc)
    doc["_id"] = result.inserted_id
    return pedido_to_response(doc)


@router.get("/cliente/pedidos")
async def mis_pedidos(current_user: dict = Depends(require_auth)):
    """Mis pedidos (cliente autenticado)."""
    user_id = current_user.get("sub")
    db = get_database()
    cursor = db["pedidos"].find({"clienteId": user_id}).sort("createdAt", -1)
    return [pedido_to_response(d) async for d in cursor]


@router.get("/admin/pedidos")
async def listar_pedidos_admin(
    sucursal_id: Optional[str] = None,
    estado: Optional[str] = None,
    current_user: dict = Depends(_require_master_or_admin),
):
    """Listar pedidos con filtros (admin). Master ve todos, admin ve solo su sucursal."""
    db = get_database()
    query = {}
    if current_user.get("rol") != "master" and current_user.get("sucursalId"):
        query["sucursalId"] = current_user.get("sucursalId")
    elif sucursal_id:
        query["sucursalId"] = sucursal_id
    if estado:
        query["estado"] = estado

    cursor = db["pedidos"].find(query).sort("createdAt", -1)
    return [pedido_to_response(d) async for d in cursor]


@router.patch("/admin/pedidos/{id}/estado")
async def cambiar_estado_pedido(id: str, data: PedidoEstadoUpdate, current_user: dict = Depends(_require_master_or_admin)):
    """Cambiar estado del pedido."""
    db = get_database()
    pedido = await db["pedidos"].find_one({"_id": ObjectId(id)})
    if not pedido:
        raise HTTPException(404, "Pedido no encontrado")
    if current_user.get("rol") != "master" and pedido.get("sucursalId") != current_user.get("sucursalId"):
        raise HTTPException(403, "No puedes modificar pedidos de otra sucursal")

    doc = await db["pedidos"].find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": {"estado": data.estado}}, return_document=True
    )
    return pedido_to_response(doc)


@router.patch("/admin/pedidos/{id}/sucursal")
async def asignar_sucursal_pedido(id: str, data: PedidoSucursalUpdate, current_user: dict = Depends(_require_master_or_admin)):
    """Asignar sucursal al pedido (solo master)."""
    if current_user.get("rol") != "master":
        raise HTTPException(403, "Solo master puede asignar sucursal")

    db = get_database()
    doc = await db["pedidos"].find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": {"sucursalId": data.sucursal_id}}, return_document=True
    )
    if not doc:
        raise HTTPException(404, "Pedido no encontrado")
    return pedido_to_response(doc)
