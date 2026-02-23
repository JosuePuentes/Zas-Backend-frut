# Instrucciones del Backend - Especificación Técnica

## 1. Autenticación

### Login con tipo
- **Admins**: login con `usuario` (o `email`) + `password`
- **Clientes**: login con `email` + `password`
- Campo `usuario` en la tabla de usuarios administrativos
- Endpoint `POST /auth/login` acepta `tipo: 'admin' | 'cliente'` para distinguir el flujo

### Endpoints Auth
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/auth/register` | Registro (email, password, nombre, telefono, rol) |
| POST | `/auth/login` | Login con `tipo: 'admin' \| 'cliente'` |

### Body Login
```json
{
  "email": "admin@ejemplo.com",
  "password": "***",
  "tipo": "admin"
}
```
Para admin: `email` puede ser usuario o email. Para cliente: solo email.

---

## 2. Anuncios y Banners

### Anuncios diarios
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/anuncios` | Listar (query: `activo_only=true` para solo activos) |
| POST | `/anuncios` | Crear |
| GET | `/anuncios/{id}` | Obtener |
| PATCH | `/anuncios/{id}` | Actualizar |
| DELETE | `/anuncios/{id}` | Eliminar |

**Body crear:** `{ texto, enlace?, activo? }`

### Banners
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/banners` | Listar (ordenados, `activo_only=true`) |
| POST | `/banners` | Crear |
| GET | `/banners/{id}` | Obtener |
| PATCH | `/banners/{id}` | Actualizar |
| DELETE | `/banners/{id}` | Eliminar |

**Body crear:** `{ imagen_url, enlace?, orden?, activo? }`

### Paneles publicidad
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/paneles` | Listar (ordenados, `activo_only=true`) |
| POST | `/paneles` | Crear |
| GET | `/paneles/{id}` | Obtener |
| PATCH | `/paneles/{id}` | Actualizar |
| DELETE | `/paneles/{id}` | Eliminar |

**Body crear:** `{ imagen_url, enlace?, orden?, activo? }`

---

## 3. Soporte

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/soporte` | Crear mensaje (clienteId, mensaje, asunto?) |
| GET | `/soporte` | Listar mensajes (admin) |
| PATCH | `/soporte/{id}/read` | Marcar como leído |

---

## 4. Compras del cliente

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/compras` | Listar compras del cliente autenticado |

**Requiere:** `Authorization: Bearer <token>`

---

## 5. Ventas (POS)

Al crear venta desde el frontend del cliente, incluir `cliente_id` en el body para vincular la compra:

```json
{
  "items": [...],
  "cliente_id": "ID_DEL_CLIENTE"
}
```

---

## 6. Usuarios

Al crear admin: incluir `usuario` para login.

```json
{
  "email": "admin@zas.com",
  "password": "***",
  "nombre": "Admin",
  "usuario": "admin",
  "rol": "admin"
}
```
