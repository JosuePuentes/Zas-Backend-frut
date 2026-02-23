# Instrucciones del Backend - Auth, Users, Notifications

## Endpoints implementados

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/auth/register` | Registro (incluir telefono) |
| POST | `/auth/login` | Login |
| GET | `/users` | Listar usuarios y clientes |
| POST | `/users` | Crear usuario (incluir telefono) |
| GET | `/notifications` | Listar notificaciones |
| PATCH | `/notifications/{id}/read` | Marcar notificación como leída |
| PATCH | `/notifications/read-all` | Marcar todas como leídas |

## Modelo de usuario

```json
{
  "email": "string",
  "password": "string",
  "nombre": "string",
  "telefono": "string",
  "rol": "string",
  "permisos": ["string"],
  "createdAt": "datetime"
}
```

## Lógica al registrar cliente

Al registrar un cliente (`POST /auth/register` con `rol: "cliente"`):

1. Crear el usuario en la base de datos
2. Crear una notificación: `{ tipo: 'nuevo_cliente', mensaje: 'Nuevo cliente registrado: [nombre]' }`

## Integración en el frontend

1. **AuthContext**: Sustituir el uso de `localStorage` por llamadas a la API:
   - `POST /auth/register` para registro
   - `POST /auth/login` para login
   - Guardar el token JWT en localStorage/state

2. **NotificationsContext**: Consumir los endpoints de notificaciones:
   - `GET /notifications` para listar
   - `PATCH /notifications/{id}/read` para marcar una
   - `PATCH /notifications/read-all` para marcar todas

3. **Headers**: Enviar el token JWT en todas las peticiones protegidas:
   ```
   Authorization: Bearer <token>
   ```

## Ejemplo de respuestas

### POST /auth/register
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": "...",
    "email": "cliente@ejemplo.com",
    "nombre": "Juan Pérez",
    "telefono": "1234567890",
    "rol": "cliente",
    "permisos": [],
    "createdAt": "2025-02-23T..."
  }
}
```

### POST /auth/login
Misma estructura que register.

### GET /notifications
```json
[
  {
    "id": "...",
    "tipo": "nuevo_cliente",
    "mensaje": "Nuevo cliente registrado: Juan Pérez",
    "leida": false,
    "createdAt": "2025-02-23T..."
  }
]
```

## Variable de entorno

Para producción, configurar en Render:

| Key | Value |
|-----|-------|
| `JWT_SECRET` | Clave secreta segura para firmar tokens |
