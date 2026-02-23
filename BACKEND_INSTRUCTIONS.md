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

## 7. Permisos
- pedidos, sucursales, finanzas-global (para rol master)
