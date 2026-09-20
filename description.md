# Sistema Web de Consulta Estudiantil

## 1. Descripción general

El proyecto consiste en desarrollar una **aplicación web de consulta de información estudiantil**, compuesta por un **frontend**, un **backend desarrollado con Python y FastAPI** y una **base de datos MySQL**.

El sistema permitirá consultar información de estudiantes utilizando diferentes criterios:

- Código
    
- DNI
    
- Apellidos y nombres
    
- Facultad
    
- Escuela profesional
    

La aplicación estará orientada inicialmente a un entorno de prueba y será desplegada utilizando servicios gratuitos o de bajo costo.

---

## 2. Arquitectura general

La aplicación estará dividida en tres componentes principales:

HTTP / HTTPS + JSONUsuarioFrontendAPI REST - FastAPISQLAlchemy(MySQL)

### Componentes

|Componente|Tecnología|Responsabilidad|
|---|---|---|
|Frontend|HTML/CSS/JS o framework web|Interfaz de usuario|
|Backend|Python + FastAPI|Lógica de aplicación|
|API|FastAPI REST|Comunicación frontend/backend|
|ORM|SQLAlchemy|Acceso a datos|
|Driver|PyMySQL|Conexión con MySQL|
|Base de datos|MySQL|Almacenamiento de información|

---

# 3. Estructura de la información

La entidad principal del sistema será el **estudiante**.

```mermaid
erDiagram
    ESTUDIANTE {
        varchar CODIGO PK
        varchar APELLIDOS_Y_NOMBRES
        varchar DNI
        varchar FACULTAD
        varchar ESCUELA_PROFESIONAL
    }
```

Los campos principales serán:

|Campo|Descripción|
|---|---|
|`CODIGO`|Código único del estudiante|
|`APELLIDOS Y NOMBRES`|Nombres completos del estudiante|
|`DNI`|Documento Nacional de Identidad|
|`FACULTAD`|Facultad a la que pertenece|
|`ESCUELA PROFESIONAL`|Escuela profesional a la que pertenece|

---

# 4. Backend

El backend será desarrollado utilizando **Python y FastAPI**.

Su responsabilidad será:

1. Recibir solicitudes del frontend.
    
2. Validar los parámetros recibidos.
    
3. Consultar la base de datos.
    
4. Procesar los resultados.
    
5. Devolver respuestas en formato JSON.
    
6. Gestionar errores HTTP.
    
7. Controlar el acceso a la base de datos.
    

La comunicación seguirá el siguiente flujo:

```mermaid
sequenceDiagram
    actor Usuario
    participant Frontend
    participant API as FastAPI
    participant DB as MySQL

    Usuario->>Frontend: Ingresa criterio de búsqueda
    Frontend->>API: GET /api/estudiantes
    API->>DB: Ejecuta consulta SQL
    DB-->>API: Devuelve registros
    API-->>Frontend: Respuesta JSON
    Frontend-->>Usuario: Muestra resultados
```

---

# 5. Estructura del backend

La estructura inicial será:

```text
backend/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   │
│   └── routers/
│       ├── __init__.py
│       └── estudiantes.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

### Responsabilidad de cada archivo

|Archivo|Función|
|---|---|
|`main.py`|Inicialización de FastAPI|
|`database.py`|Configuración de conexión a MySQL|
|`models.py`|Modelos SQLAlchemy|
|`schemas.py`|Validación de datos con Pydantic|
|`routers/estudiantes.py`|Endpoints de estudiantes|
|`.env`|Variables de entorno|
|`requirements.txt`|Dependencias Python|

---

# 6. Modelo de datos

El modelo SQLAlchemy representará la tabla existente en MySQL.

```python
class Estudiante(Base):
    __tablename__ = "estudiantes"

    codigo = Column(
        "CODIGO",
        String(20),
        primary_key=True
    )

    apellidos_nombres = Column(
        "APELLIDOS Y NOMBRES",
        String(150)
    )

    dni = Column(
        "DNI",
        String(8)
    )

    facultad = Column(
        "FACULTAD",
        String(150)
    )

    escuela_profesional = Column(
        "ESCUELA PROFESIONAL",
        String(150)
    )
```

El backend utilizará nombres compatibles con Python:

```text
MySQL                       Python / API
────────────────────────────────────────────
CODIGO                   →  codigo
APELLIDOS Y NOMBRES      →  apellidos_nombres
DNI                      →  dni
FACULTAD                 →  facultad
ESCUELA PROFESIONAL      →  escuela_profesional
```

De esta manera no es necesario modificar los nombres originales de las columnas de la base de datos.

---

# 7. API REST

La API será el punto de comunicación entre el frontend y la base de datos.

## 7.1 Obtener estudiantes

```http
GET /api/estudiantes
```

Devuelve una lista de estudiantes.

Ejemplo:

```json
[
    {
        "codigo": "20240001",
        "apellidos_nombres": "PEREZ QUISPE JUAN",
        "dni": "12345678",
        "facultad": "INGENIERIA DE PRODUCCION Y SERVICIOS",
        "escuela_profesional": "INGENIERIA DE SISTEMAS"
    }
]
```

---

## 7.2 Buscar por código

```http
GET /api/estudiantes/codigo/{codigo}
```

Ejemplo:

```http
GET /api/estudiantes/codigo/20240001
```

---

## 7.3 Buscar por DNI

```http
GET /api/estudiantes/dni/{dni}
```

Ejemplo:

```http
GET /api/estudiantes/dni/12345678
```

---

## 7.4 Buscar por nombre

```http
GET /api/estudiantes?nombre=perez
```

La búsqueda podrá realizarse parcialmente sobre el campo `APELLIDOS Y NOMBRES`.

---

## 7.5 Filtrar por facultad

```http
GET /api/estudiantes?facultad=ingenieria
```

---

## 7.6 Filtrar por escuela profesional

```http
GET /api/estudiantes?escuela=sistemas
```

---

## 7.7 Combinar filtros

La API permitirá combinar criterios:

```http
GET /api/estudiantes?nombre=perez&facultad=ingenieria&escuela=sistemas
```

El flujo será:

CódigoDNINombreFacultadEscuelaFrontendCriterios de búsquedaBuscar por códigoBuscar por DNIBuscar por nombreFiltrar facultadFiltrar escuelaFastAPI(MySQL)

---

# 8. Formato de respuesta

La API utilizará **JSON** como formato estándar.

Ejemplo:

```json
{
    "codigo": "20240001",
    "apellidos_nombres": "PEREZ QUISPE JUAN",
    "dni": "12345678",
    "facultad": "INGENIERIA DE PRODUCCION Y SERVICIOS",
    "escuela_profesional": "INGENIERIA DE SISTEMAS"
}
```

En caso de que el estudiante no exista, la API responderá con un error HTTP:

```json
{
    "detail": "Estudiante no encontrado"
}
```

con código:

```text
404 Not Found
```

---

# 9. Frontend

El frontend será la interfaz utilizada por los usuarios para realizar las consultas.

La interfaz inicial podrá contener:

```text
┌──────────────────────────────────────────────────┐
│             CONSULTA DE ESTUDIANTES              │
├──────────────────────────────────────────────────┤
│                                                  │
│ Código:              [________________]          │
│ DNI:                 [________________]          │
│ Apellidos/Nombres:   [________________]          │
│ Facultad:            [________________]          │
│ Escuela Profesional: [________________]          │
│                                                  │
│                    [ BUSCAR ]                    │
│                                                  │
├──────────────────────────────────────────────────┤
│ RESULTADOS                                       │
│                                                  │
│ Código: 20240001                                 │
│ Nombre: PEREZ QUISPE JUAN                        │
│ DNI: 12345678                                    │
│ Facultad: Ingeniería de Producción y Servicios   │
│ Escuela: Ingeniería de Sistemas                  │
└──────────────────────────────────────────────────┘
```

El frontend no tendrá acceso directo a la base de datos.

La comunicación será:

Solicitud HTTPConsultaDatosJSONUsuarioFrontendAPI FastAPI(MySQL)

---

# 10. Seguridad de la conexión

Las credenciales de MySQL no estarán almacenadas directamente en el código fuente.

Se utilizarán variables de entorno:

```env
DATABASE_URL=mysql+pymysql://usuario:password@host:3306/base_datos
```

El archivo `.env` deberá estar incluido en `.gitignore`:

```gitignore
.env
__pycache__/
*.pyc
.venv/
```

La aplicación deberá mantener la siguiente regla:

HTTPSCredenciales protegidasNO acceso directoFrontendFastAPI(MySQL)

El frontend nunca deberá conectarse directamente a MySQL.

---

# 11. Arquitectura de despliegue

Para la versión de prueba se plantea utilizar un servicio de hosting para el frontend/backend y un proveedor externo para MySQL.

```mermaid
flowchart TB
    USER[Usuario]

    subgraph RENDER["Host de aplicación"]
        FRONT[Frontend]
        API[FastAPI]
    end

    subgraph MYSQL["Host externo"]
        DB[(MySQL)]
    end

    USER -->|HTTPS| FRONT
    FRONT -->|REST API / HTTPS| API
    API -->|MySQL| DB
```

La separación física será:

```text
Host 1
└── Frontend
└── FastAPI

Host 2
└── MySQL
```

Aunque la base de datos se encuentre en otro host, el usuario solamente interactuará con el frontend y la API.

---

# 12. Flujo completo de una consulta

Ejemplo: un usuario desea consultar al estudiante con DNI `12345678`.

```mermaid
sequenceDiagram
    actor Usuario
    participant Web as Frontend
    participant API as FastAPI
    participant MySQL

    Usuario->>Web: Ingresa DNI
    Usuario->>Web: Presiona BUSCAR

    Web->>API: GET /api/estudiantes/dni/12345678

    API->>MySQL: SELECT estudiante WHERE DNI = 12345678

    MySQL-->>API: Datos del estudiante

    API-->>Web: JSON

    Web-->>Usuario: Muestra información
```

Respuesta:

```json
{
    "codigo": "20240001",
    "apellidos_nombres": "PEREZ QUISPE JUAN",
    "dni": "12345678",
    "facultad": "INGENIERIA DE PRODUCCION Y SERVICIOS",
    "escuela_profesional": "INGENIERIA DE SISTEMAS"
}
```

---

# 13. Tecnologías

```mermaid
mindmap
    root((Sistema de Consulta))
        Frontend
            HTML
            CSS
            JavaScript
            Framework opcional
        Backend
            Python
            FastAPI
            Pydantic
            SQLAlchemy
        Base de datos
            MySQL
            PyMySQL
        Despliegue
            Render
            Host MySQL
        Comunicación
            REST
            HTTP
            HTTPS
            JSON
```

---

# 14. Dependencias del backend

El archivo `requirements.txt` contendrá inicialmente:

```text
fastapi
uvicorn[standard]
sqlalchemy
pymysql
python-dotenv
pydantic
```

---

# 15. Objetivo de la primera versión

La primera versión del sistema tendrá como objetivo proporcionar una **API funcional de consulta de estudiantes**, conectada a MySQL y consumida desde una interfaz web.

El alcance inicial comprende:

- Conexión segura con MySQL.
    
- Consulta de estudiantes.
    
- Búsqueda por código.
    
- Búsqueda por DNI.
    
- Búsqueda por apellidos y nombres.
    
- Filtro por facultad.
    
- Filtro por escuela profesional.
    
- Combinación de filtros.
    
- Respuestas JSON.
    
- Manejo de errores.
    
- Documentación automática mediante Swagger/OpenAPI.
    
- Interfaz web para realizar consultas.
    
- Despliegue de prueba mediante servicios gratuitos.
    

La arquitectura estará preparada para incorporar posteriormente nuevas funcionalidades sin tener que modificar completamente la estructura del proyecto.

---

# 16. Arquitectura final propuesta

```mermaid
flowchart TB

    U[Usuario]

    subgraph HOST1["Host de aplicación"]
        FE[Frontend]
        API[FastAPI REST]

        FE --> API
    end

    subgraph HOST2["Host de base de datos"]
        DB[(MySQL)]
    end

    U -->|HTTPS| FE
    API -->|SQL / MySQL| DB

    API --> S[SQLAlchemy]
    S --> DB
```

En resumen:

```text
                    USUARIO
                       │
                       │ HTTPS
                       ▼
              ┌─────────────────┐
              │    FRONTEND     │
              │    Aplicación   │
              │      Web        │
              └────────┬────────┘
                       │
                       │ REST / JSON
                       ▼
              ┌─────────────────┐
              │     FASTAPI     │
              │     Python      │
              │      API        │
              └────────┬────────┘
                       │
                       │ SQLAlchemy
                       ▼
              ┌─────────────────┐
              │      MYSQL      │
              │                 │
              │  ESTUDIANTES    │
              │                 │
              │ • CODIGO        │
              │ • NOMBRES       │
              │ • DNI           │
              │ • FACULTAD      │
              │ • ESCUELA       │
              └─────────────────┘
```