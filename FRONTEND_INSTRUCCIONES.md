# Instrucciones para el Frontend - Zas! Batidos

Guía para conectar tu frontend React/Next.js con el backend.

---

## 1. URL Base de la API

```javascript
// Desarrollo local
const API_BASE = "http://localhost:8000";

// Producción (cuando despliegues el backend)
const API_BASE = "https://tu-backend.railway.app"; // o tu URL
```

---

## 2. Endpoints Disponibles

### Materia Prima (`/inventory-raw`)
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/inventory-raw` | Listar toda la materia prima |
| POST | `/inventory-raw` | Crear materia prima |
| GET | `/inventory-raw/{id}` | Obtener por ID |
| PATCH | `/inventory-raw/{id}` | Actualizar |
| DELETE | `/inventory-raw/{id}` | Eliminar |

**Body para crear materia prima:**
```json
{
  "nombre": "Cambur",
  "cantidad_total": 5000,
  "costo_por_unidad": 0.5,
  "unidad_medida": "g",
  "stock_minimo": 1000,
  "fecha_ingreso": "2025-02-22T00:00:00Z",
  "es_desechable": false
}
```

---

### Recetas (`/recipes`)
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/recipes` | Listar recetas |
| POST | `/recipes` | Crear receta |
| GET | `/recipes/{id}` | Obtener por ID |
| PATCH | `/recipes/{id}` | Actualizar |
| DELETE | `/recipes/{id}` | Eliminar |

**Body para crear receta:**
```json
{
  "nombre_batido": "Batido de Cambur",
  "ingredientes": [
    { "materia_prima_id": "ID_OBJECTID_MATERIA_PRIMA", "cantidad_gramos": 150 }
  ],
  "precio_sugerido": 3.50
}
```

---

### Producción (`/production`)
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/production/procesar-dosis` | Procesar N dosis de un batido |

**Body:**
```json
{
  "recipe_id": "ID_DE_LA_RECETA",
  "cantidad_dosis": 10
}
```

---

### Disponibilidad (`/availability`)
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/availability/batidos` | Disponibilidad de cada batido |

**Respuesta:**
```json
[
  {
    "recipe_id": "...",
    "nombre_batido": "Batido de Cambur",
    "stock_dosis": 5,
    "producibles_con_materia_prima": 20,
    "total_disponible": 25,
    "precio_sugerido": 3.50
  }
]
```

---

### Ventas / POS (`/sales`)
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/sales` | Cerrar venta (actualiza inventarios) |
| GET | `/sales?limit=50` | Listar ventas recientes |

**Body para cerrar venta:**
```json
{
  "items": [
    {
      "recipe_id": "ID_RECETA",
      "nombre_batido": "Batido de Cambur",
      "cantidad": 1,
      "precio_unitario": 3.50,
      "extras": [
        {
          "materia_prima_id": "ID_GALLETAS",
          "nombre": "Galletas",
          "cantidad": 1,
          "precio_extra": 0.50
        }
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
```

---

### Planificación (`/planning`)
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/planning/lista-compras` | Lista de compras (stock < mínimo) |

---

### Reportes (`/reports`)
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/reports/utilidad?fecha_inicio=&fecha_fin=` | Reporte de utilidad |
| GET | `/reports/mas-vendidos?limite=10` | Batidos más vendidos |
| GET | `/reports/mayor-margen?limite=10` | Mayor margen de ganancia |

---

### Alertas (`/alerts`)
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/alerts/caducidad?dias_antiguedad=3` | Materia prima por antigüedad |

---

## 3. Ejemplo de Cliente API (React/Next.js)

```typescript
// lib/api.ts
const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function fetchApi<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    headers: { "Content-Type": "application/json", ...options?.headers },
    ...options,
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

// Ejemplos
export const api = {
  getMateriaPrima: () => fetchApi("/inventory-raw"),
  getRecetas: () => fetchApi("/recipes"),
  getDisponibilidad: () => fetchApi("/availability/batidos"),
  procesarDosis: (recipeId: string, cantidad: number) =>
    fetchApi("/production/procesar-dosis", {
      method: "POST",
      body: JSON.stringify({ recipe_id: recipeId, cantidad_dosis: cantidad }),
    }),
  crearVenta: (items: SaleItem[]) =>
    fetchApi("/sales", {
      method: "POST",
      body: JSON.stringify({ items }),
    }),
  getListaCompras: () => fetchApi("/planning/lista-compras"),
  getReporteUtilidad: (fechaInicio?: string, fechaFin?: string) =>
    fetchApi(`/reports/utilidad?fecha_inicio=${fechaInicio || ""}&fecha_fin=${fechaFin || ""}`),
  getMasVendidos: (limite = 10) => fetchApi(`/reports/mas-vendidos?limite=${limite}`),
  getAlertasCaducidad: () => fetchApi("/alerts/caducidad"),
};
```

---

## 4. Variables de Entorno (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Para producción (Vercel):
```env
NEXT_PUBLIC_API_URL=https://tu-backend-desplegado.com
```

---

## 5. Flujo de la Interfaz POS

1. **Cargar pantalla**: `GET /availability/batidos` → mostrar batidos con stock disponible.
2. **Buscador**: Filtrar por `nombre_batido` en el cliente.
3. **Al hacer clic en batido**: Abrir modal con extras (lista de `inventory_raw` donde `es_desechable=false`).
4. **Añadir al carrito**: Item con cantidad, extras, precio.
5. **Cerrar venta**: `POST /sales` con todos los items.

---

## 6. CORS

El backend ya tiene CORS habilitado para todos los orígenes (`allow_origins=["*"]`). Para producción, considera restringir a tu dominio de Vercel.

---

## 7. Documentación Interactiva

Con el backend corriendo, visita: **http://localhost:8000/docs**

Ahí puedes probar todos los endpoints directamente.
