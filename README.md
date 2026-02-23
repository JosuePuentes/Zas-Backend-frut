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

## Instalación

```bash
# Crear entorno virtual
python -m venv venv
venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Copiar variables de entorno
copy .env.example .env
# Editar .env con tu URL de MongoDB
```

## Ejecutar

```bash
python run.py
# o
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API disponible en: **http://localhost:8000**  
Documentación Swagger: **http://localhost:8000/docs**

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
