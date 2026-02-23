"""Zas! Backend - Sistema de Gestión de Batidos."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import connect_to_mongo, close_mongo_connection
from app.routers import (
    auth,
    users,
    notifications,
    sucursales,
    pedidos,
    admin_finanzas,
    admin_soporte,
    home,
    admin_content,
    soporte,
    compras,
    inventory_raw,
    inventory_dosis,
    recipes,
    production,
    availability,
    sales,
    planning,
    reports,
    alerts,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ciclo de vida: conectar/desconectar MongoDB."""
    await connect_to_mongo()
    # Seed usuario master si no existe
    from app.database import get_database
    from app.auth import hash_password
    from datetime import datetime
    db = get_database()
    if db is not None:
        try:
            master = await db["users"].find_one({"rol": "master"})
            master_doc = {
                "email": "master@zas.com",
                "usuario": "master",
                "password_hash": hash_password("clave123"),
                "nombre": "Master",
                "telefono": "",
                "rol": "master",
                "permisos": ["pedidos", "sucursales", "finanzas-global"],
                "sucursalId": "",
                "ubicacion": {},
                "createdAt": datetime.utcnow(),
            }
            if not master:
                await db["users"].insert_one(master_doc)
            else:
                await db["users"].update_one(
                    {"rol": "master"},
                    {"$set": {"password_hash": master_doc["password_hash"]}},
                )
        except Exception as e:
            import logging
            logging.getLogger("uvicorn.error").warning(f"Master seed falló (MongoDB): {e}")
    yield
    await close_mongo_connection()


app = FastAPI(
    title="Zas! API - Gestión de Batidos",
    description="Sistema de gestión para tienda de batidos: materia prima, dosis, ventas y reportes.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(notifications.router)
app.include_router(sucursales.router)
app.include_router(pedidos.router)
app.include_router(admin_finanzas.router)
app.include_router(admin_soporte.router)
app.include_router(home.router)
app.include_router(admin_content.router)
app.include_router(soporte.router)
app.include_router(compras.router)
app.include_router(inventory_raw.router)
app.include_router(inventory_dosis.router)
app.include_router(recipes.router)
app.include_router(production.router)
app.include_router(availability.router)
app.include_router(sales.router)
app.include_router(planning.router)
app.include_router(reports.router)
app.include_router(alerts.router)


@app.get("/")
async def root():
    """Health check."""
    return {
        "message": "Zas! API - Sistema de Gestión de Batidos",
        "docs": "/docs",
        "version": "1.0.0",
    }
