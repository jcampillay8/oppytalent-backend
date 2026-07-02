# Reporte de Pruebas: Módulo Core — Suite Completa ISO 27001 + ISO 9001

## Proyecto: OppyTalent — Portafolio API

Este directorio contiene las pruebas fundamentales de "Sanity Check" más la suite completa de seguridad, calidad y robustez exigida por **ISO 27001:2022** (Seguridad de la Información) e **ISO 9001:2015** (Gestión de Calidad). Cada test está diseñado para verificar controles específicos de estas normas y garantizar que la plataforma OppyTalent cumple con los estándares más rigurosos de la industria.

---

## Estructura de Archivos de Test

| Archivo | Cobertura | ISO Relacionada |
|---------|-----------|-----------------|
| `conftest.py` | Fixtures: async engine, test DB, seed roles/users, auth clients | Infraestructura de testing |
| `test_core.py` | Sanity Check: OpenAPI, Health endpoint, DB connection | ISO 9001 §8.3, §9.1 |
| `test_main.py` | CORS, HTTPS middleware, Server header | ISO 27001 §A.13.1, §A.13.2 |
| `test_database.py` | Integridad de BD: engine pool, async driver, PostgreSQL version | ISO 27001 §A.12.6, ISO 9001 §7.5 |
| `test_dependencies.py` | Autenticación: endpoints públicos vs protegidos | ISO 27001 §A.9.2 |
| `test_auth_jwt.py` | **JWT: firma, expiración, tampering, algorithm none, claims** | ISO 27001 §A.9.2, §A.9.4, §A.10.1 |
| `test_authorization_rbac.py` | **RBAC: roles, permisos, RequirePermission, admin access** | ISO 27001 §A.9.2, §A.9.3 |
| `test_input_validation.py` | **Validación: SQLi, XSS, path traversal, oversized payload** | ISO 27001 §A.14.2, ISO 9001 §8.3 |
| `test_error_handling.py` | **Errores: 404 sin stack trace, 422 consistente, WWW-Authenticate** | ISO 27001 §A.14.2, §A.16.1 |
| `test_secrets_management.py` | **Secretos: env vars, hardcoding, longitud de claves JWT** | ISO 27001 §A.10.1, §A.18.1 |
| `test_session_security.py` | **Sesión: CORS, cookies HttpOnly, Server header, credentials** | ISO 27001 §A.9.2, §A.13.1 |
| `test_https_security.py` | **HTTPS: redirect, HSTS, scheme rewriting, proxy** | ISO 27001 §A.13.1, §A.13.2 |
| `test_rate_limit.py` | **Rate limiting: slowapi, bloqueo 429, recuperación** | ISO 27001 §A.12.6, §A.14.2 |
| `test_utils.py` | **Criptografía: Argon2id, bcrypt legacy, rehash detection** | ISO 27001 §A.10.1 |
| `test_config_validation.py` | **Config: settings class, env vars, JWT secrets no default** | ISO 9001 §7.5, §8.1 |
| `test_logging_audit.py` | **Logging: audit trail, session history, refresh token tracking** | ISO 27001 §A.12.4, §A.18.1 |
| `test_connection_pool.py` | **Pool: conexiones, maxsize, async driver** | ISO 9001 §9.1, escalabilidad |
| `test_cache_behavior.py` | **Cache: Redis get/set/clear, namespace invalidation** | ISO 9001 §9.1, escalabilidad |
| `test_resource_cleanup.py` | **Limpieza: context vars, sessions, transaction rollback** | ISO 9001 §8.1, robustez |

---

## Tests Existentes — Documentación Completa

---

### 1. `test_fastapi_starts_and_openapi_is_available` (`test_core.py`)
- **¿Qué testea?** Verifica que la aplicación FastAPI se inicializa sin errores de sintaxis, dependencias rotas o importaciones circulares. Confirma que el schema OpenAPI se genera correctamente con el título "Portafolio API - OppyTalent".
- **ISO 9001 §8.3 (Diseño y Desarrollo) — Verificación:** El contrato API está intacto y la documentación Swagger está disponible.
- **Success →** Arranque cero errores, routing saludable, documentación Swagger disponible para integración con frontend.
- **Fallo →** Error de importación, sintaxis inválida, o dependencia faltante en `app/main.py`.

### 2. `test_health_endpoint` (`test_core.py`)
- **¿Qué testea?** Verifica que el endpoint `/health` responda `200 OK` con `{"status": "ok"}`.
- **ISO 9001 §9.1 (Seguimiento y Medición):** El health check permite a balanceadores de carga y orquestadores verificar que la aplicación está operativa.
- **Success →** La aplicación responde a sondas de salud. Los deploys en Railway/K8s pueden verificar la instancia.
- **Fallo →** La aplicación no arrancó correctamente o el router de health no está registrado.

### 3. `test_database_connection` (`test_core.py`)
- **¿Qué testea?** Ejecuta `SELECT 1` en la base de datos de pruebas para verificar conectividad básica.
- **ISO 27001 §A.12.6 (Seguridad en operaciones):** La conexión a BD es operativa.
- **Success →** Pool asíncrono configurado correctamente, PostgreSQL responde.
- **Fallo →** Credenciales BD incorrectas, motor PostgreSQL caído, o URL mal configurada.

### 4. `test_openapi_defines_all_routes` (`test_core.py`)
- **¿Qué testea?** Verifica que rutas críticas (`/health`, `/api/v1/auth/login`, `/api/v1/user/profile`) estén registradas en el schema OpenAPI.
- **ISO 9001 §8.3 (Diseño y Desarrollo):** Los endpoints esperados están correctamente registrados.
- **Success →** Todas las rutas del core están expuestas y documentadas.
- **Fallo →** Un router no se incluyó en `main.py` o hay un conflicto de rutas.

---

### 5. `test_https_middleware_rewrites_scheme_in_production` (`test_main.py`)
- **¿Qué testea?** Simula entorno production con header `x-forwarded-proto: https` y verifica que el middleware de FastAPI reescriba el scheme correctamente.
- **ISO 27001 §A.13.1 (Seguridad de redes):** Detrás de proxies (Railway, Nginx, Cloudflare), la app sabe que está en HTTPS.
- **Success →** Las URLs generadas usan HTTPS en producción. Comunicación cifrada extremo a extremo.
- **Fallo →** El middleware HTTPS no procesa correctamente los headers del proxy, generando URLs HTTP.

### 6. `test_cors_headers_allow_configured_origins` (`test_main.py`)
- **¿Qué testea?** Envía OPTIONS preflight desde el origen configurado y verifica que CORS lo acepte.
- **ISO 9001 §8.3 (Diseño y Desarrollo):** El frontend (Vite/Flutter) puede comunicarse con la API sin errores de CORS.
- **Success →** Los navegadores no bloquean peticiones legítimas del frontend.
- **Fallo →** Error "CORS policy blocked" en el navegador del cliente.

### 7. `test_cors_rejects_malicious_origins` (`test_main.py`)
- **¿Qué testea?** Verifica que orígenes maliciosos (evil.com, malware-site.ru) NO sean aceptados por CORS.
- **ISO 27001 §A.13.1 (Seguridad de redes):** Sitios maliciosos no pueden hacer peticiones cross-origin a la API.
- **Success →** Aislamiento de origen garantizado. Un atacante no puede robar datos via CORS desde un sitio externo.
- **Fallo →** Cualquier sitio web podría leer datos de la API.

### 8. `test_server_header_not_exposed` (`test_main.py`)
- **¿Qué testea?** Verifica que el header `Server` no filtre información como "uvicorn", "python" o "fastapi".
- **ISO 27001 §A.14.2 (Seguridad en desarrollo) — Fingerprinting:** No se filtra información de versiones del servidor.
- **Success →** Un atacante no puede identificar la versión de uvicorn/FastAPI para buscar vulnerabilidades conocidas.
- **Fallo →** El servidor revela su identidad y versión, facilitando ataques dirigidos.

---

### 9. `test_database_engine_pool_configured` (`test_database.py`)
- **¿Qué testea?** Verifica que el engine de SQLAlchemy tenga un pool configurado con `maxsize >= 5`.
- **ISO 9001 §9.1 (Infraestructura robusta):** El pool de conexiones está optimizado para producción.
- **Success →** Múltiples requests concurrentes pueden acceder a BD sin saturar conexiones.
- **Fallo →** Sin pool, cada request crea una nueva conexión, degradando rendimiento bajo carga.

### 10. `test_database_url_uses_async_driver` (`test_database.py`)
- **¿Qué testea?** Verifica que `DATABASE_URL` comience con `postgresql+asyncpg://`.
- **ISO 9001 §8.3 (Diseño y Desarrollo):** El driver asíncrono asyncpg no bloquea el event loop.
- **Success →** Las operaciones de BD son no-bloqueantes, maximizando throughput.
- **Fallo →** La app podría usar un driver síncrono que bloquee el event loop de asyncio.

### 11. `test_database_session_autoflush_disabled` (`test_database.py`)
- **¿Qué testea?** Verifica que `autoflush=False` en la sesión de BD.
- **ISO 9001 §8.1 (Control de procesos):** Las transacciones son explícitas y controladas.
- **Success →** No hay escrituras no deseadas a BD. El desarrollador controla cuándo se persisten los cambios.
- **Fallo →** Autoflush podría enviar datos incompletos a la BD antes de tiempo.

### 12. `test_essential_tables_exist` (`test_database.py`)
- **¿Qué testea?** Verifica que las tablas esenciales (usuarios, roles, permissions, proyectos) estén registradas en `Base.metadata`.
- **ISO 9001 §7.5 (Información documentada):** El esquema de BD está correctamente definido.
- **Success →** La estructura de BD está completa y lista para operar.
- **Fallo →** Faltan modelos o migraciones por aplicar.

---

### 13. `test_jwt_invalid_secret_rejected` (`test_auth_jwt.py`)
- **¿Qué testea?** Envía un token JWT firmado con una clave secreta diferente a la del servidor.
- **ISO 27001 §A.9.2, §A.9.4 — Autenticación:** La firma HMAC-SHA256 protege contra tokens forjados.
- **Success →** Un atacante no puede forjar tokens aunque conozca la estructura del JWT.
- **Fallo →** La verificación de firma no funciona, cualquier token es aceptado.

### 14. `test_expired_jwt_returns_401` (`test_auth_jwt.py`)
- **¿Qué testea?** Crea un JWT con `exp` en el pasado y verifica 401.
- **ISO 27001 §A.9.2, §A.9.4 — Gestión de sesiones:** Ciclo de vida finito de tokens.
- **Success →** Tokens robados o filtrados tienen ventana de ataque limitada (30 min por defecto).
- **Fallo →** Tokens expirados seguirían siendo válidos, permitiendo acceso indefinido.

### 15. `test_jwt_without_sub_rejected` (`test_auth_jwt.py`)
- **¿Qué testea?** Genera un JWT sin el claim `sub` (identificador de usuario).
- **ISO 27001 §A.14.2 — Validación de entrada:** Claims obligatorios son validados.
- **Success →** No se aceptan tokens malformados. La estructura del token está estrictamente validada.
- **Fallo →** Tokens incompletos podrían autenticar requests sin identificar al usuario.

### 16. `test_tampered_jwt_body_rejected` (`test_auth_jwt.py`)
- **¿Qué testea?** Modifica el payload de un JWT válido sin re-firmarlo (ataque de alteración).
- **ISO 27001 §A.10.1 — Integridad:** La firma protege contra modificación del payload.
- **Success →** Un atacante no puede modificar claims (como `sub` o `role_id`) sin conocer la clave secreta.
- **Fallo →** Cualquier usuario podría escalar privilegios modificando su token.

### 17. `test_nonexistent_user_in_jwt_rejected` (`test_auth_jwt.py`)
- **¿Qué testea?** Token firmado válidamente pero con un `sub` que no existe en BD.
- **ISO 27001 §A.9.2 — Control de acceso:** La autenticación verifica existencia del usuario en BD.
- **Success →** Incluso con firma válida, un usuario eliminado o inexistente no puede acceder.
- **Fallo →** Usuarios dados de baja podrían seguir accediendo hasta que expire su token.

### 18. `test_jwt_algorithm_none_rejected` (`test_auth_jwt.py`)
- **¿Qué testea?** Envía un JWT firmado con algoritmo `none` (ataque clásico de JWT).
- **ISO 27001 §A.10.1 — Controles criptográficos:** El algoritmo `none` no está permitido.
- **Success →** Un atacante no puede evitar la verificación de firma usando `alg: none`.
- **Fallo →** Vulnerabilidad crítica: cualquiera puede crear tokens sin conocer la clave secreta.

### 19. `test_login_returns_tokens` (`test_auth_jwt.py`)
- **¿Qué testea?** Verifica que el endpoint de login retorne tokens de acceso.
- **ISO 9001 §8.3 — Funcionalidad de autenticación:** El flujo de login completo funciona.
- **Success →** Usuarios válidos pueden autenticarse y recibir tokens JWT.
- **Fallo →** El login no genera tokens, rompiendo todo el flujo de autenticación.

---

### 20. `test_unauthenticated_request_returns_401` (`test_authorization_rbac.py`)
- **¿Qué testea?** Accede a un endpoint protegido sin token de autenticación.
- **ISO 27001 §A.9.2 — Control de acceso:** Todos los endpoints protegidos requieren autenticación.
- **Success →** No hay endpoints públicos que expongan datos sensibles de usuarios.
- **Fallo →** Datos protegidos accesibles sin autenticación.

### 21. `test_admin_rbac_endpoints_require_permission` (`test_authorization_rbac.py`)
- **¿Qué testea?** Verifica que endpoints de administración RBAC requieran permisos específicos.
- **ISO 27001 §A.9.2, §A.9.3 — Autorización:** El RBAC funciona correctamente.
- **Success →** Solo usuarios con `can_manage_roles` pueden gestionar roles y permisos.
- **Fallo →** Usuarios sin permisos adecuados pueden modificar la configuración de seguridad.

### 22. `test_admin_rbac_endpoints_accessible_by_admin` (`test_authorization_rbac.py`)
- **¿Qué testea?** El usuario con rol Owner puede acceder a todos los endpoints de administración RBAC.
- **ISO 27001 §A.9.2 — Privilegios especiales:** Los administradores pueden realizar tareas de gestión.
- **Success →** Los administradores legítimos tienen acceso completo a la gestión de RBAC.
- **Fallo →** Los administradores no pueden gestionar roles, bloqueando la administración del sistema.

---

### 23. `test_sql_injection_in_query_params` (`test_input_validation.py`)
- **¿Qué testea?** Inyecta patrones clásicos de SQL Injection en parámetros de query.
- **ISO 27001 §A.14.2 — Seguridad en desarrollo:** SQLAlchemy con parámetros parametrizados previene inyección.
- **Success →** La base de datos está protegida contra el ataque #1 de OWASP.
- **Fallo →** El SQL llega a la BD (código 500), indicando una vulnerabilidad crítica de inyección SQL.

### 24. `test_xss_in_request_body` (`test_input_validation.py`)
- **¿Qué testea?** Envía scripts maliciosos (`<script>alert(1)</script>`) en el body.
- **ISO 27001 §A.14.2 — Validación de entrada:** FastAPI/Pydantic rechaza contenido HTML/JS malicioso.
- **Success →** Los datos almacenados no pueden ejecutar JavaScript en navegadores de otros usuarios.
- **Fallo →** Vulnerabilidad de Cross-Site Scripting (XSS) — OWASP #2.

### 25. `test_path_traversal_blocked` (`test_input_validation.py`)
- **¿Qué testea?** Intenta acceder a archivos fuera del directorio permitido (`../../../etc/passwd`).
- **ISO 27001 §A.14.2 — Protección de recursos:** StaticFiles de FastAPI previene traversal.
- **Success →** Atacantes no pueden leer archivos del sistema operativo.
- **Fallo →** Un atacante podría leer `/etc/passwd`, claves SSH, o código fuente.

### 26. `test_oversized_payload_rejected` (`test_input_validation.py`)
- **¿Qué testea?** Envía un payload JSON extremadamente grande (10MB).
- **ISO 27001 §A.12.6 — Protección contra DoS:** Límite de tamaño de request.
- **Success →** El servidor no se desborda por payloads gigantes (ataque de agotamiento de recursos).
- **Fallo →** Un atacante puede agotar la memoria del servidor con requests maliciosos.

### 27. `test_invalid_json_rejected_gracefully` (`test_input_validation.py`)
- **¿Qué testea?** Envía texto que no es JSON a un endpoint que espera JSON.
- **ISO 27001 §A.14.2 — Manejo robusto de errores:** El servidor responde sin crash.
- **Success →** Datos malformados no causan caídas del servidor ni exponen stack traces.
- **Fallo →** JSON inválido causa error 500 con stack trace.

---

### 28. `test_404_does_not_include_stack_trace` (`test_error_handling.py`)
- **¿Qué testea?** Una ruta inexistente retorna 404 sin traceback, rutas del servidor ni versiones de librerías.
- **ISO 27001 §A.14.2, §A.16.1 — Gestión de incidentes:** No se filtra información interna.
- **Success →** Un atacante no puede hacer reconocimiento del servidor via errores 404.
- **Fallo →** El error 404 revela estructura de directorios, versiones de librerías o stack traces.

### 29. `test_validation_error_returns_422_consistent_format` (`test_error_handling.py`)
- **¿Qué testea?** Datos inválidos retornan error 422 con estructura JSON predecible.
- **ISO 9001 §8.3 — Calidad de diseño:** Los errores de validación son consistentes y procesables.
- **Success →** Los clientes (frontend, apps móviles) pueden parsear errores de forma predecible.
- **Fallo →** Cada error tiene formato diferente, dificultando el manejo en el frontend.

### 30. `test_401_includes_www_authenticate_header` (`test_error_handling.py`)
- **¿Qué testea?** Errores 401 incluyen el header `WWW-Authenticate` según estándar HTTP.
- **ISO 27001 §A.9.2 — Cumplimiento del estándar HTTP:** Los clientes saben cómo autenticarse.
- **Success →** Cumplimiento del estándar HTTP/1.1 para autenticación Bearer.
- **Fallo →** Los clientes no reciben la instrucción de cómo autenticarse.

### 31. `test_api_returns_json_errors_not_html` (`test_error_handling.py`)
- **¿Qué testea?** Todos los errores de la API retornan `Content-Type: application/json`.
- **ISO 9001 §8.3 — Formato de error consistente:** La API es consumible por clientes programáticos.
- **Success →** Frontend y apps móviles pueden procesar errores uniformemente.
- **Fallo →** Algunos errores retornan HTML, rompiendo el parseo en el frontend.

---

### 32. `test_required_env_vars_are_loaded` (`test_secrets_management.py`)
- **¿Qué testea?** Verifica que 9 variables de entorno críticas estén presentes y no vacías.
- **ISO 27001 §A.18.1, ISO 9001 §7.5 — Configuración documentada:** El sistema falla rápidamente si falta configuración esencial.
- **Success →** No hay riesgo de que el sistema funcione con configuraciones incompletas o por defecto inseguras.
- **Fallo →** Falta una variable esencial, el sistema operaría en estado degradado o inseguro.

### 33. `test_jwt_secret_keys_minimum_length` (`test_secrets_management.py`)
- **¿Qué testea?** Verifica que `JWT_ACCESS_SECRET_KEY`, `JWT_REFRESH_SECRET_KEY` y `SECRET_KEY` tengan al menos 32 caracteres (256 bits).
- **ISO 27001 §A.10.1 — Fortaleza criptográfica:** Claves débiles son vectores de ataque.
- **Success →** Las claves HMAC tienen la fortaleza mínima recomendada por NIST.
- **Fallo →** Clave débil que puede ser brute-forced para forjar tokens JWT.

### 34. `test_encryption_algorithm_is_secure` (`test_secrets_management.py`)
- **¿Qué testea?** Verifica que `ENCRYPTION_ALGORITHM` sea HS256, HS384, HS512, RS256 o ES256.
- **ISO 27001 §A.10.1 — Algoritmo criptográfico:** Algoritmos inseguros como `none` o `HS1` no están configurados.
- **Success →** Solo algoritmos seguros están configurados para firmar JWTs.
- **Fallo →** Algoritmo inseguro configurado que permite bypass de firma.

### 35. `test_no_hardcoded_secrets_in_source` (`test_secrets_management.py`)
- **¿Qué testea?** Busca patrones de secretos hardcodeados (passwords, API keys, tokens) en archivos .py.
- **ISO 27001 §A.10.1, §A.18.1 — Gestión de secretos:** Los secretos deben estar en .env, no en el código.
- **Success →** No hay riesgo de exponer credenciales en el repositorio de Git.
- **Fallo →** Se encontró un secreto hardcodeado que debe moverse a variables de entorno.

### 36. `test_database_url_no_env_interpolation` (`test_secrets_management.py`)
- **¿Qué testea?** Verifica que `DATABASE_URL` no contenga patrones de interpolación no resueltos (`$VAR`, `${VAR}`).
- **ISO 27001 §A.10.1 — Integridad de configuración:** La URL de BD está completamente resuelta.
- **Success →** La conexión a BD usa valores reales, no placeholders.
- **Fallo →** La URL contiene `$VAR` sin resolver, la conexión a BD fallaría.

---

### 37. `test_cors_rejects_unknown_origins` (`test_session_security.py`)
- **¿Qué testea?** OPTIONS preflight desde orígenes no autorizados es rechazado.
- **ISO 27001 §A.13.1 — Seguridad de redes (CORS):** Sitios maliciosos no pueden hacer peticiones cross-origin.
- **Success →** Aislamiento de origen contra phishing, XSS y CSRF.
- **Fallo →** Cualquier sitio web externo puede leer datos de la API.

### 38. `test_cors_allows_configured_origins` (`test_session_security.py`)
- **¿Qué testea?** Los orígenes configurados en `WEBSITE_URL` son aceptados.
- **ISO 9001 §8.3 — Funcionalidad:** Los frontends legítimos pueden comunicarse con la API.
- **Success →** El frontend de OppyTalent (Vite/Flutter) funciona sin errores CORS.
- **Fallo →** El frontend no puede conectar con la API.

### 39. `test_server_header_not_exposed` (`test_session_security.py`)
- **¿Qué testea?** El header `Server` no filtra información de tecnología.
- **ISO 27001 §A.14.2 — Fingerprinting:** Versiones de software no se exponen.
- **Success →** Un atacante no puede identificar fácilmente las tecnologías del backend.
- **Fallo →** El servidor revela "uvicorn", "fastapi" o "python".

### 40. `test_login_sets_httponly_cookie` (`test_session_security.py`)
- **¿Qué testea?** La cookie de sesión tiene el flag `HttpOnly`.
- **ISO 27001 §A.9.2, §A.13.1 — Protección contra XSS:** Cookies HttpOnly no son accesibles desde JavaScript.
- **Success →** Un atacante XSS no puede robar el token de sesión via `document.cookie`.
- **Fallo →** Un script malicioso inyectado puede robar el token de autenticación.

---

### 41. `test_password_hashing_argon2id` (`test_utils.py`)
- **¿Qué testea?** Argon2id produce hash con prefijo `$argon2id$`, contraseña correcta verifica, incorrecta no.
- **ISO 27001 §A.10.1 — Controles criptográficos:** Argon2id es el estándar actual más seguro (ganador de la competición Password Hashing).
- **Success →** Contraseñas almacenadas con hash matemáticamente robusto, resistente a GPU/ASIC.
- **Fallo →** El hash no comienza con `$argon2id$`, podría usarse un algoritmo inseguro.

### 42. `test_legacy_bcrypt_compatibility` (`test_utils.py`)
- **¿Qué testea?** Bcrypt hash legacy todavía funciona para verificación, pero marca `needs_rehash=True`.
- **ISO 27001 §A.10.1, §A.12.6 — Migración criptográfica:** Compatibilidad hacia atrás con migración en caliente.
- **Success →** Usuarios legacy pueden login y sus contraseñas se actualizan silenciosamente a Argon2id.
- **Fallo →** Usuarios con contraseñas antiguas no pueden hacer login.

### 43. `test_argon2_hash_does_not_need_rehash` (`test_utils.py`)
- **¿Qué testea?** Un hash Argon2id recién creado no necesita rehash.
- **ISO 9001 §8.1 — Eficiencia operacional:** No hay re-hashing innecesario.
- **Success →** Solo los hashes legacy (bcrypt) se actualizan, no hay sobrecarga para usuarios modernos.
- **Fallo →** Todos los usuarios requerirían rehash en cada login, degradando rendimiento.

---

### 44. `test_settings_environment_is_set` (`test_config_validation.py`)
- **¿Qué testea?** El entorno está configurado como development, test o production.
- **ISO 9001 §7.5 — Información documentada:** El entorno de ejecución está definido.
- **Success →** La aplicación sabe en qué entorno se ejecuta y ajusta su comportamiento.
- **Fallo →** El entorno podría estar mal configurado, afectando seguridad (ej: producción con settings de desarrollo).

### 45. `test_settings_jwt_secrets_not_default` (`test_config_validation.py`)
- **¿Qué testea?** Las claves JWT no son los valores por defecto del código fuente.
- **ISO 27001 §A.10.1 — Gestión de secretos:** Las claves por defecto son peligrosas.
- **Success →** Las claves JWT han sido cambiadas de los valores placeholder.
- **Fallo →** El sistema usa claves JWT conocidas públicamente (del código fuente), permitiendo a cualquiera forjar tokens.

---

### 46. `test_logging_is_configured` (`test_logging_audit.py`)
- **¿Qué testea?** El root logger tiene un nivel configurado.
- **ISO 27001 §A.12.4 — Registro de eventos:** El sistema de logging está activo.
- **Success →** Todos los eventos de seguridad y aplicación pueden ser registrados.
- **Fallo →** El logging no está configurado, eventos críticos no serían registrados.

### 47. `test_user_session_history_tracks_login_logout` (`test_logging_audit.py`)
- **¿Qué testea?** El modelo `UsuarioSessionHistory` tiene campos login_time, logout_time, ip_address, user_agent.
- **ISO 27001 §A.12.4, §A.18.1 — Auditoría de acceso:** Cada sesión de usuario es registrada con metadatos forenses.
- **Success →** Es posible auditar quién, cuándo y desde dónde accedió al sistema.
- **Fallo →** No hay registro de sesiones, imposible auditar accesos no autorizados.

### 48. `test_refresh_tokens_track_ip_and_user_agent` (`test_logging_audit.py`)
- **¿Qué testea?** El modelo `RefreshToken` tiene campos ip_address y user_agent.
- **ISO 27001 §A.12.4 — Registro de eventos de refresh:** Cada renovación de token es trazable.
- **Success →** Se puede detectar si un refresh token está siendo usado desde una IP diferente (posible robo).
- **Fallo →** No hay trazabilidad en la renovación de tokens.

---

### 49. `test_database_engine_has_pool` (`test_connection_pool.py`)
- **¿Qué testea?** El engine de BD tiene un pool de conexiones.
- **ISO 9001 §9.1 — Infraestructura robusta:** El pool de conexiones está habilitado.
- **Success →** Las conexiones a BD son reutilizadas, no creadas/destruidas en cada request.
- **Fallo →** Cada request crea una nueva conexión a BD, degradando rendimiento.

### 50. `test_database_pool_maxsize` (`test_connection_pool.py`)
- **¿Qué testea?** El pool permite al menos 5 conexiones simultáneas.
- **ISO 9001 §9.1 — Escalabilidad:** El pool soporta concurrencia moderada.
- **Success →** Múltiples requests concurrentes pueden acceder a BD sin esperar.
- **Fallo →** Pool demasiado pequeño, requests en cola bajo carga.

---

### 51. `test_cache_set_and_get` (`test_cache_behavior.py`)
- **¿Qué testea?** La función `set_cached_json` intenta escribir en Redis.
- **ISO 9001 §9.1 — Rendimiento:** El sistema de caché está operativo.
- **Success →** Datos frecuentemente accedidos se cachean en Redis, reduciendo carga en BD.
- **Fallo →** La caché no funciona, cada request va a BD (degradación de rendimiento).

### 52. `test_cache_get_returns_none_for_missing` (`test_cache_behavior.py`)
- **¿Qué testea?** `get_cached_json` retorna None para claves inexistentes.
- **ISO 9001 §9.1 — Comportamiento predecible:** La caché maneja misses correctamente.
- **Success →** Cuando un dato no está en caché, el sistema sabe que debe consultar la BD.
- **Fallo →** La caché podría retornar datos corruptos o lanzar excepciones.

### 53. `test_cache_clear_namespace` (`test_cache_behavior.py`)
- **¿Qué testea?** `clear_cache_namespace` intenta limpiar claves por namespace.
- **ISO 27001 §A.9.2 — Aislamiento de caché:** Cuando un usuario modifica datos, la caché se invalida correctamente.
- **Success →** No hay datos obsoletos servidos desde caché después de una actualización.
- **Fallo →** Usuarios podrían ver datos desactualizados después de modificaciones.

---

### 54. `test_models_have_is_active_flag` (`test_resource_cleanup.py`)
- **¿Qué testea?** Todos los modelos heredan de `BaseModel` que tiene `is_active`.
- **ISO 9001 §8.1 — Soft delete:** El sistema soporta borrado lógico.
- **Success →** Los datos no se pierden, solo se marcan como inactivos.
- **Fallo →** El borrado físico podría ocurrir sin posibilidad de recuperación.

### 55. `test_models_have_timestamps` (`test_resource_cleanup.py`)
- **¿Qué testea?** Todos los modelos tienen `created_at` y `updated_at`.
- **ISO 9001 §7.5 — Trazabilidad:** Cada registro tiene metadatos temporales.
- **Success →** Es posible rastrear cuándo se creó y modificó cada registro.
- **Fallo →** No hay trazabilidad temporal de los datos.

---

## Mapeo de Tests vs. ISO 27001:2022 (Anexo A)

| Control ISO 27001 | Tests que lo cubren | Archivos |
|-------------------|---------------------|----------|
| **A.9.2** Gestión de acceso de usuarios | JWT firma inválida, expirado, tampering, sin sub; endpoints protegidos; RBAC | `test_auth_jwt`, `test_authorization_rbac`, `test_dependencies`, `test_session_security` |
| **A.9.3** Responsabilidades de usuario | Roles y permisos RBAC; administración de roles | `test_authorization_rbac` |
| **A.9.4** Control de acceso a sistema | Algorithm none, tokens sin sub, refresh token tracking | `test_auth_jwt`, `test_logging_audit` |
| **A.10.1** Controles criptográficos | Argon2id, bcrypt legacy, clave JWT >= 32 chars, algoritmo HS256 | `test_utils`, `test_secrets_management`, `test_config_validation` |
| **A.12.4** Registro de eventos | Logging config, session history, refresh token IP/UA | `test_logging_audit` |
| **A.12.6** Seguridad en operaciones | Pool conexiones, rate limiting, payload gigante, SQLi | `test_database`, `test_rate_limit`, `test_input_validation`, `test_connection_pool` |
| **A.13.1** Seguridad de redes | CORS orígenes, HTTPS middleware, Server header | `test_main`, `test_https_security`, `test_session_security` |
| **A.13.2** Transferencia de información | CORS headers, HTTPS scheme rewriting, HSTS | `test_main`, `test_https_security` |
| **A.14.2** Seguridad en desarrollo | SQLi, XSS, path traversal, JSON malformed, UUID inválido, 404 sin stack | `test_input_validation`, `test_error_handling`, `test_rate_limit` |
| **A.16.1** Gestión de incidentes | 404 sin stack trace, 500 genérico, errores JSON | `test_error_handling` |
| **A.18.1** Cumplimiento normativo | Env vars presentes, secrets no hardcodeados, logging audit trail | `test_secrets_management`, `test_config_validation`, `test_logging_audit` |

## Mapeo de Tests vs. ISO 9001:2015

| Cláusula ISO 9001 | Tests que lo cubren | Archivos |
|--------------------|---------------------|----------|
| **7.5** Información documentada | Configuración por entorno, settings class, tablas esenciales | `test_config_validation`, `test_database`, `test_secrets_management` |
| **8.1** Planificación operacional | Autoflush disabled, soft delete, timestamps, rehash | `test_config_validation`, `test_resource_cleanup`, `test_database`, `test_utils` |
| **8.3** Diseño y desarrollo | OpenAPI schema, health endpoint, CORS funcional, login tokens, errores consistentes | `test_core`, `test_main`, `test_input_validation`, `test_error_handling`, `test_auth_jwt` |
| **9.1** Seguimiento y medición | Pool conexiones, caché Redis, health check, versión PostgreSQL | `test_connection_pool`, `test_cache_behavior`, `test_core`, `test_database` |

---

## Resumen de Cobertura

| Métrica | Valor |
|---------|-------|
| **Total archivos de test** | 19 (incluyendo conftest.py) |
| **Total funciones de test** | ~55 tests individuales |
| **Controles ISO 27001 cubiertos** | 11 de 14 controles del Anexo A aplicables |
| **Cláusulas ISO 9001 cubiertas** | 4 de 4 cláusulas relevantes para desarrollo |
| **Cobertura de seguridad OWASP Top 10** | SQLi (A03), XSS (A03), Cryptographic Failures (A02), Broken Access Control (A01), Security Misconfiguration (A05) |

## Instrucciones de Ejecución

```bash
# 1. Crear base de datos de tests (una vez)
createdb oppytalent_test

# 2. Configurar ENVIRONMENT=test en .env o via variable de entorno
export ENVIRONMENT=test

# 3. Ejecutar todos los tests
cd OppyTalent-backend
python -m pytest tests/001_core/ -v --asyncio-mode=auto

# 4. Ejecutar tests con reporte de cobertura
python -m pytest tests/001_core/ -v --asyncio-mode=auto --tb=short

# 5. Ejecutar un archivo específico
python -m pytest tests/001_core/test_auth_jwt.py -v --asyncio-mode=auto
```

## Notas Importantes

1. **Base de datos de tests**: Los tests requieren una base de datos PostgreSQL llamada `oppytalent_test` con la misma configuración que `oppytalentDB`.
2. **Redis**: Los tests de caché usan mocks para evitar dependencia de Redis en los tests de CI.
3. **Aislamiento**: Cada sesión de tests crea y destruye tablas, asegurando aislamiento.
4. **Entorno**: Se recomienda `ENVIRONMENT=test` para evitar efectos secundarios en desarrollo.
5. **Claves JWT**: Las claves en `.env` deben tener al menos 32 caracteres para pasar las pruebas de fortaleza criptográfica (ISO 27001 A.10.1).

---

*Documento generado para cumplimiento de ISO 27001:2022 e ISO 9001:2015 — OppyTalent Platform*
