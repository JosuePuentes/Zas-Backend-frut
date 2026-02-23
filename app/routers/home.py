"""Endpoints públicos del home: anuncios, banners, paneles."""
from datetime import datetime
from fastapi import APIRouter

from app.database import get_database

router = APIRouter(prefix="/home", tags=["Home"])


def _anuncio_response(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "texto": doc.get("texto", ""),
        "orden": doc.get("orden", 0),
        "activo": doc.get("activo", True),
    }


def _banner_response(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "imagen": doc.get("imagen", ""),
        "titulo": doc.get("titulo", ""),
        "subtitulo": doc.get("subtitulo", ""),
        "enlace": doc.get("enlace", ""),
        "orden": doc.get("orden", 0),
        "activo": doc.get("activo", True),
    }


def _panel_response(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "imagen": doc.get("imagen", ""),
        "titulo": doc.get("titulo", ""),
        "subtitulo": doc.get("subtitulo", ""),
        "orden": doc.get("orden", 0),
        "activo": doc.get("activo", True),
    }


@router.get("/anuncios")
async def listar_anuncios():
    """Listar anuncios activos (público)."""
    db = get_database()
    cursor = db["anuncios"].find({"activo": True}).sort("orden", 1)
    return [_anuncio_response(d) async for d in cursor]


@router.get("/banners")
async def listar_banners():
    """Listar banners activos (público)."""
    db = get_database()
    cursor = db["banners"].find({"activo": True}).sort("orden", 1)
    return [_banner_response(d) async for d in cursor]


@router.get("/paneles")
async def listar_paneles():
    """Listar paneles activos (público)."""
    db = get_database()
    cursor = db["paneles"].find({"activo": True}).sort("orden", 1)
    return [_panel_response(d) async for d in cursor]
