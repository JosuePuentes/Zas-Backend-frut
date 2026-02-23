"""Endpoints de usuarios."""
from datetime import datetime
from fastapi import APIRouter, HTTPException
from bson import ObjectId

from app.database import get_database
from app.auth import hash_password
from app.schemas.user import UserCreateRequest, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


def user_to_response(doc: dict) -> dict:
    """Convertir documento a respuesta."""
    return {
        "id": str(doc["_id"]),
        "email": doc["email"],
        "nombre": doc["nombre"],
        "telefono": doc.get("telefono", ""),
        "usuario": doc.get("usuario", ""),
        "rol": doc.get("rol", "cliente"),
        "permisos": doc.get("permisos", []),
        "sucursalId": doc.get("sucursalId", ""),
        "ubicacion": doc.get("ubicacion", {}),
        "createdAt": doc.get("createdAt", datetime.utcnow()),
    }


@router.get("", response_model=list[UserResponse])
async def listar_usuarios():
    """Listar usuarios y clientes."""
    db = get_database()
    cursor = db["users"].find({})
    return [user_to_response(doc) async for doc in cursor]


@router.post("", response_model=UserResponse)
async def crear_usuario(data: UserCreateRequest):
    """Crear usuario (incluir teléfono)."""
    db = get_database()
    users_col = db["users"]

    existing = await users_col.find_one({"email": data.email.lower()})
    if existing:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    if data.rol == "admin" and data.usuario:
        existing_user = await users_col.find_one({"usuario": data.usuario})
        if existing_user:
            raise HTTPException(status_code=400, detail="El usuario ya existe")

    ubicacion = data.ubicacion.model_dump() if data.ubicacion else {}
    user_doc = {
        "email": data.email.lower(),
        "password_hash": hash_password(data.password),
        "nombre": data.nombre,
        "telefono": data.telefono,
        "usuario": data.usuario if data.rol in ("admin", "master") else "",
        "rol": data.rol,
        "permisos": data.permisos,
        "sucursalId": data.sucursalId or "",
        "ubicacion": ubicacion,
        "createdAt": datetime.utcnow(),
    }

    result = await users_col.insert_one(user_doc)
    user_doc["_id"] = result.inserted_id

    return user_to_response(user_doc)
