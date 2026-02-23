# Desplegar en Render

## Pasos

### 1. Crear base de datos MongoDB Atlas

1. Entra en [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Crea un cluster gratuito
3. Crea un usuario de base de datos
4. En **Network Access**, añade `0.0.0.0/0` para permitir conexiones desde Render
5. Copia la cadena de conexión (Connection String), por ejemplo:
   ```
   mongodb+srv://usuario:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```

### 2. Conectar el repositorio en Render

1. Entra en [Render](https://render.com) e inicia sesión
2. **New** → **Web Service**
3. Conecta tu cuenta de GitHub y selecciona el repo **Zas-Backend-frut**
4. Si existe `render.yaml`, Render detectará la configuración automáticamente

### 3. Configuración manual (si no usas Blueprint)

Si creas el servicio sin Blueprint, usa:

| Campo | Valor |
|-------|-------|
| **Name** | zas-backend-frut |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |

### 4. Variables de entorno

En **Environment** del servicio, añade:

| Key | Value |
|-----|-------|
| `MONGODB_URL` | Tu connection string de MongoDB Atlas |
| `MONGODB_DB_NAME` | `zas_batidos` |

### 5. Desplegar

Haz clic en **Create Web Service**. Render desplegará el backend y te dará una URL como:

```
https://zas-backend-frut.onrender.com
```

### 6. Frontend

En tu proyecto Next.js (Vercel), configura:

```env
NEXT_PUBLIC_API_URL=https://zas-backend-frut.onrender.com
```

(Usa la URL real que te asigne Render.)

---

**Nota:** En el plan gratuito de Render, el servicio puede tardar unos segundos en responder tras un periodo de inactividad (cold start).
