# Proyecto Tienda - API

API en Flask para gestionar una tienda de barrio. Incluye módulos de usuarios, productos, categorías, clientes, inventarios, pedidos, facturas y reportes.

## Requisitos

- Python 3.10+
- MySQL

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Variables de entorno

Crea un archivo `.env` en la raíz con:

```env
MYSQL_HOST=localhost
MYSQL_USER=tu_usuario
MYSQL_PASSWORD=tu_password
MYSQL_DATABASE=tu_bd
MYSQL_PORT=3306
SECRET_KEY=tu_secret_key
API_KEY=tu_api_key
FRONTEND_URL=http://localhost:3000
```

## Ejecución

```bash
python app.py
```

La API quedará disponible en `http://localhost:5000`.

## Autenticación

- **JWT**: se envía en el header `Authorization` con el formato:

  ```
  Authorization: Bearer <token>
  ```

- **API Key**: se envía en el header `X-API-KEY`:

  ```
  X-API-KEY: <api_key>
  ```

## Swagger

La documentación interactiva está disponible en:

```
http://localhost:5000/swagger
```
