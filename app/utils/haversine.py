"""Cálculo de distancia Haversine entre coordenadas."""
import math


def haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Distancia en km entre dos puntos (lat, lng)."""
    R = 6371  # Radio de la Tierra en km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def sucursal_mas_cercana(lat: float, lng: float, sucursales: list[dict]) -> dict | None:
    """Retorna la sucursal activa más cercana a (lat, lng)."""
    activas = [s for s in sucursales if s.get("activa", True)]
    if not activas:
        return None
    mejor = min(
        activas,
        key=lambda s: haversine_km(lat, lng, s.get("lat", 0), s.get("lng", 0)),
    )
    return mejor
