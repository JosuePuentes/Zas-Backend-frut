# Prompt para IA del Frontend - Zas! Batidos

Copia y pega este prompt completo a tu IA (Cursor, ChatGPT, etc.) para que construya el frontend.

---

## PROMPT

```
Contexto:
Necesito un frontend React/Next.js para una tienda de batidos. El backend ya está desplegado y funcionando.

URL de la API: https://zas-backend-frut.onrender.com

Stack: React + Next.js + Tailwind CSS. Listo para desplegar en Vercel.

---

## Endpoints del Backend (ya funcionando)

### Materia Prima
- GET /inventory-raw → Listar materia prima
- POST /inventory-raw → Crear (body: nombre, cantidad_total, costo_por_unidad, unidad_medida, stock_minimo, fecha_ingreso?, es_desechable?)

### Recetas
- GET /recipes → Listar recetas de batidos
- POST /recipes → Crear (body: nombre_batido, ingredientes[{materia_prima_id, cantidad_gramos}], precio_sugerido)

### Disponibilidad (para el POS)
- GET /availability/batidos → Retorna cada batido con: recipe_id, nombre_batido, stock_dosis, producibles_con_materia_prima, total_disponible, precio_sugerido

### Producción
- POST /production/procesar-dosis → (body: recipe_id, cantidad_dosis) Procesa materia prima en bolsitas

### Ventas (POS)
- POST /sales → Cerrar venta (body: items[])
  Cada item: recipe_id, nombre_batido, cantidad, precio_unitario, extras[], costo_envase, envase_items[]
  extras: [{materia_prima_id, nombre, cantidad, precio_extra}]
  envase_items: [{materia_prima_id, cantidad}] para vaso, tapa, pitillo

### Planificación
- GET /planning/lista-compras → Stock actual vs mínimo

### Reportes
- GET /reports/utilidad → Reporte de ganancia
- GET /reports/mas-vendidos?limite=10 → Batidos más vendidos

### Alertas
- GET /alerts/caducidad → Materia prima por antigüedad (usar primero)

---

## Módulos a implementar

### 1. Punto de Venta (POS) - Principal
- Interfaz responsive con Tailwind CSS
- Buscador de productos (filtrar batidos por nombre)
- Al hacer clic en un batido: modal para añadir EXTRAS (Galletas, Pistacho, etc.) que incrementan el precio
- Carrito de compras
- Botón "Cerrar venta" que llama POST /sales con todos los items
- Mostrar disponibilidad: usar GET /availability/batidos para saber cuántos de cada batido hay

### 2. Módulo de Producción
- Listar recetas
- Input: "Procesar X dosis de [Batido]"
- Botón que llama POST /production/procesar-dosis

### 3. Módulo de Planificación
- Mostrar GET /planning/lista-compras
- Lista de compras: items con stock_actual < stock_minimo

### 4. Dashboard
- Gráfico "Lo más vendido" (usar Recharts) con GET /reports/mas-vendidos
- Gráfico o card de utilidad con GET /reports/utilidad

### 5. Gestión de Inventario (opcional)
- CRUD de materia prima (inventory-raw)
- CRUD de recetas (recipes)

### 6. Alertas de Caducidad
- Mostrar GET /alerts/caducidad: materia prima ordenada por fecha_ingreso (usar primero la más antigua)

---

## Variables de entorno del frontend

NEXT_PUBLIC_API_URL=https://zas-backend-frut.onrender.com

---

## Diseño
- Interfaz limpia con Tailwind CSS
- POS responsive
- Un solo botón para cerrar venta que actualiza todo
- Considerar que cada batido usa: vaso + tapa + pitillo (envase_items) - el frontend debe enviarlos en cada item de venta si están configurados como materia prima

---

## Ejemplo de body para cerrar venta

{
  "items": [
    {
      "recipe_id": "ID_DE_LA_RECETA",
      "nombre_batido": "Batido de Cambur",
      "cantidad": 1,
      "precio_unitario": 3.50,
      "extras": [
        { "materia_prima_id": "ID_GALLETAS", "nombre": "Galletas", "cantidad": 1, "precio_extra": 0.50 }
      ],
      "costo_envase": 0.15,
      "envase_items": [
        { "materia_prima_id": "ID_VASO", "cantidad": 1 },
        { "materia_prima_id": "ID_TAPA", "cantidad": 1 },
        { "materia_prima_id": "ID_PITILLO", "cantidad": 1 }
      ]
    }
  ]
}

Nota: Si no hay vaso/tapa/pitillo configurados en materia prima, envase_items puede ir vacío y costo_envase en 0.
```

---

## Cómo usar

1. Copia todo el contenido entre las comillas invertidas (desde "Contexto:" hasta el final del ejemplo JSON)
2. Pégalo en tu IA (Cursor, ChatGPT, Claude, etc.)
3. La IA tendrá toda la información para construir el frontend
