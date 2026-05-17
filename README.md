# 🚀 Portafolio API Backend Service

Este repositorio contiene el *backend* de la API para gestionar todos los datos del portafolio profesional. Está diseñado bajo una arquitectura moderna y escalable utilizando **FastAPI** en Python, con soporte asíncrono (`asyncio`), lo que garantiza un alto rendimiento al manejar múltiples peticiones simultáneamente.

## ⚙️ Visión General y Arquitectura

La API sigue el patrón de diseño RESTful, exponiendo *routers* específicos para cada entidad del portafolio (Proyectos, Experiencias, Estudios, etc.). Su objetivo principal es servir como una capa de negocio robusta que valida, almacena y recupera la información del usuario antes de enviarla al cliente frontend.

**Tecnologías Clave:**
*   **Framework:** FastAPI (Python)
*   **Base de Datos:** PostgreSQL (mediante SQLAlchemy ORM asíncrono).
*   **Cache/Sesiones:** Redis (para gestión de tokens y rate limiting).
*   **Seguridad:** JWT (JSON Web Tokens) para autenticación, y `bcrypt` para el *hashing* seguro de contraseñas.
*   **IA Integración:** Soporte para servicios avanzados como la API de Google Gemini (`google-genai`).

## 🛠️ Configuración e Instalación

### 1. Requisitos Previos
Asegúrate de tener instalado Python 3.8+ y Docker/Docker Compose, ya que el servicio depende de PostgreSQL y Redis.

### 2. Dependencias
Instala las librerías necesarias utilizando los requisitos definidos:

```bash
pip install -r requirements.txt
```

### 3. Inicialización del Proyecto (Migrations)
El sistema utiliza **Alembic** para gestionar la evolución del esquema de la base de datos, asegurando que el modelo de código coincida con la estructura real de PostgreSQL.

1.  **Crear las Migraciones:** Genera los scripts necesarios para actualizar el esquema:
    ```bash
    alembic revision --autogenerate -m "Descripción de la nueva funcionalidad"
    ```
2.  **Aplicar Migraciones:** Ejecuta las migraciones para aplicar los cambios a la base de datos:
    ```bash
    alembic upgrade head
    ```

## 📂 Estructura Modular del Código

El *backend* está organizado en módulos funcionales que desacoplan la lógica de negocio, haciendo el sistema fácil de mantener y escalar.

| Directorio | Propósito | Componentes Clave |
| :--- | :--- | :--- |
| `app/` | **Raíz Lógica:** Contiene todos los componentes principales del API. | `main.py`, `database.py`, etc. |
| `app/models/` | **Definición de Esquemas:** Define las estructuras de datos persistentes (Modelos SQLAlchemy). | `usuario.py`, `proyecto.py`, `experiencia.py`. |
| `app/schemas/` | **Validación de Datos:** Utiliza Pydantic para definir el formato y la validación de los datos entrantes y salientes del API. | `auth.py`, `perfil.py`, etc. |
| `app/services/` | **Lógica de Negocio (Core):** Contiene las funciones que orquestan interacciones complejas, como el manejo de archivos o la sincronización de datos JSON. | `crud.py` (Operaciones CRUD genéricas), `auth.py`. |
| `app/api/v1/` | **Endpoints API:** Cada archivo aquí define un *router* específico y expone los puntos finales HTTP (`@router.get`, `@router.post`). | `proyectos.py`, `estudios.py`, etc. |
| `alembic/` | **Migrations:** Scripts de Alembic para el control de versiones del esquema de la base de datos. | `0001_create_all_tables.py`. |

## 🌐 Endpoints API Detallados (`/api/v1`)

Todos los *routers* están agrupados bajo el prefijo `/api/v1` y requieren autenticación (JWT) para la mayoría de las operaciones de escritura (POST, PUT).

### 🛡️ `auth.router`
Gestiona la identidad del usuario y el acceso al sistema.
*   **Funcionalidad:** Registro de usuarios, login, generación y validación de tokens JWT.
*   **Roles:** Maneja la semilla inicial (`seed_admin_user`) para crear un administrador por defecto.

### 💼 `proyectos.router`
Gestión del portafolio de proyectos.
*   **CRUD:** Crear, leer, actualizar y eliminar proyectos.
*   **Modelo:** Incluye campos como título, descripción detallada, tecnologías usadas, enlaces (GitHub/Demo) y una imagen asociada (`images.py`).

### 🗓️ `experiencias.router`
Gestión de la experiencia laboral.
*   **CRUD:** Permite añadir o modificar roles laborales.
*   **Modelo:** Almacena detalles como empresa, cargo, fechas de inicio/fin y responsabilidades clave.

### 🎓 `estudios.router`
Gestión académica.
*   **CRUD:** Registro de instituciones educativas, títulos obtenidos y periodos de estudio.

### 👤 `perfil.router`
Datos biográficos generales del usuario.
*   **Modelo:** Contiene información general como el nombre completo, la foto de perfil (avatar) y una sección de descripción personal (*About Me*).

### 🖼️ `images.router`
Manejo de recursos multimedia.
*   **Funcionalidad:** Endpoint dedicado para subir imágenes. Es crucial porque enlaza las rutas o IDs de las imágenes con los modelos de datos principales (Proyectos, Perfil, etc.).

### 💬 `chat.router`
Integración avanzada de IA.
*   **Funcionalidad:** Permite interactuar con un modelo de lenguaje grande (LLM), probablemente para generar descripciones o contenido basado en el contexto del portafolio. **Depende de la configuración de Google GenAI.**

## 🚀 Flujo Operacional (`main.py`)

El archivo `app/main.py` es el punto de entrada y define el ciclo de vida (lifespan) de la aplicación:

1.  **Inicialización (Lifespan):** Al arrancar, se ejecuta `init_db()` para asegurar que la conexión a PostgreSQL está activa.
2.  **Seed Data:** Se llama a `seed_admin_user(session)` para garantizar que siempre haya un usuario administrador configurado con credenciales iniciales.
3.  **Middleware CORS:** Configura los permisos de origen (`allow_origins=["*"]`) y métodos HTTP, lo cual es vital para la comunicación entre el frontend (que puede correr en otro puerto/dominio) y el backend.

---
*(Este README fue generado automáticamente basándose en la estructura del código fuente.)*