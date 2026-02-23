# Instrucciones del Backend - Especificación Técnica

## 1. Modelos

### Sucursal
- nombre, direccion, lat, lng, telefono, activa

### User
- email, password, nombre, telefono, rol, permisos, sucursalId, ubicacion, createdAt
- Rol master: acceso total
- ubicacion: { lat, lng, direccion } para clientes (delivery)

### Order (Pedido)
- clienteId, sucursalId, items, total, estado, ubicacion, direccionEntrega, notas, createdAt

---

## 2. Sucursales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/sucursales` | Listar sucursales activas (público) |
| GET | `/admin/sucursales` | Listar todas (solo master) |
| POST | `/admin/sucursales` | Crear sucursal (solo master, requiere PIN en body) |
| PUT | `/admin/sucursales/{id}` | Actualizar sucursal |

**PIN:** Variable `PIN_MASTER` en .env (default 1234). En body: `{ ..., "pin": "1234" }`

---

## 3. Pedidos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/pedidos` | Crear pedido (asigna sucursal más cercana por Haversine) |
| GET | `/cliente/pedidos` | Mis pedidos (auth) |
| GET | `/admin/pedidos` | Listar con filtros (admin, filtrado por sucursal si no master) |
| PATCH | `/admin/pedidos/{id}/estado` | Cambiar estado |
| PATCH | `/admin/pedidos/{id}/sucursal` | Asignar sucursal (solo master) |

---

## 4. Finanzas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/admin/finanzas` | Suma ventas todas sucursales (solo master) |

---

## 5. Auth y Usuarios

### Registro público (POST /auth/register)
Solo clientes. No acepta rol ni usuario.
- Body: email, password, nombre, telefono, ubicacion (obligatorio)
- Respuesta: `{ user: {...}, token: "jwt..." }`

### Crear usuarios (POST /users)
Solo admin/master autenticados.
- Cliente: rol, ubicacion obligatorio
- Admin: usuario, permisos, sucursalId
- Master: solo si el usuario actual es master

### Login
- tipo: `admin` | `cliente`
- Admin/Master: usuario o email + password
- Cliente: email + password

### Credenciales de prueba
- **Master:** usuario `master`, email `master@zas.com`, password `master`
- **PIN:** 1234 (variable PIN_MASTER en .env)

---

## 6. Ventas
- Incluir `sucursal_id` y `cliente_id` opcionales al crear venta.

---

## 7. Anuncios, Banners y Paneles

### Modelos
- **Anuncios:** { texto, orden, activo }
- **Banners:** { imagen, titulo, subtitulo, enlace, orden, activo }
- **Paneles:** { imagen, titulo, subtitulo, orden, activo }

### Endpoints públicos (GET)
| GET | `/home/anuncios` | `/home/banners` | `/home/paneles` |

### Endpoints admin (auth admin/master)
| Método | Endpoint | Body |
|--------|----------|------|
| POST | `/admin/anuncios` | { texto } |
| PUT | `/admin/anuncios/{id}` | { texto?, orden?, activo? } |
| DELETE | `/admin/anuncios/{id}` | — |
| POST | `/admin/banners` | { imagen, titulo, subtitulo?, enlace? } |
| PUT | `/admin/banners/{id}` | { imagen?, titulo?, subtitulo?, enlace?, orden?, activo? } |
| DELETE | `/admin/banners/{id}` | — |
| POST | `/admin/paneles` | { imagen, titulo, subtitulo? } |
| PUT | `/admin/paneles/{id}` | { imagen?, titulo?, subtitulo?, orden?, activo? } |
| DELETE | `/admin/paneles/{id}` | — |

---

## 8. Permisos
- pedidos, sucursales, finanzas-global (para rol master)

---

## 12. Sistema de Inventario (Nuevo - Super Fruty)

El frontend usa InventarioContext con localStorage. Para producción, implementa estos modelos y endpoints.

### 12.1 Inventario Materia Prima

**ProductoMateriaPrima:** `{ id, codigo, descripcion, categoria: "fruta"|"adicionales", unidad: "kg"|"unidad" }`
- Fruta → unidad kg
- Adicionales → unidad cantidad

**CompraMateriaPrima:** `{ id, productoId, cantidad, precioUnitario, fecha }`

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/inventario/materia-prima/productos` | Listar productos |
| POST | `/inventario/materia-prima/productos` | Crear producto |
| PUT | `/inventario/materia-prima/productos/:id` | Actualizar |
| DELETE | `/inventario/materia-prima/productos/:id` | Eliminar |
| POST | `/inventario/materia-prima/compras` | Registrar compra |
| POST | `/inventario/materia-prima/import-excel` | Importar CSV (codigo, descripcion, categoria) |

### 12.2 Inventario de Venta

**ProductoInventarioVenta:** `{ id, codigo, descripcion, precio, tamanioVaso, tieneEtiqueta, ingredientes: [{ materiaPrimaId, nombre, gramos }], vasoId?, etiquetaId?, costoVaso?, costoEtiqueta?, cantidad }`

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/inventario/venta` | Listar productos venta |
| POST | `/inventario/venta` | Crear producto |
| PUT | `/inventario/venta/:id` | Actualizar |
| DELETE | `/inventario/venta/:id` | Eliminar |

### 12.3 Inventario Preparación (automático)

Calculado: stock materia prima + recetas inventario venta → bolsitas disponibles por producto.

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/inventario/preparacion` | Lista código, descripción, cantidad, costoUnitario |

### 12.4 Producción

Muestra recetas (gramos por ingrediente) y bolsitas disponibles. Descuento automático al vender en POS o pedidos online.

### 12.5 POS - Punto de Venta

**ClientePOS:** `{ id, cedula, nombre, apellido, direccion, telefono, esPuntoVenta, vecesComprado, createdAt }`

**Venta:** `{ id, numeroFactura, clienteId?, clienteNombre, items: [{ productoId, nombre, cantidad, precioUnitario, total }], subtotal, metodoPago: "efectivo_bs"|"efectivo_usd"|"zelle"|"pago_movil"|"transferencia"|"binance", montoRecibido?, vuelto?, comprobanteUrl?, fecha }`

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/pos/ventas` | Registrar venta |
| POST | `/pos/clientes` | Registrar/actualizar cliente POS |
| GET | `/pos/clientes` | Listar clientes (filtro esPuntoVenta) |
| GET | `/pos/ventas` | Listar ventas (filtro fechaInicio, fechaFin) |

### 12.6 Gastos

**Gasto:** `{ id, descripcion, monto, fecha }`

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/gastos` | Listar gastos |
| POST | `/gastos` | Registrar gasto |

### 12.7 Catálogo Cliente

Muestra solo: código, descripción, precio (sin costo vaso/etiqueta). Productos desde inventario venta.

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/catalogo` | Catálogo público (código, descripción, precio) |

### Integración con módulos existentes

Si ya tienes `inventory_raw`, `inventory_dosis`, `compras` y `sales`, conviene integrar la sección 12 con ellos:
- `inventory_raw` → ProductoMateriaPrima + CompraMateriaPrima (stock = suma de compras)
- `compras` → CompraMateriaPrima
- `inventory_dosis` → Inventario Preparación (calculado)
- `sales` → Venta (POS)
