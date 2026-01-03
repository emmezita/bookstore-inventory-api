# Bookstore Inventory API

API REST para gestión de inventario de librerías con validación de precios en tiempo real mediante tasas de cambio.

## Tecnologías

- Python 3.12+
- Django 6.0
- Django REST Framework 3.14
- PostgreSQL 15
- Docker & Docker Compose

## Requisitos Previos

- Python 3.12 o superior
- Docker y Docker Compose
- Git

## Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/bookstore-inventory-api.git
cd bookstore-inventory-api
```

### 2. Crear y activar entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus configuraciones (opcional)
```

### 5. Iniciar base de datos con Docker

```bash
docker-compose up -d db
```

### 6. Ejecutar migraciones

```bash
python manage.py migrate
```

### 7. Cargar datos de ejemplo (opcional)

```bash
python manage.py seed_books
```

### 8. Crear superusuario (opcional)

```bash
python manage.py createsuperuser
```

### 9. Iniciar servidor de desarrollo

```bash
python manage.py runserver
```

La API estará disponible en: `http://localhost:8000/api/`

### Alternativa: Ejecutar todo con Docker

```bash
# Construir y levantar los servicios
docker-compose up --build

# En otra terminal, cargar datos de ejemplo
docker-compose exec api python manage.py seed_books
```

## Endpoints

### CRUD de Libros

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/books/` | Crear un nuevo libro |
| GET | `/api/books/` | Listar todos los libros (paginado) |
| GET | `/api/books/{id}/` | Obtener un libro por ID |
| PUT | `/api/books/{id}/` | Actualizar un libro |
| DELETE | `/api/books/{id}/` | Eliminar un libro |

### Endpoints Adicionales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/books/search/?category={category}` | Buscar libros por categoría |
| GET | `/api/books/low-stock/?threshold={n}` | Listar libros con stock bajo |
| POST | `/api/books/{id}/calculate-price/` | Calcular precio de venta sugerido |

## Ejemplos de Uso

### Crear un libro

```bash
curl -X POST http://localhost:8000/api/books/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "El Quijote",
    "author": "Miguel de Cervantes",
    "isbn": "978-84-376-0494-7",
    "cost_usd": "15.99",
    "stock_quantity": 25,
    "category": "Literatura Clásica",
    "supplier_country": "ES"
  }'
```

Respuesta:
```json
{
  "id": 1,
  "title": "El Quijote",
  "author": "Miguel de Cervantes",
  "isbn": "978-84-376-0494-7",
  "cost_usd": "15.99",
  "selling_price_local": null,
  "stock_quantity": 25,
  "category": "Literatura Clásica",
  "supplier_country": "ES",
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z"
}
```

### Calcular precio de venta

```bash
curl -X POST http://localhost:8000/api/books/1/calculate-price/
```

Respuesta:
```json
{
  "book_id": 1,
  "cost_usd": 15.99,
  "exchange_rate": 0.92,
  "cost_local": 14.71,
  "margin_percentage": 40,
  "selling_price_local": 20.59,
  "currency": "EUR",
  "calculation_timestamp": "2025-01-15T10:30:00Z"
}
```

### Buscar por categoría

```bash
curl "http://localhost:8000/api/books/search/?category=Literatura"
```

### Libros con stock bajo

```bash
curl "http://localhost:8000/api/books/low-stock/?threshold=10"
```

## Reglas de Negocio

- `cost_usd` debe ser mayor a 0
- `stock_quantity` no puede ser negativo
- `isbn` debe tener formato válido (10 o 13 dígitos)
- No se permiten libros duplicados (mismo ISBN)
- Si la API de tasas de cambio falla, se usa una tasa por defecto
- Margen de ganancia aplicado: 40%

## Países y Monedas Soportados

| País | Código | Moneda |
|------|--------|--------|
| España | ES | EUR |
| Estados Unidos | US | USD |
| México | MX | MXN |
| Colombia | CO | COP |
| Argentina | AR | ARS |
| Chile | CL | CLP |
| Perú | PE | PEN |
| Brasil | BR | BRL |
| Reino Unido | GB | GBP |

## Estructura del Proyecto

```
bookstore-inventory-api/
├── books/
│   ├── management/
│   │   └── commands/
│   │       └── seed_books.py
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── services.py
│   ├── urls.py
│   └── views.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── postman_collection.json
├── README.md
└── requirements.txt
```

## Colección Postman

Importa el archivo `postman_collection.json` en Postman para probar todos los endpoints.

## Autor

Estefany Torres