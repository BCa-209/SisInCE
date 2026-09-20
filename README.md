# Sistema de Consulta Estudiantil (SisInCE)

Aplicación web modular orientada a la búsqueda, visualización y exportación (a PDF) de datos de estudiantes de una institución académica (como la U.N.S.A.). 

El sistema está dividido en dos partes: una **API REST (Backend)** construida con Python y un cliente ligero **Frontend** (HTML/JS Vanilla) diseñado para ser rápido, responsivo y fácil de usar.

---

## 🚀 Características Principales

* **Búsqueda Avanzada**: Permite realizar búsquedas rápidas por Código o DNI, y búsquedas personalizadas cruzando múltiples criterios (Apellidos, Nombres, Facultad, Escuela Profesional, Año de Ingreso, Ciclo y Género).
* **Plantilla Editable y Exportación PDF**: Genera automáticamente una vista previa (carnet/ficha) prellenada. El usuario puede modificar los campos haciendo clic antes de exportarlo a formato PDF usando `html2pdf.js`.
* **Modo Oscuro (Dark Mode)**: Interfaz que se adapta automáticamente mediante el guardado de preferencias en memoria local.
* **Caché Inteligente de Catálogos**: El frontend extrae las facultades y escuelas de la base de datos la primera vez que se carga la página y las almacena en memoria (`localStorage`) para evitar peticiones repetitivas al servidor y optimizar el rendimiento.
* **Modularidad ES6**: El código del cliente está completamente modularizado (sin empaquetadores como Webpack) facilitando su mantenimiento y escalabilidad.

---

## 🛠️ Tecnologías Usadas

### Backend
* **FastAPI** (Python): Framework veloz y moderno para la construcción de la API.
* **SQLAlchemy**: ORM para gestionar de manera segura las interacciones con la base de datos y evitar inyecciones SQL.
* **Pydantic**: Para la validación de esquemas de datos.
* **Uvicorn**: Servidor ASGI para correr FastAPI.

### Frontend
* **HTML5 & CSS3 Vanilla**: Sistema de diseño en cuadrículas (CSS Grid) completamente responsivo para adaptarse a dispositivos móviles.
* **JavaScript ES6 (Módulos)**: Organización de código por módulos (`main.js`, `api.js`, `ui.js`, `theme.js`, etc).
* **html2pdf.js**: Librería externa para la conversión de la plantilla HTML a un documento PDF descargable.

---

## ⚙️ Estructura del Proyecto

```
SisInCE/
│
├── backend/                  # Código fuente del Backend (API)
│   ├── app/
│   │   ├── routers/          # Endpoints de la API
│   │   ├── database.py       # Configuración y conexión de BD
│   │   ├── main.py           # Archivo de arranque de FastAPI (Config. CORS)
│   │   ├── models.py         # Modelos de tablas (SQLAlchemy)
│   │   └── schemas.py        # Esquemas de validación (Pydantic)
│   └── requirements.txt      # Dependencias de Python
│
└── frontend/                 # Interfaz de Usuario
    ├── js/                   # Módulos JavaScript (Control, API, UI)
    ├── index.html            # Estructura principal
    ├── style.css             # Estilos y variables (Modo Claro/Oscuro)
    └── vercel.json           # Configuración de enrutamiento para despliegue en Vercel
```

---

## 🔧 Instalación y Ejecución Local

### 1. Levantar el Backend
Necesitarás **Python 3.8+** instalado.

```bash
# 1. Navegar a la carpeta del backend
cd backend

# 2. Crear un entorno virtual e instalar dependencias
python -m venv .venv
# En Windows:
.venv\Scripts\activate
# En Linux/Mac:
source .venv/bin/activate
pip install -r requirements.txt

# 3. Arrancar el servidor local
uvicorn app.main:app --reload
```
*La API estará disponible en `http://localhost:8000`*

### 2. Levantar el Frontend
Debes servir los archivos usando un servidor web local (necesario por el uso de módulos ES6). Puedes usar Python para levantarlo rápidamente:

```bash
# 1. Abre otra terminal y ve a la carpeta del frontend
cd frontend

# 2. Inicia el servidor
python -m http.server 8080
```
*Visita `http://localhost:8080` en tu navegador para ver la aplicación.*

---

## 🔒 Consideraciones para Producción (Despliegue)
- **Base de Datos y Secretos**: Al desplegar el backend, recuerda crear un archivo `.env` que contenga tu cadena de conexión (`DATABASE_URL`). Este repositorio ignora intencionalmente los archivos `.env` y `.db` por seguridad.
- **Frontend URL**: Si subes el backend a la nube (ej. Render o Railway), actualiza la variable `FRONTEND_URL` en las variables de entorno para configurar adecuadamente el CORS, y cambia la constante `API_URL` en `frontend/js/config.js` para que apunte al nuevo servidor remoto.
