# Zas! Backend - Sistema de Gestión de Batidos

Backend en **Python + FastAPI + MongoDB** para una tienda de batidos.

## Estructura del Proyecto

```
Zas!backend-frut/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicación FastAPI
│   ├── config.py            # Configuración
│   ├── database.py          # Conexión MongoDB (Motor)
│   ├── models/              # Modelos de datos
│   │   ├── inventory_raw.py
│   │   ├── recipes_dosis.py
│   │   ├── inventory_dosis.py
│   │   └── sales.py
│   ├── schemas/             # Esquemas Pydantic
│   ├── routers/             # Endpoints API
│   │   ├── inventory_raw.py
│   │   ├── inventory_dosis.py
│   │   ├── recipes.py
│   │   ├── production.py
│   │   ├── availability.py
│   │   ├── sales.py
│   │   ├── planning.py
│   │   ├── reports.py
│   │   └── alerts.py
│   └── services/            # Lógica de negocio
├── requirements.txt
├── .env.example
└── run.py
```

## Colecciones MongoDB

| Colección       | Descripción                                      |
|-----------------|--------------------------------------------------|
| `inventory_raw` | Materia prima (frutas, extras, envases)         |
| `recipes_dosis` | Recetas de batidos (ingredientes por dosis)      |
| `inventory_dosis` | Stock de bolsitas preparadas                   |
| `sales`         | Ventas con items y extras                        |

## Despliegue en Render

1. Conecta tu repositorio en [Render](https://render.com)
2. Crea un **Web Service** y vincula el repo `Zas-Backend-frut`
3. Configuración automática (si usas `render.yaml`):
   - **Build**: `pip install -r requirements.txt`
   - **Start**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Añade la variable de entorno **MONGODB_URL** (usa [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) para la base de datos en la nube)
5. Tu API quedará en `https://zas-backend-frut.onrender.com` (o el nombre que elijas)

## Desarrollo local

```bash
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
copy .env.example .env  # Editar con tu MongoDB
python run.py
```

API local: **http://localhost:8000** | Docs: **http://localhost:8000/docs**

## Endpoints Principales

### Materia Prima
- `GET/POST /inventory-raw` - Listar / Crear
- `GET/PATCH/DELETE /inventory-raw/{id}`

### Recetas
- `GET/POST /recipes` - Listar / Crear
- `GET/PATCH/DELETE /recipes/{id}`

### Producción
- `POST /production/procesar-dosis` - Procesar N dosis (resta materia prima, suma dosis)

### Disponibilidad
- `GET /availability/batidos` - Cuántos batidos se pueden vender

### Ventas (POS)
- `POST /sales` - Cerrar venta (actualización atómica de inventarios)
- `GET /sales` - Listar ventas

### Planificación
- `GET /planning/lista-compras` - Stock actual vs mínimo

### Reportes
- `GET /reports/utilidad` - Ganancia neta
- `GET /reports/mas-vendidos` - Batidos más vendidos
- `GET /reports/mayor-margen` - Mayor margen de ganancia

### Alertas
- `GET /alerts/caducidad` - Materia prima por fecha de ingreso (usar primero)
