"""Endpoints de autenticación."""
from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from bson import ObjectId

from app.database import get_database
from app.auth import hash_password, verify_password, create_access_token
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


def user_to_response(doc: dict) -> dict:
    """Convertir documento a respuesta (sin password)."""
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


@router.post("/register", response_model=TokenResponse)
async def register(data: RegisterRequest):
    """
    Registro de usuario (principalmente clientes).
    Al registrar un cliente, se crea una notificación.
    """
    db = get_database()
    users_col = db["users"]
    notifications_col = db["notifications"]

    existing = await users_col.find_one({"email": data.email.lower()})
    if existing:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    ubicacion = data.ubicacion.model_dump() if data.ubicacion else {}
    user_doc = {
        "email": data.email.lower(),
        "password_hash": hash_password(data.password),
        "nombre": data.nombre,
        "telefono": data.telefono,
        "rol": data.rol,
        "permisos": [],
        "sucursalId": "",
        "ubicacion": ubicacion,
        "createdAt": datetime.utcnow(),
    }

    result = await users_col.insert_one(user_doc)
    user_doc["_id"] = result.inserted_id

    # Si es cliente, crear notificación
    if data.rol == "cliente":
        notification = {
            "tipo": "nuevo_cliente",
            "mensaje": f"Nuevo cliente registrado: {data.nombre}",
            "leida": False,
            "createdAt": datetime.utcnow(),
        }
        await notifications_col.insert_one(notification)

    token_data = {
        "sub": str(user_doc["_id"]),
        "email": user_doc["email"],
        "rol": user_doc["rol"],
        "sucursalId": user_doc.get("sucursalId", ""),
    }
    token = create_access_token(token_data)

    return TokenResponse(
        access_token=token,
        user=user_to_response(user_doc),
    )


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest):
    """
    Login con tipo: 'admin' | 'cliente'
    - Admin: busca por usuario O email + password
    - Cliente: busca por email + password
    """
    db = get_database()
    users_col = db["users"]

    if data.tipo == "admin":
        # Admin/Master: puede usar usuario o email
        user = await users_col.find_one({
            "$or": [
                {"usuario": data.email},
                {"email": data.email.lower()},
            ],
            "rol": {"$in": ["admin", "master"]},
        })
    else:
        # Cliente: solo email
        user = await users_col.find_one({"email": data.email.lower(), "rol": "cliente"})

    if not user or not verify_password(data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token_data = {
        "sub": str(user["_id"]),
        "email": user["email"],
        "rol": user.get("rol", "cliente"),
        "sucursalId": user.get("sucursalId", ""),
    }
    token = create_access_token(token_data)

    return TokenResponse(
        access_token=token,
        user=user_to_response(user),
    )
