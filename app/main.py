"""Zas! Backend - Sistema de Gestión de Batidos."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import connect_to_mongo, close_mongo_connection
from app.routers import (
    auth,
    users,
    notifications,
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
