# OppyTalent Backend — API de Portafolios Profesionales con IA

Backend asíncrono para la plataforma **OppyTalent**, un ecosistema de portafolios profesionales potenciados por inteligencia artificial. Permite a talentos mostrar su trayectoria, a reclutadores buscar perfiles mediante búsqueda semántica vectorial, y facilita la conexión directa entre ambos mediante una red profesional integrada con chat en tiempo real.

---

## Índice

1. [Visión del Producto](#-visión-del-producto)
2. [Stack Tecnológico](#-stack-tecnológico)
3. [Arquitectura General](#-arquitectura-general)
4. [Instalación y Configuración](#-instalación-y-configuración)
   - [Requisitos](#requisitos)
   - [Entorno Local](#entorno-local)
   - [Docker](#docker)
   - [Migraciones](#migraciones)
5. [Estructura del Proyecto](#-estructura-del-proyecto)
6. [Modelos de Datos (Base de Datos)](#-modelos-de-datos-base-de-datos)
   - [Core — Usuario](#core--usuario)
   - [Portafolio](#portafolio)
   - [RBAC (Roles y Permisos)](#rbac-roles-y-permisos)
   - [Red Profesional (Networking)](#red-profesional-networking)
   - [Mensajería Peer-to-Peer](#mensajería-peer-to-peer)
   - [B2B / Tribunal de Talentos](#b2b--tribunal-de-talentos)
   - [IA y Embeddings Vectoriales](#ia-y-embeddings-vectoriales)
   - [Autenticación y Sesiones](#autenticación-y-sesiones)
7. [Endpoints API](#-endpoints-api)
   - [Autenticación](#1-autenticación-api-v1-auth)
   - [Registro de Cuenta](#2-registro-de-cuenta)
   - [Usuario / Perfil](#3-usuario--perfil-v1-user)
   - [Portafolio — CRUDs](#4-portafolio-cruds)
   - [Imágenes](#5-imágenes)
   - [Chat IA del Portafolio](#6-chat-ia-del-portafolio)
   - [AI Management](#7-ai-management)
   - [Red Profesional (Networking)](#8-red-profesional-networking)
   - [Chat Peer-to-Peer](#9-chat-peer-to-peer)
   - [B2B / Meta-Reclutador](#10-b2b-meta-reclutador)
   - [Administración RBAC](#11-administración-rbac)
   - [Open Graph Cards](#12-open-graph-cards)
   - [Storage Vinculado](#13-storage-vinculado)
   - [Utilidades](#14-utilidades)
8. [Flujo de Autenticación](#-flujo-de-autenticación)
9. [Sistema de Roles y Permisos (RBAC)](#-sistema-de-roles-y-permisos-rbac)
10. [Motor de IA y RAG Vectorial](#-motor-de-ia-y-rag-vectorial)
11. [Ecosistema B2B](#-ecosistema-b2b)
    - [Meta-Reclutador (Búsqueda Semántica)](#meta-reclutador-búsqueda-semántica)
    - [Tribunal de Talentos](#tribunal-de-talentos)
    - [Insights de Demanda](#insights-de-demanda)
12. [Almacenamiento de Archivos](#-almacenamiento-de-archivos)
    - [Cloudflare R2 (Premium)](#cloudflare-r2-premium)
    - [Google Drive (Free Tier)](#google-drive-free-tier)
13. [Notificaciones y Email](#-notificaciones-y-email)
14. [Cache y Rate Limiting](#-cache-y-rate-limiting)
15. [WebSockets — Conexiones en Tiempo Real](#-websockets--conexiones-en-tiempo-real)
16. [Seguridad](#-seguridad)
17. [Despliegue](#-despliegue)
18. [Flujo de CI / Seed Data](#-flujo-de-ci--seed-data)
19. [Configuración de Entorno (.env)](#-configuración-de-entorno-env)

---

## 📋 Visión del Producto

OppyTalent es una plataforma que transforma el currículum tradicional en un **portafolio digital interactivo con un asistente de IA** que lo conoce todo sobre el talento. Cada usuario obtiene:

- Un portafolio profesional vivo (proyectos, experiencia, estudios, reconocimientos, habilitaciones).
- Un **chat con IA** que responde preguntas de reclutadores como si fuera el propio talento.
- **Búsqueda semántica vectorial** para que reclutadores encuentren talento por afinidad conceptual.
- **Tribunal B2B**: un reclutador lanza una pregunta técnica y los clones de IA de varios candidatos compiten respondiendo, con un moderador neutral que los evalúa.
- **Red profesional** con gestión de conexiones, feed de actividad, sugerencias IA y chat peer-to-peer en tiempo real.
- **Personalización**: temas visuales (dark-glass, etc.), layouts, slugs personalizados, y reglas de `pitch` para la IA.

---

## 🛠️ Stack Tecnológico

| Componente               | Tecnología                                                              |
| ------------------------ | ----------------------------------------------------------------------- |
| **Framework Web**        | FastAPI (Python 3.12+)                                                  |
| **Runtime**              | Uvicorn (ASGI)                                                          |
| **Base de Datos**        | PostgreSQL 16 con extensiones `pgvector` (embeddings) y `uuid-ossp`      |
| **ORM**                  | SQLAlchemy 2.0 (asíncrono)                                              |
| **Migraciones**          | Alembic                                                                 |
| **Cache / Sesiones**     | Redis 7                                                                 |
| **IA / LLM**             | Google Gemini (`google-genai`) — modelos `gemini-2.5-flash` y `gemini-2.5-flash-lite` |
| **Embeddings**           | `gemini-embedding-2` (768 dimensiones)                                  |
| **Autenticación**        | JWT (access + refresh tokens), OAuth2 Google                            |
| **Hashing de Password**  | Argon2 (`argon2-cffi`)                                                  |
| **Almacenamiento**       | Cloudflare R2 (S3-compatible) + Google Drive API (free tier)            |
| **WebSockets**           | FastAPI WebSockets                                                      |
| **Document Intake**      | MarkItDown (convierte PDFs, DOCX, imágenes a markdown)                  |
| **Traducción**           | Gemini (traducción automática de contenido JSON del portafolio)         |
| **Email**                | Resend API / SMTP (via FastMail)                                        |
| **Contenedores**         | Docker + Docker Compose                                                 |

---

## 🏗️ Arquitectura General

```
┌──────────────┐     ┌──────────────────────────────────────────────┐
│   Frontend   │     │            OppyTalent Backend API            │
│ (React/Vite) │◄───►│           FastAPI + Uvicorn (ASGI)           │
└──────────────┘     │                                              │
                     │  ┌─────────┐ ┌──────────┐ ┌──────────────┐  │
                     │  │  Routers│ │ Services │ │  AI Engine   │  │
                     │  │ (API/v1)│ │(Negocio) │ │ (Gemini RAG) │  │
                     │  └────┬────┘ └────┬─────┘ └──────┬───────┘  │
                     │       │           │               │          │
                     │  ┌────▼───────────▼───────────────▼────┐     │
                     │  │         SQLAlchemy Async ORM        │     │
                     │  └────────────────┬────────────────────┘     │
                     └───────────────────┼──────────────────────────┘
                                         │
              ┌──────────────────────────┼──────────────────────────┐
              │                          │                          │
         ┌────▼────┐              ┌──────▼──────┐           ┌───────▼───────┐
         │PostgreSQL│              │    Redis    │           │ Cloudflare R2 │
         │(pgvector)│              │ (Cache/QS)  │           │  (Imágenes)   │
         └─────────┘              └─────────────┘           └───────────────┘
```

### Principios de Diseño

- **Arquitectura RESTful** modular con routers por dominio.
- **Async-first**: toda la pila es asíncrona (`async/await`), desde FastAPI hasta SQLAlchemy y Redis.
- **Separación de capas**: Routers → Servicios (lógica de negocio) → Modelos (ORM).
- **Multi-tenancy vía esquemas PostgreSQL** (opcional, configurable con `DB_SCHEMA`), actualmente en modo single-tenant.
- **Seed automático** en cada inicio: roles RBAC, modelos de IA y usuario administrador.

---

## 🔧 Instalación y Configuración

### Requisitos

- Python 3.12+
- Docker & Docker Compose
- PostgreSQL 16 con `pgvector`
- Redis 7
- API Key de Google Gemini

### Entorno Local

```bash
# 1. Clonar el repositorio
git clone <repo-url> oppytalent-backend
cd oppytalent-backend

# 2. Crear entorno virtual
python -m venv .venv
source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Iniciar servicios (PostgreSQL + Redis)
docker compose up -d postgres redis

# 5. Configurar variables de entorno (copiar .env)

# 6. Ejecutar migraciones
alembic upgrade head

# 7. Iniciar servidor de desarrollo
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Docker

```bash
# Construir y levantar todos los servicios
docker compose up --build

# Servicios:
#   - PostgreSQL en puerto 5443 (mapeado desde 5432)
#   - Redis en puerto 6379
#   - Backend API en puerto 8000
```

### Migraciones (Alembic)

```bash
# Crear una nueva migración
alembic revision --autogenerate -m "descripción del cambio"

# Aplicar migraciones
alembic upgrade head

# Revertir última migración
alembic downgrade -1
```

---

## 📁 Estructura del Proyecto

```
OppyTalent-backend/
├── app/                          # ★ Código principal de la aplicación
│   ├── __init__.py
│   ├── main.py                   # Punto de entrada, lifespan, middlewares y registro de routers
│   ├── config.py                 # Configuración centralizada (Settings via Pydantic)
│   ├── database.py               # Engine asíncrono, sesión, base declarativa, helpers
│   ├── dependencies.py           # Dependencias globales: get_current_user, RequirePermission
│   ├── utils.py                  # Hash/verify password (Argon2), helpers generales
│   │
│   ├── models/                   # ★ Modelos SQLAlchemy (ORM)
│   │   ├── usuario.py            # Usuario (entidad raíz del sistema)
│   │   ├── perfil.py             # Perfil profesional (datos biográficos + traducciones)
│   │   ├── proyecto.py           # Proyectos del portafolio + traducciones
│   │   ├── experiencia.py        # Experiencia laboral + traducciones
│   │   ├── estudio.py            # Estudios/títulos + traducciones
│   │   ├── reconocimiento.py     # Reconocimientos/premios/publicaciones + traducciones
│   │   ├── habilitacion.py       # Habilitaciones/licencias + traducciones
│   │   ├── frase.py              # Frases célebres del talento + traducciones
│   │   ├── seccion_config.py     # Configuración de secciones expandidas/colapsadas
│   │   ├── rbac.py               # Roles, Permisos y asociación Role-Permission
│   │   ├── networking.py         # Red profesional (conexiones, follows, feed, sugerencias)
│   │   ├── conversation.py       # Conversaciones y mensajes peer-to-peer
│   │   ├── chat_log.py           # Logs del chat IA del portafolio
│   │   ├── portfolio_document.py # Documentos vectoriales para RAG (pgvector)
│   │   ├── b2b_tribunal.py       # Logs del tribunal B2B (preguntas, respuestas, feedback)
│   │   └── __init__.py
│   │
│   ├── schemas/                  # ★ Schemas Pydantic (validación request/response)
│   │   ├── auth.py               # Auth schemas
│   │   ├── perfil.py             # Perfil schemas
│   │   ├── proyecto.py           # Proyecto schemas
│   │   ├── experiencia.py        # Experiencia schemas
│   │   ├── estudio.py            # Estudio schemas
│   │   ├── reconocimiento.py     # Reconocimiento schemas
│   │   ├── habilitacion.py       # Habilitación schemas
│   │   ├── frase.py              # Frase schemas
│   │   ├── seccion_config.py     # SeccionConfig schemas
│   │   ├── chat_p2p.py           # Chat P2P schemas
│   │   └── __init__.py
│   │
│   ├── api/v1/                   # ★ Endpoints REST (routers)
│   │   ├── auth.py               # Login, refresh, logout, forgot/reset password, impersonate
│   │   ├── proyectos.py          # CRUD proyectos
│   │   ├── experiencias.py       # CRUD experiencias
│   │   ├── estudios.py           # CRUD estudios
│   │   ├── perfil.py             # CRUD perfil
│   │   ├── reconocimientos.py    # CRUD reconocimientos
│   │   ├── habilitaciones.py     # CRUD habilitaciones
│   │   ├── frases.py             # CRUD frases
│   │   ├── seccion_config.py     # CRUD configuración de secciones
│   │   ├── images.py             # Subida a R2 + proxy de imágenes
│   │   ├── chat.py               # Chat IA del portafolio (RAG + Gemini)
│   │   ├── ai.py                 # Traducción y extracción de CVs
│   │   ├── chat_p2p.py           # Mensajería peer-to-peer + WebSockets
│   │   ├── network.py            # Red profesional (conexiones, feed, sugerencias)
│   │   ├── b2b.py                # Búsqueda semántica, tribunal, insights
│   │   ├── admin_rbac.py         # Gestión de roles y permisos
│   │   ├── storage_auth.py       # OAuth Google Drive
│   │   ├── og.py                 # Open Graph cards
│   │   └── __init__.py
│   │
│   ├── services/                 # ★ Lógica de negocio
│   │   ├── auth.py               # Creación de tokens JWT, autenticación, seed admin
│   │   ├── crud.py               # CRUD genérico (get_all, get_by_id, create, update, soft_delete)
│   │   ├── image.py              # Parseo y proxy de URLs de imágenes (Google Drive)
│   │   ├── cloud_storage.py      # Upload a Cloudflare R2 (S3-compatible)
│   │   ├── cache.py              # Cache Redis + limpieza de contexto IA
│   │   ├── rate_limit.py         # Rate limiting por IP + moderation strikes
│   │   ├── crypto.py             # Encriptación Fernet (API keys)
│   │   ├── websocket_manager.py  # Gestor de conexiones WebSocket
│   │   └── __init__.py
│   │
│   ├── authentication/           # ★ Módulo de autenticación completo
│   │   ├── router.py             # Login, refresh, logout, reset password, impersonate
│   │   ├── services.py           # Lógica de autenticación, sesiones, refresh tokens
│   │   ├── models.py             # SessionHistory, PasswordResetToken, RefreshToken, EmailConfirmation
│   │   ├── schemas.py            # Schemas de autenticación
│   │   ├── utils.py              # Creación de JWT access/refresh tokens
│   │   ├── dependencies.py       # Dependencias de autenticación
│   │   ├── google_oauth_router.py    # OAuth2 con Google (web + mobile)
│   │   ├── user_details_router.py    # Perfil de usuario, configuraciones, KYC, RAG sync
│   │   └── __init__.py
│   │
│   ├── ai_management/            # ★ Motor de IA
│   │   ├── client.py             # Cliente Gemini (llamadas a API con costo dinámico)
│   │   ├── config.py             # Configuración de modelos y precios
│   │   ├── models.py             # LLMRequestLog + AIModelConfig (modelos dinámicos)
│   │   ├── schemas.py            # Schemas de respuesta IA
│   │   ├── services.py           # Orquestador ask_oppy_ai (retry, fallback, billing)
│   │   ├── embeddings.py         # Generación de embeddings (gemini-embedding-2)
│   │   ├── rag_sync.py           # Sincronización RAG (modelos → vectores pgvector)
│   │   └── __init__.py
│   │
│   ├── registration/             # ★ Registro de nuevos usuarios
│   │   ├── router.py             # Endpoints de registro + confirmación de email
│   │   ├── services.py           # Lógica de registro + subida de imagen + email
│   │   └── schemas.py            # Schemas de registro
│   │
│   ├── email/                    # ★ Servicio de correo electrónico
│   │   ├── email_service.py      # Envío via Resend API o SMTP (fallback)
│   │   └── __init__.py
│   │
│   ├── scripts/                  # ★ Scripts de seed
│   │   ├── seed_rbac.py          # Siembra de roles y permisos por defecto
│   │   ├── seed_ai.py            # Siembra de modelos de IA por defecto
│   │   └── drop_table.py         # Utilidad para eliminar tablas
│   │
│   ├── templates/emails/         # Plantillas HTML para correos
│   │   ├── email_confirmation.html
│   │   ├── password_reset.html
│   │   └── reception_discrepancy.html
│   │
│   └── json_data/                # Datos semilla JSON
│       ├── usuarios.json
│       ├── perfil.json
│       ├── proyectos.json
│       ├── experiencias.json
│       └── estudios.json
│
├── alembic/                      # Migraciones de base de datos
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       ├── 34a182dc639a_initial_schema_uuid.py
│       ├── 3ec8713b4237_add_custom_slug_to_usuario.py
│       ├── 476a93be8bae_add_galeria_to_proyecto.py
│       ├── 9f66806f3b58_add_conversation_and_message_models.py
│       ├── de6b12d15891_add_networksuggestion_model.py
│       └── df6b305250d7_add_networking_models.py
│
├── Dockerfile                    # Imagen Docker para producción
├── docker-compose.yml            # Orquestación local (PostgreSQL + Redis + API)
├── requirements.txt              # Dependencias Python
├── alembic.ini                   # Configuración de Alembic
├── seed_ai.py                    # Seed independiente de modelos IA
└── patch_routers.py              # Utilidad de parche
```

---

## 🗄️ Modelos de Datos (Base de Datos)

### Core — Usuario

**`usuarios`** — Entidad raíz del sistema. Alberga desde credenciales hasta configuración de IA, B2B y premium.

| Campo                    | Tipo                          | Descripción                                              |
| ------------------------ | ----------------------------- | -------------------------------------------------------- |
| `id`                     | UUID (PK)                     | Identificador único                                      |
| `username`               | String(100), UNIQUE, NOT NULL | Nombre de usuario (usado como email en muchos casos)     |
| `email`                  | String(255), UNIQUE, NOT NULL | Correo electrónico                                       |
| `hashed_password`        | Text, NOT NULL                | Hash Argon2 de la contraseña                             |
| `role`                   | String(20)                    | Rol legacy (ADMIN, VIEWER, SUPERADMIN)                   |
| `role_id`                | UUID (FK → roles.id)          | Rol RBAC actual                                          |
| `first_name` / `last_name` | String(100)                 | Nombre y apellido                                        |
| `user_image`             | String(1048)                  | URL de imagen de perfil                                  |
| `custom_slug`            | String(100), UNIQUE           | Slug personalizado para URL del portafolio               |
| `is_deleted`             | Boolean                       | Soft delete                                              |
| `has_accepted_terms`     | Boolean                       | Términos y condiciones aceptados                         |
| `is_recruiter`           | Boolean                       | Es reclutador (B2B)                                      |
| `is_visible_b2b`         | Boolean                       | Visible en búsqueda B2B                                  |
| `chat_welcome_message`   | Text                          | Mensaje de bienvenida del chat IA                        |
| `ai_pitch_rules`         | JSON                          | Reglas de pitch para la IA (keywords + argumentos)       |
| `portfolio_theme`        | String(50)                    | Tema visual (default: `dark-glass`)                      |
| `portfolio_layout`       | String(20)                    | Layout (default: `tabs`)                                 |
| `is_premium`             | Boolean                       | Usuario premium                                          |
| `google_*_token`         | String(2048)                  | Tokens de Google Drive (storage free tier)               |
| `encrypted_gemini_key`   | String(2048)                  | API Key de Gemini encriptada                             |
| `ai_credits`             | Integer                       | Créditos de IA (default: 10)                             |
| `storage_used`           | Integer                       | Almacenamiento usado en bytes                            |
| `last_login`             | DateTime                      | Último inicio de sesión                                  |
| `failed_login_attempts`  | Integer                       | Intentos fallidos de login                               |
| `locked_until`           | DateTime                      | Bloqueo por intentos fallidos                            |

### Portafolio

Cada entidad del portafolio sigue el mismo patrón: modelo base con `usuario_id` (FK), `is_active`, `created_at`, `updated_at`, y modelos de traducción asociados (`*_traducciones`) con soporte multi-idioma (`idioma: String(5)`).

| Entidad           | Tabla                     | Campos clave                                              |
| ----------------- | ------------------------- | --------------------------------------------------------- |
| **Perfil**        | `perfiles`                | `nombre_completo`, `ocupacion`, `descripcion`, `image_url`, `avatar_url`, `telefono`, `email`, `linkedin`, `github`, `ciudad`, `youtube_url`, `certificaciones[]`, `idiomas[]`, `habilidades[]` |
| **Proyecto**      | `proyectos`               | `titulo`, `descripcion_corta`, `descripcion_detallada`, `stack_tecnologico[]`, `fecha_proyecto`, `link_github`, `link_demo`, `kpis{}`, `galeria[]`, `tags[]`, `image_url`, `youtube_url` |
| **Experiencia**   | `experiencias`            | `empresa`, `rol`, `periodo_inicio`, `periodo_fin`, `descripcion_logros`, `tags_industria[]`, `link`, `link_demo`, `image_url` |
| **Estudio**       | `estudios`                | `institucion`, `titulo`, `anio_obtencion`, `descripcion_detallada`, `link`, `image_url` |
| **Reconocimiento**| `reconocimientos`         | `tipo` (PREMIO/PUBLICACION/MEDIO), `titulo`, `institucion`, `fecha`, `descripcion`, `enlace`, `referencia`, `image_url` |
| **Habilitación**  | `habilitaciones`          | `tipo` (DISPONIBILIDAD/LICENCIA), `titulo`, `descripcion`, `image_url`, `enlace` |
| **Frase**         | `frases_celebres`         | `texto`, `autor`                                           |
| **SeccionConfig** | `seccion_configs`         | `seccion`, `is_expanded` (controla UI colapsable)          |

### RBAC (Roles y Permisos)

| Tabla                | Descripción                                      |
| -------------------- | ------------------------------------------------ |
| `roles`              | Roles del sistema (Owner, Admin, Hunter, Talent, Worker) |
| `permissions`        | Permisos atómicos (8 definidos: `can_execute_tribunal`, `can_use_b2b_search`, etc.) |
| `role_permissions`   | Asociación muchos-a-muchos entre roles y permisos |

### Red Profesional (Networking)

| Tabla                   | Descripción                                               |
| ----------------------- | --------------------------------------------------------- |
| `network_connections`   | Conexiones entre usuarios (PENDING, ACCEPTED, REJECTED, BLOCKED) + `affinity_score` |
| `network_follows`       | Seguimientos (follower → following)                       |
| `feed_events`           | Eventos de actividad (NEW_PROJECT, NEW_EXPERIENCE, etc.)  |
| `network_suggestions`   | Sugerencias de conexión generadas por IA                  |

### Mensajería Peer-to-Peer

| Tabla           | Descripción                                      |
| --------------- | ------------------------------------------------ |
| `conversations` | Canales entre dos participantes                   |
| `messages`      | Mensajes individuales con `is_read`, `sender_id`  |

### B2B / Tribunal de Talentos

| Tabla                        | Descripción                                                |
| ---------------------------- | ---------------------------------------------------------- |
| `b2b_tribunal_logs`          | Historial de tribunales: pregunta del recruiter + resumen del moderador |
| `b2b_tribunal_participants`  | Respuestas de cada candidato + `talent_feedback` generado por IA |

### IA y Embeddings Vectoriales

| Tabla                | Descripción                                                  |
| -------------------- | ------------------------------------------------------------ |
| `portfolio_documents`| Fragmentos del portafolio convertidos a vectores (768 dims via `pgvector`) + índice HNSW |
| `llm_request_log`    | Registro de todas las llamadas a la API de Gemini (tokens, costo, duración, éxito/fallo) |
| `ai_model_configs`   | Configuración dinámica de modelos de IA (nombre, precios por millón de tokens, activo/default) |

### Autenticación y Sesiones

| Tabla                      | Descripción                                  |
| -------------------------- | -------------------------------------------- |
| `user_session_history`     | Historial de sesiones (login/logout, IP, UA) |
| `password_reset_tokens`    | Tokens de restablecimiento de contraseña     |
| `refresh_tokens`           | Refresh tokens JWT con revocación            |
| `email_confirmation_tokens`| Tokens de confirmación de email para registro|

---

## 🌐 Endpoints API

Todos los endpoints están bajo `/api/v1` a menos que se indique lo contrario.

### 1. Autenticación (`/api/v1/auth`)

| Método | Ruta                    | Auth        | Descripción                                       |
| ------ | ----------------------- | ----------- | ------------------------------------------------- |
| POST   | `/login`                | Público     | Login con username/email + password (JWT en cookies y body) |
| POST   | `/refresh`              | Cookie      | Refresca el access token usando refresh token      |
| POST   | `/logout`               | Cookie      | Revoca refresh token y limpia cookies             |
| POST   | `/forgot-password`      | Público     | Envía email con token de reseteo                  |
| POST   | `/reset-password`       | Público     | Resetea contraseña con token                      |
| POST   | `/impersonate`          | Owner       | Genera tokens suplantando un rol (para testing/QA)|
| POST   | `/restore`              | Auth        | Restaura tokens al rol real del usuario           |

### 2. Registro de Cuenta (`/api/v1/auth`)

| Método | Ruta                 | Auth    | Descripción                                        |
| ------ | -------------------- | ------- | -------------------------------------------------- |
| POST   | `/register`          | Público | Registro con email, password, imagen + confirmación por email |
| GET    | `/confirm-email/{token}` | Público | Confirma email y crea usuario (redirige al frontend) |

### 3. Usuario / Perfil (`/api/v1/user`)

| Método | Ruta                        | Auth | Descripción                                          |
| ------ | --------------------------- | ---- | ---------------------------------------------------- |
| GET    | `/profile`                  | Auth | Perfil completo del usuario autenticado (incluye permisos RBAC) |
| GET    | `/search?q=`                | Auth | Búsqueda de usuarios por nombre                      |
| GET    | `/{username}`               | Público | Datos públicos de un usuario por username/slug   |
| PUT    | `/chat-config`              | Auth | Actualiza mensaje de bienvenida y reglas de pitch    |
| PUT    | `/theme-config`             | Auth | Actualiza tema visual y layout del portafolio        |
| PUT    | `/b2b-config`               | Auth | Activa/desactiva visibilidad en B2B                  |
| POST   | `/select-role`              | Auth | Selecciona rol inicial (Hunter/Talent)               |
| PUT    | `/gemini-key`               | Auth | Guarda API Key de Gemini (encriptada)                |
| PUT    | `/slug`                     | Auth | Actualiza slug personalizado del portafolio          |
| POST   | `/sync-rag`                 | Auth | Dispara sincronización manual de vectores RAG        |
| PUT    | `/kyc/verify-recruiter/{id}`| Admin | Aprueba/revoca verificación KYC de reclutador       |

### 4. Portafolio — CRUDs

Cada entidad tiene un router estándar con operaciones CRUD. Todos requieren autenticación para escritura.

| Entidad          | Router                     | Endpoints                         |
| ---------------- | -------------------------- | --------------------------------- |
| Perfil           | `/api/v1/perfil`           | GET, POST, PUT, DELETE             |
| Proyectos        | `/api/v1/proyectos`        | GET, POST, PUT, DELETE            |
| Experiencias     | `/api/v1/experiencias`     | GET, POST, PUT, DELETE            |
| Estudios         | `/api/v1/estudios`         | GET, POST, PUT, DELETE            |
| Reconocimientos  | `/api/v1/reconocimientos`  | GET, POST, PUT, DELETE            |
| Habilitaciones   | `/api/v1/habilitaciones`   | GET, POST, PUT, DELETE            |
| Frases           | `/api/v1/frases`           | GET, POST, PUT, DELETE            |
| SeccionConfig    | `/api/v1/seccion_config`   | GET, POST, PUT, DELETE            |

Cada endpoint soporta:
- `?skip=N&limit=N` para paginación.
- Filtros por campos del modelo.
- Traducciones multi-idioma incluidas en el mismo payload.

### 5. Imágenes (`/api/v1/images`)

| Método | Ruta      | Auth | Descripción                                         |
| ------ | --------- | ---- | --------------------------------------------------- |
| POST   | `/upload` | Auth | Sube imagen a Cloudflare R2 (con control de cuota: 25MB free, ilimitado premium) |
| GET    | `/proxy`  | Público | Proxy para imágenes de Google Drive (evita CORS y problemas de autenticación) |

### 6. Chat IA del Portafolio (`/api/v1/chat`)

| Método | Ruta           | Auth     | Descripción                                             |
| ------ | -------------- | -------- | ------------------------------------------------------- |
| POST   | `/`            | Público  | Envía mensaje al asistente IA del portafolio (RAG + Gemini) |
| PATCH  | `/{log_id}/click` | Público | Registra click en link del chat                       |
| GET    | `/logs`        | Auth     | Historial de conversaciones del usuario                 |
| GET    | `/stats`       | Auth     | Estadísticas de interacciones (últimos 30 días)         |

**Características del Chat IA:**
- **RAG Híbrido** (por defecto): búsqueda semántica vectorial (`pgvector`) sobre los `portfolio_documents`, con fallback a contexto completo.
- **Cache en Redis** del contexto IA (30 minutos).
- **Cuota diaria**: 10 mensajes para usuarios no autenticados.
- **Rate limiting**: 5 requests/minuto por IP.
- **Moderación**: 3 strikes y bloqueo por contenido ofensivo.
- **Pitch Rules**: reglas personalizadas de venta definidas por el talento.
- **Integración Gemini**: modelo configurable, retry con backoff exponencial, y fallback a modelo alternativo.

### 7. AI Management (`/api/v1/ai`)

| Método | Ruta           | Auth     | Descripción                                            |
| ------ | -------------- | -------- | ------------------------------------------------------ |
| POST   | `/translate`   | Admin    | Traduce contenido JSON del portafolio a otro idioma usando Gemini |
| POST   | `/cv-extract`  | Auth     | Extrae datos de un CV (PDF/DOCX/imagen) a JSON estructurado usando MarkItDown + Gemini |

### 8. Red Profesional — Networking (`/api/v1/network`)

| Método | Ruta                          | Auth | Descripción                                          |
| ------ | ----------------------------- | ---- | ---------------------------------------------------- |
| POST   | `/connect/{user_id}`          | Auth | Enviar solicitud de conexión                         |
| PUT    | `/accept/{connection_id}`     | Auth | Aceptar conexión (crea conversación + mensaje auto)  |
| PUT    | `/reject/{connection_id}`     | Auth | Rechazar conexión                                    |
| GET    | `/connections`                | Auth | Listar conexiones aceptadas                          |
| GET    | `/pending`                    | Auth | Listar solicitudes de conexión pendientes            |
| GET    | `/status/{target_user_id}`    | Auth | Ver estado de conexión con un usuario específico     |
| GET    | `/degrees/{target_user_id}`   | Auth | Grados de separación (0-3, usando CTE recursivo SQL) |
| GET    | `/feed`                       | Auth | Feed de actividad de la red (eventos de conexiones de 1er y 2do grado) |
| GET    | `/suggestions`                | Auth | Sugerencias de conexión generadas por IA (Headhunter Matchmaker) |

### 9. Chat Peer-to-Peer (`/api/v1/chat-p2p`)

| Método | Ruta                                       | Auth  | Descripción                                      |
| ------ | ------------------------------------------ | ----- | ------------------------------------------------ |
| POST   | `/conversations`                           | Auth  | Iniciar u obtener conversación con otro usuario  |
| GET    | `/conversations`                           | Auth  | Listar conversaciones del usuario                |
| GET    | `/conversations/{id}/messages`             | Auth  | Obtener mensajes de una conversación             |
| POST   | `/conversations/{id}/messages`             | Auth  | Enviar mensaje                                   |
| PUT    | `/conversations/{id}/read`                 | Auth  | Marcar mensajes como leídos                      |
| GET    | `/unread-count`                            | Auth  | Contador de mensajes no leídos                   |
| WS     | `/ws?token=`                               | Auth  | WebSocket para mensajes en tiempo real           |

### 10. B2B / Meta-Reclutador (`/api/v1/b2b`)

| Método | Ruta                               | Auth | Permiso Requerido       | Descripción                                         |
| ------ | ---------------------------------- | ---- | ----------------------- | --------------------------------------------------- |
| POST   | `/search`                          | Auth | `can_use_b2b_search`    | Búsqueda semántica de talento (pgvector cosine distance) |
| POST   | `/tribunal/candidate`              | Auth | `can_execute_tribunal`  | Evalúa un candidato individual para el tribunal     |
| POST   | `/tribunal/moderator`              | Auth | `can_execute_tribunal`  | Evalúa y modera respuestas de múltiples candidatos  |
| GET    | `/tribunals/history`               | Auth | `can_execute_tribunal`  | Historial de tribunales del reclutador              |
| GET    | `/tribunals/talent-feedback`       | Auth | `can_view_own_feedback` | Feedback recibido por el talento en tribunales      |
| GET    | `/insights/demand`                 | Auth | `can_view_demand`       | Insights de demanda del mercado (simulado)          |
| POST   | `/qa/reset-credits`                | Auth | SUPERADMIN              | Recarga créditos para testing                       |

### 11. Administración RBAC (`/api/v1/admin/rbac`)

| Método | Ruta                                   | Auth | Permiso              | Descripción                               |
| ------ | -------------------------------------- | ---- | -------------------- | ----------------------------------------- |
| GET    | `/roles`                               | Auth | `can_manage_roles`   | Lista todos los roles con sus permisos    |
| GET    | `/permissions`                         | Auth | `can_manage_roles`   | Lista todos los permisos disponibles      |
| POST   | `/roles/{id}/permissions/toggle`       | Auth | `can_manage_roles`   | Otorga/revoca un permiso a un rol         |
| GET    | `/users`                               | Auth | `can_manage_roles`   | Lista usuarios para asignación de roles   |
| PUT    | `/users/{id}/role`                     | Auth | `can_manage_roles`   | Asigna un rol a un usuario                |

### 12. Open Graph Cards (`/card/{username}`)

| Método | Ruta              | Auth    | Descripción                                             |
| ------ | ----------------- | ------- | ------------------------------------------------------- |
| GET    | `/card/{username}`| Público | Genera meta tags OG (Open Graph) para compartir en redes sociales (Facebook, LinkedIn, Twitter, WhatsApp) + redirección al frontend |

### 13. Storage Vinculado (`/api/v1/storage`)

| Método | Ruta              | Auth | Descripción                                         |
| ------ | ----------------- | ---- | --------------------------------------------------- |
| GET    | `/google/login`   | Auth | Inicia OAuth para vincular Google Drive (free tier) |
| GET    | `/google/callback`| Auth | Callback OAuth — guarda refresh token de Google     |

### 14. Utilidades

| Método | Ruta       | Auth    | Descripción               |
| ------ | ---------- | ------- | ------------------------- |
| GET    | `/health`  | Público | Health check de la API    |

---

## 🔐 Flujo de Autenticación

```
┌──────────┐         ┌──────────────┐         ┌───────────┐
│ Frontend │         │  Backend     │         │ PostgreSQL│
└────┬─────┘         └──────┬───────┘         └─────┬─────┘
     │                      │                       │
     │  POST /auth/login    │                       │
     │  (username+password) │                       │
     ├─────────────────────►│                       │
     │                      │  Verificar credenciales│
     │                      ├──────────────────────►│
     │                      │◄──────────────────────┤
     │                      │                       │
     │                      │  1. Generar Access JWT│
     │                      │  2. Generar Refresh JWT│
     │                      │  3. Guardar Refresh en DB│
     │                      ├──────────────────────►│
     │                      │◄──────────────────────┤
     │  Set-Cookie:         │                       │
     │  access_token (httpOnly)                     │
     │  refresh_token (httpOnly)                    │
     │◄─────────────────────┤                       │
     │                      │                       │
     │  GET /user/profile   │                       │
     │  Cookie: access_token│                       │
     ├─────────────────────►│                       │
     │                      │  Validar JWT (firma, exp)│
     │                      │  Extraer usuario via sub │
     │                      │  Verificar is_deleted  │
     │                      │  (Opcional) impersonar │
     │  Perfil + permisos   │                       │
     │◄─────────────────────┤                       │
```

### Mecanismos de Seguridad

- **Passwords**: hasheadas con **Argon2** (el ganador del PHC — Password Hashing Competition).
- **JWT dual**: Access Token (corta duración, 30 min por defecto) + Refresh Token (larga duración, 7 días por defecto) con rotación y revocación.
- **HttpOnly Cookies**: los tokens viajan en cookies, no accesibles desde JavaScript.
- **Rate Limiting**: Redis-based sliding window para el chat público.
- **Moderation Strikes**: 3 strikes y bloqueo de IP por 24 horas.
- **Encryption de API Keys**: las keys de Gemini se encriptan con **Fernet (AES-128-CBC)** antes de almacenarse.
- **Impersonation**: solo usuarios con permiso `can_impersonate` pueden generar tokens de suplantación (para testing/QA).
- **Password Complexity**: 8+ caracteres, mayúscula, minúscula, número, carácter especial.
- **Hot-rehash**: migración automática de hashes antiguos a Argon2 en el login.
- **Lockout**: cuenta bloqueada tras múltiples intentos fallidos.

---

## 👥 Sistema de Roles y Permisos (RBAC)

### Roles por Defecto

| Rol      | Permisos                                                              | ¿Quién lo tiene?                |
| -------- | --------------------------------------------------------------------- | ------------------------------- |
| **Owner**| Todos (8 permisos) incluyendo `can_impersonate`, `can_manage_roles`    | Dueño del sistema / SUPERADMIN  |
| **Admin**| `can_approve_kyc`, `can_view_demand`                                  | Administradores                 |
| **Hunter**| `can_execute_tribunal`, `can_use_b2b_search`, `can_view_demand`     | Reclutadores verificados (KYC)  |
| **Talent**| `can_edit_portfolio`, `can_view_own_feedback`, `can_view_demand`    | Talentos con portafolio         |
| **Worker**| `can_view_demand`                                                    | Usuarios sin rol específico     |

### Permisos Atómicos

| Permiso                  | Descripción                                         |
| ------------------------ | --------------------------------------------------- |
| `can_execute_tribunal`   | Ejecutar tribunales B2B (gasta créditos)            |
| `can_approve_kyc`        | Aprobar cuentas de reclutadores                     |
| `can_use_b2b_search`     | Buscar en la base de talentos                       |
| `can_edit_portfolio`     | Editar el portafolio propio                         |
| `can_view_own_feedback`  | Ver feedback de tribunales                          |
| `can_impersonate`        | Suplantar usuarios (QA)                             |
| `can_view_demand`        | Ver insights de demanda del mercado                 |
| `can_manage_roles`       | Gestionar roles y permisos (Admin panel)            |

---

## 🤖 Motor de IA y RAG Vectorial

### Arquitectura del Sistema RAG

```
                    ┌──────────────────────┐
                    │   Base de Datos      │
                    │  (PostgreSQL + ORM)  │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │   rag_sync.py        │
                    │   sync_user_rag_     │
                    │   embeddings()       │
                    │   (model → texto →   │
                    │    embedding → store)│
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │  portfolio_documents  │
                    │  (pgvector 768d)      │
                    │  Índice HNSW         │
                    └──────────┬───────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
  ┌───────▼───────┐   ┌───────▼───────┐   ┌────────▼────────┐
  │  Chat IA      │   │  B2B Search   │   │  B2B Tribunal   │
  │  (RAG híbrido)│   │  (semántico)  │   │  (evaluación)   │
  └───────────────┘   └───────────────┘   └─────────────────┘
```

### Flujo: sync_user_rag_embeddings()

```
1. Leer todos los modelos activos del usuario (Perfil, Experiencia, Proyecto, etc.)
2. Serializar cada registro a texto plano (JSON)
3. Para cada registro:
   a. Si existe un PortfolioDocument con mismo (tipo_entidad, entidad_id):
      - Si el texto es idéntico → SKIP (ahorro de tokens)
      - Si cambió → regenerar embedding + actualizar
   b. Si no existe → generar embedding + crear nuevo documento
4. Eliminar documentos huérfanos (registros que ya no existen o están inactivos)
```

### Flujo: Chat (RAG Híbrido)

```
1. Recibir mensaje del usuario + username del portafolio
2. Verificar autenticación, rate limit, cuota diaria, moderación
3. Obtener usuario del portafolio (por username/slug/email)
4. Generar embedding de la consulta del usuario
5. Búsqueda semántica en pgvector (cosine distance):
   - Siempre incluir PERFIL del usuario
   - Top 5 documentos más relevantes
6. Si la búsqueda vectorial falla → fallback a contexto completo (todos los modelos)
7. Cachear en Redis por 30 minutos
8. Construir system prompt con contexto + pitch rules + directrices
9. Llamar a Gemini (ask_oppy_ai) con retry y fallback
10. Moderar respuesta (ALERTA_DE_SEGURIDAD_OPPY_001)
11. Registrar en chat_logs (con geolocalización vía ipinfo.io)
```

### Orquestador: ask_oppy_ai()

```
1. Obtener configuración del modelo desde AIModelConfig (BD dinámica)
2. Determinar API Key (propia del usuario encriptada vs. global)
3. Si usa API Key global → descontar crédito (o cobrar si es premium)
4. Ejecutar llamada a Gemini con temperature, system_instruction, response_mime_type
5. Si falla → retry con backoff exponencial (2^attempt seconds)
6. Último intento → cambiar a modelo alternativo (fallback)
7. Reparar JSON si se espera JSON (usando json-repair)
8. Registrar métricas en LLMRequestLog (tokens, costo, duración, éxito/fallo)
9. Si todos los intentos fallan → refund de crédito + mensaje de error
```

---

## 💼 Ecosistema B2B

### Meta-Reclutador (Búsqueda Semántica)

```
POST /api/v1/b2b/search
─────────────────────────────────────────────────
1. Recibir consulta del reclutador (texto libre)
2. Generar embedding de la consulta (gemini-embedding-2)
3. Buscar en portfolio_documents usando cosine_distance
4. Agrupar por usuario, filtrando solo is_visible_b2b = True
5. Devolver top N usuarios con match_score (% de similitud)
6. Descontar crédito al reclutador (freemium)
```

### Tribunal de Talentos

El Tribunal B2B es un sistema multi-agente donde:

1. **Reclutador** elige una pregunta técnica y N candidatos.
2. **Por cada candidato** (`/tribunal/candidate`):
   - Se genera un embedding de la pregunta.
   - Se buscan los 3 documentos más relevantes del candidato.
   - El "Clon Digital" (Gemini) responde usando SÓLO ese contexto (zero-hallucination).
   - Pitch rules del candidato se inyectan si aplican.
3. **Moderador** (`/tribunal/moderator`):
   - Recibe todas las respuestas en orden aleatorio (anti-sesgo).
   - Gemini actúa como "Moderador Neutral" evaluando mérito técnico.
   - Devuelve resumen markdown con fortalezas y debilidades.
4. **Feedback Post-Tribunal** (background task):
   - Para cada candidato, Gemini genera feedback constructivo privado sobre cómo mejorar su perfil.

### Insights de Demanda

Endpoint `/b2b/insights/demand` — Actualmente retorna datos simulados del mercado tech global (React/Next.js, Python/FastAPI, Cloud AWS/GCP) como solución al "Cold Start Problem". Diseñado para escalar a datos orgánicos desde `B2BSearchLog`.

---

## 💾 Almacenamiento de Archivos

### Cloudflare R2 (Premium)

- **S3-compatible**: usa `boto3` con endpoint de R2.
- **Nombres únicos**: cada archivo se almacena con un UUID prefix para evitar colisiones.
- **Cuota**: 25 MB para usuarios gratuitos, ilimitado para premium (trackeado via `storage_used` en usuario).
- **Público**: URLs públicas configurables via `R2_PUBLIC_URL`.

### Google Drive (Free Tier)

- **OAuth2**: flujo de autorización para acceso a Google Drive del usuario.
- **Alcance**: `drive.file` — solo archivos creados por la app.
- **Refresh token**: almacenado en BD para acceso persistente.
- **Proxy de imágenes**: el endpoint `/api/v1/images/proxy` sirve imágenes de Google Drive para evitar problemas de CORS y autenticación.

---

## 📧 Notificaciones y Email

Servicio de correo unificado (`EmailService`) con dos proveedores configurables via `EMAIL_PROVIDER`:

| Proveedor | Configuración                            | Uso                            |
| --------- | ---------------------------------------- | ------------------------------ |
| **Resend**| `EMAIL_PROVIDER=resend` + `RESEND_API_KEY` | Producción (API moderna)      |
| **SMTP**  | `EMAIL_PROVIDER=smtp` + credenciales SMTP  | Desarrollo / legacy           |

**Plantillas HTML disponibles:**
- `email_confirmation.html` — Confirmación de registro
- `password_reset.html` — Restablecimiento de contraseña
- `reception_discrepancy.html` — Discrepancias de recepción

---

## ⚡ Cache y Rate Limiting

### Redis — Usos

| Uso                    | Key Pattern                          | TTL      |
| ---------------------- | ------------------------------------ | -------- |
| Contexto IA (chat)     | `ai_context:{usuario_id}`            | 30 min   |
| Cuota chat no-auth     | `chat_quota:{ip}:{portfolio_user_id}`| 24 hrs   |
| Rate limiting          | `rate_limit:chat:{ip}`               | 1 min    |
| Moderation strikes     | `moderation_strikes:{ip}`            | 24 hrs   |
| Global Gemini Lock     | `gemini_global_api_lock`             | 15 seg   |

### Rate Limiting por Endpoint

| Endpoint      | Límite              | Ventana |
| ------------- | ------------------- | ------- |
| Chat público  | 5 requests          | 60 seg  |
| Cuota no-auth | 10 mensajes         | 24 hrs  |

---

## 🔌 WebSockets — Conexiones en Tiempo Real

Endpoint: `ws://host:8000/api/v1/chat-p2p/ws?token={jwt_token}`

El `ConnectionManager` maneja las conexiones activas (mapeo `user_id → Set[WebSocket]`).

**Eventos enviados:**
- `{"type": "new_message", "conversation_id": "uuid"}` — notifica al destinatario de un nuevo mensaje.

---

## 🛡️ Seguridad

| Capa              | Medida                                                       |
| ----------------- | ------------------------------------------------------------ |
| **Transporte**    | HTTPS en producción; CORS configurado; SessionMiddleware para OAuth |
| **Autenticación** | JWT dual (access + refresh); HttpOnly cookies; OAuth2 Google |
| **Contraseñas**   | Argon2 (PHC winner); hot-rehash en login; complexity validation |
| **API Keys**      | Encriptación Fernet (AES-128-CBC) en BD                      |
| **Rate Limit**    | Sliding window en Redis; quotas diarias para no-auth          |
| **Moderación**    | 3 strikes de seguridad → bloqueo de IP por 24h               |
| **Input**         | Validación Pydantic en todos los endpoints; sanitización en prompts IA |
| **Inyección SQL** | ORM SQLAlchemy (previene SQL injection); queries parametrizadas |
| **Soft Delete**   | Ninguna entidad se elimina físicamente (`is_active = False`)  |
| **Cuentas**       | Lockout por múltiples intentos fallidos de login              |

---

## 🚀 Despliegue

### Docker (Recomendado)

```bash
# Build y deploy
docker compose up --build -d

# La API estará disponible en http://localhost:8000
# Documentación interactiva: http://localhost:8000/docs
```

### Producción (Railway / Render / Fly.io)

```yaml
# Variables de entorno requeridas:
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db
REDIS_URL=redis://host:6379/0
SECRET_KEY=<random-64-hex>
JWT_ACCESS_SECRET_KEY=<random-64-hex>
JWT_REFRESH_SECRET_KEY=<random-64-hex>
ENCRYPTION_KEY=<fernet-key>
GEMINI_API_KEY=<google-gemini-key>
R2_ACCOUNT_ID=<cloudflare-r2-id>
R2_ACCESS_KEY_ID=<r2-access-key>
R2_SECRET_ACCESS_KEY=<r2-secret>
R2_BUCKET_NAME=<bucket-name>
R2_PUBLIC_URL=<bucket-public-url>
ENVIRONMENT=production
```

---

## 🌱 Flujo de CI / Seed Data

En cada inicio de la aplicación (lifespan de FastAPI):

1. **`init_db()`** → Crea extensión `vector` en PostgreSQL + tablas si no existen.
2. **`seed_ai_models()`** → Inserta modelos Gemini con sus precios si no existen.
3. **`seed_rbac()`** → Crea roles (Owner, Admin, Hunter, Talent, Worker) y permisos.
4. **`seed_admin_user()`** → Crea el usuario administrador si no existe (username y password desde `.env`).
5. **`sync_database_sequences()`** → Sincroniza secuencias PostgreSQL para evitar errores de duplicado de IDs.

---

## 🔧 Configuración de Entorno (`.env`)

```ini
# --- App Configuration ---
ENVIRONMENT=development
WEBSITE_URL=http://localhost:5173
API_URL=http://localhost:8000

# --- Database ---
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/oppytalentDB
DB_SCHEMA=oppy

# --- Redis ---
REDIS_URL=redis://host:6379/0

# --- JWT & Security ---
JWT_ACCESS_SECRET_KEY=<64-char-hex>
JWT_REFRESH_SECRET_KEY=<64-char-hex>
SECRET_KEY=<64-char-hex>
ENCRYPTION_KEY=<fernet-base64-key>
ACCESS_TOKEN_EXPIRE_MINUTES=1440
REFRESH_TOKEN_EXPIRE_MINUTES=10080

# --- Google OAuth ---
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/google/callback

# --- Cloudflare R2 ---
R2_ACCOUNT_ID=...
R2_ACCESS_KEY_ID=...
R2_SECRET_ACCESS_KEY=...
R2_BUCKET_NAME=oppytalent-images
R2_PUBLIC_URL=https://pub-xxxxx.r2.dev

# --- Admin ---
ADMIN_USERNAME=admin
ADMIN_PASSWORD=<secure-password>

# --- AI ---
GEMINI_API_KEY=<google-gemini-api-key>

# --- Email ---
EMAIL_PROVIDER=resend
RESEND_API_KEY=re_...
MAIL_FROM="OppyTalent <support@oppytalent.com>"
```

---

## 📊 Resumen de Capacidades

| Funcionalidad                          | Estado     | Dependencias                   |
| -------------------------------------- | ---------- | ------------------------------ |
| CRUD de portafolio (7 entidades)       | ✅ Completo | PostgreSQL                     |
| Multi-idioma (traducciones)            | ✅ Completo | PostgreSQL                     |
| Chat IA con RAG vectorial              | ✅ Completo | Gemini, pgvector, Redis        |
| Búsqueda semántica B2B                 | ✅ Completo | pgvector, Gemini embeddings    |
| Tribunal de Talentos (multi-agente)    | ✅ Completo | Gemini, pgvector               |
| Red profesional (conexiones, feed)     | ✅ Completo | PostgreSQL                     |
| Chat P2P + WebSockets                 | ✅ Completo | PostgreSQL, Redis              |
| Autenticación JWT + OAuth Google       | ✅ Completo | PostgreSQL, Redis              |
| RBAC granular                          | ✅ Completo | PostgreSQL                     |
| Extracción de CV (MarkItDown + Gemini) | ✅ Completo | Gemini, MarkItDown             |
| Traducción automática                  | ✅ Completo | Gemini                         |
| Almacenamiento R2 + Google Drive       | ✅ Completo | Cloudflare R2, Google Drive API|
| Rate limiting + moderación             | ✅ Completo | Redis                          |
| Emails transaccionales                 | ✅ Completo | Resend / SMTP                  |
| Open Graph cards                       | ✅ Completo | —                              |
| Sugerencias de red con IA              | ✅ Completo | Gemini, pgvector               |
| Insights de demanda (simulados)        | ✅ Completo | —                              |

---

> **OppyTalent** — Transformando currículums en experiencias interactivas potenciadas por IA.
