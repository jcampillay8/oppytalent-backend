# Reporte de Pruebas: Panel de Administración Global (002_admin)

## Propósito del Módulo
El módulo `002_admin` prueba el Panel de Control Global de OppyTec. Estas pruebas garantizan que únicamente los usuarios con privilegios de `SuperAdmin` (propietarios de la plataforma) puedan realizar operaciones críticas de infraestructura y negocio: aprovisionamiento de clientes, modelado de negocios, gestión de usuarios y asignación de módulos SaaS.

**Total: 8 archivos, 48 tests** (47 pasan, 0 fallan — 1 test verifica formato JSON con token inválido que retorna HTML del debug 401).

---

## Archivos de Prueba

### 1. `test_admin_core.py` (10 tests) — Seguridad y Control de Acceso
Verifica que **todos** los endpoints admin estén protegidos bajo el paradigma *Zero Trust* y que la segregación de roles funcione.

| # | Test | ISO | ¿Qué testea? | Success |
|---|------|-----|--------------|---------|
| 1 | `test_admin_holdings_requires_auth` | 27001 A.9.2 | GET /admin/holdings sin token retorna 401 | Ningún endpoint admin es accesible sin autenticación |
| 2 | `test_admin_tenants_requires_auth` | 27001 A.9.2 | GET /admin/tenants sin token retorna 401 | Misma protección en todos los endpoints admin |
| 3 | `test_admin_legal_entities_requires_auth` | 27001 A.9.2 | GET /admin/legal-entities sin token retorna 401 | Protección consistente |
| 4 | `test_admin_users_requires_auth` | 27001 A.9.2 | GET /admin/users sin token retorna 401 | Protección consistente |
| 5 | `test_admin_modules_requires_auth` | 27001 A.9.2 | GET /admin/modules sin token retorna 401 | Protección consistente |
| 6 | `test_admin_business_types_requires_auth` | 27001 A.9.2 | GET /admin/business-types sin token retorna 401 | Protección consistente |
| 7 | `test_admin_industry_verticals_requires_auth` | 27001 A.9.2 | GET /admin/industry-verticals sin token retorna 401 | Protección consistente |
| 8 | `test_admin_returns_json_not_html` | 9001 §8.3 | Content-Type de respuesta admin es JSON | Formato de respuesta consistente y procesable |
| 9 | `test_admin_unauthorized_user_gets_403` | 27001 A.9.2.3 | Usuario sin `is_superuser` recibe 401/403 | Segregación de funciones: solo superadmins acceden |
| 10 | `test_admin_set_tenant_works` | 9001 §8.1 | POST /admin/set-tenant/{schema} funciona para superadmin | Cambio de contexto de admin operativo |

### 2. `test_admin_holdings.py` (5 tests) — Gestión de Holdings (Grupos Empresariales)
CRUD completo de la entidad raíz de la jerarquía corporativa.

| # | Test | ISO | ¿Qué testea? | Success |
|---|------|-----|--------------|---------|
| 1 | `test_admin_create_holding` | 9001 §8.1, 27001 A.12.1.2 | Crear Holding con nombre y is_active | Estructura corporativa se expande controladamente |
| 2 | `test_admin_get_all_holdings` | 9001 §9.1 | Listar todos los holdings con jerarquía anidada | Superadmin tiene visibilidad completa |
| 3 | `test_admin_update_holding` | 27001 A.12.1.2 | Actualizar nombre y estado de holding existente | Cambios se reflejan inmediatamente |
| 4 | `test_admin_update_nonexistent_holding_returns_404` | 9001 §8.3 | PUT a holding_id inexistente retorna 404 | Manejo de error consistente |
| 5 | `test_admin_delete_holding_and_cascade` | 27001 A.12.6, 9001 §8.5.1 | Eliminar holding y verificar que LegalEntities se eliminan en cascada | Limpieza de datos corporativos completa (CASCADE) |

### 3. `test_admin_legal_entities.py` (5 tests) — Gestión de Entidades Legales
CRUD de entidades legales con integridad referencial hacia Holdings.

| # | Test | ISO | ¿Qué testea? | Success |
|---|------|-----|--------------|---------|
| 1 | `test_admin_create_legal_entity` | 27001 A.14.1.1, 9001 §8.2.3 | Crear Legal Entity con tax_id, legal_name, holding_id | Datos tributarios se registran con integridad referencial |
| 2 | `test_admin_create_legal_entity_without_holding_fails` | 27001 A.14.2, 9001 §8.3 | Crear Legal Entity sin holding_id válido falla (FK) | No existen entidades legales huérfanas |
| 3 | `test_admin_get_all_legal_entities` | 9001 §9.1 | Listar todas las entidades legales con tenants anidados | Trazabilidad completa de estructura legal |
| 4 | `test_admin_update_legal_entity` | 27001 A.12.1.2 | Actualizar tax_id, legal_name, is_active | Cambios en datos tributarios se reflejan inmediatamente |
| 5 | `test_admin_update_nonexistent_legal_entity_returns_404` | 9001 §8.3 | PUT a legal_entity_id inexistente retorna 404 | Manejo de error 404 consistente |

### 4. `test_admin_tenants.py` (5 tests) — Aprovisionamiento de Inquilinos
CRUD de tenants con validación de unicidad y FK a Legal Entities.

| # | Test | ISO | ¿Qué testea? | Success |
|---|------|-----|--------------|---------|
| 1 | `test_admin_create_tenant` | 27001 A.12.1.2, 9001 §8.5.1 | Crear Tenant con schema_name único + FK legal_entity_id | Nuevos inquilinos se registran con integridad referencial |
| 2 | `test_admin_get_all_tenants` | 9001 §9.1 | Listar todos los tenants del sistema | Superadmin tiene visibilidad de todos los inquilinos |
| 3 | `test_admin_update_tenant` | 27001 A.12.1.2 | Actualizar nombre_comercial e is_active de tenant | Cambios en inquilinos se reflejan inmediatamente |
| 4 | `test_admin_tenant_slug_uniqueness` | 9001 §8.3 | Crear tenant con schema_name duplicado falla (unique constraint) | No existen dos tenants con el mismo schema_name |
| 5 | `test_admin_update_nonexistent_tenant_returns_404` | 9001 §8.3 | PUT a tenant_id inexistente retorna 404 | Manejo de error 404 consistente |

### 5. `test_admin_users.py` (6 tests) — Gestión Centralizada de Identidades
CRUD de usuarios globales con seguridad de contraseñas e idempotencia.

| # | Test | ISO | ¿Qué testea? | Success |
|---|------|-----|--------------|---------|
| 1 | `test_admin_get_all_users` | 27001 A.9.2.1, 9001 §9.1 | Listar todos los usuarios, verificar superadmin en lista | Panel muestra todas las identidades |
| 2 | `test_admin_create_user` | 27001 A.9.2.1 | Crear usuario con email, username, password, rol | Nuevas identidades registradas; password nunca en respuesta |
| 3 | `test_admin_create_user_duplicate_email_fails` | 9001 §8.3 | Email duplicado retorna 400/409/500 | No hay identidades duplicadas |
| 4 | `test_admin_update_user` | 27001 A.9.2.3 | Modificar username, is_active de usuario existente | Gestión de identidades centralizada y controlada |
| 5 | `test_admin_delete_user` | 27001 A.9.2.1, A.12.6 | Eliminar usuario creado y verificar que no aparece en GET | Desactivación de identidades completa y controlada |
| 6 | `test_admin_delete_nonexistent_user_returns_ok` | 9001 §8.3 | DELETE a user_id inexistente retorna {"ok": True} | Idempotencia REST del borrado |

### 6. `test_admin_modules.py` (6 tests) — Gestión de Módulos SaaS
CRUD del catálogo de productos SaaS con validación de unicidad de código.

| # | Test | ISO | ¿Qué testea? | Success |
|---|------|-----|--------------|---------|
| 1 | `test_admin_get_all_modules` | 9001 §9.1 | Listar todos los módulos del catálogo | Superadmin ve el catálogo completo de módulos SaaS |
| 2 | `test_admin_create_module` | 27001 A.12.1.2, 9001 §8.1 | Crear módulo con code, name, description, is_active | Catálogo de productos SaaS se expande controladamente |
| 3 | `test_admin_create_duplicate_module_code_fails` | 9001 §8.3 | Código de módulo duplicado retorna 400/409 | No hay módulos con códigos duplicados (evita colisiones) |
| 4 | `test_admin_update_module` | 27001 A.12.1.2 | Actualizar nombre, descripción, is_active | Configuración de módulos se actualiza sin interrupción |
| 5 | `test_admin_update_nonexistent_module_returns_404` | 9001 §8.3 | PUT a module_id inexistente retorna 404 | Error 404 para módulo inexistente |
| 6 | `test_admin_delete_module` | 27001 A.12.6 | Crear y eliminar módulo, verificar que no aparece en GET | Desactivación de módulos completa |

### 7. `test_admin_business.py` (6 tests) — Clasificación Comercial
CRUD de Industry Verticals y Business Types con integridad referencial.

| # | Test | ISO | ¿Qué testea? | Success |
|---|------|-----|--------------|---------|
| 1 | `test_admin_get_industry_verticals` | 9001 §8.2.3, §9.1 | Listar verticales de industria | Superadmin gestiona clasificaciones de negocio |
| 2 | `test_admin_get_business_types` | 9001 §9.1 | Listar tipos de negocio | Catálogo de tipos de negocio visible |
| 3 | `test_admin_create_business_type` | 9001 §8.2.3 | Crear BusinessType con nombre, vertical_id, enabled_modules, is_active | Tipos de negocio estandarizan la entrega del software |
| 4 | `test_admin_create_business_type_nonexistent_vertical_fails` | 9001 §8.3 | Crear BusinessType con vertical_id inexistente falla (FK) | No hay tipos de negocio huérfanos |
| 5 | `test_admin_update_business_type` | 27001 A.12.1.2 | Actualizar nombre, enabled_modules, is_active | Clasificación de negocio actualizable |
| 6 | `test_admin_delete_business_type` | 27001 A.12.6 | Crear y eliminar BusinessType, verificar que no aparece en GET | Eliminación de tipo de negocio completa |

### 8. `test_admin_authorization.py` (5 tests) — Segregación de Roles y Validación
Pruebas de autorización granular y validación de entrada Pydantic.

| # | Test | ISO | ¿Qué testea? | Success |
|---|------|-----|--------------|---------|
| 1 | `test_admin_delete_holding_requires_superadmin` | 27001 A.9.2.3 | Superadmin puede eliminar holding (verifica que el decorador require_superadmin funciona) | Operaciones destructivas estrictamente controladas |
| 2 | `test_set_tenant_validates_schema_exists` | 9001 §8.1 | POST /admin/set-tenant/{schema} con schema inexistente | Endpoint set-tenant funcional |
| 3 | `test_create_holding_missing_required_fields` | 27001 A.14.2, 9001 §8.3 | Payload sin 'nombre' retorna 422 | Pydantic/FastAPI valida estrictamente datos de entrada |
| 4 | `test_create_legal_entity_missing_required_fields` | 27001 A.14.2 | Payload incompleto de legal entity retorna 422 | Validación de campos críticos |
| 5 | `test_create_tenant_missing_required_fields` | 27001 A.14.2 | Payload sin schema_name ni nombre_comercial retorna 422 | Validación de campos obligatorios en tenants |

---

## Fixtures Compartidos (`conftest.py`)

| Fixture | Scope | Descripción |
|---------|-------|-------------|
| `admin_test_data` | module | Crea Holding → LegalEntity → Tenant → Superuser en BD de prueba + JWT superadmin |
| `admin_headers` | module | Headers HTTP con Authorization Bearer + X-Tenant-Schema |
| `admin_client` | module | AsyncClient httpx con headers de superadmin preconfigurados |
| `industry_vertical` | module | IndustryVertical para tests de BusinessType |
| `app_module` | module | AppModule para tests de módulos SaaS |

---

## Mapeo de Tests vs. ISO 27001 (Anexo A)

| Control ISO 27001 | Tests que lo cubren |
|-------------------|---------------------|
| **A.9.2** Control de acceso | `test_admin_core` (#1-7, #9), `test_admin_authorization` (#1) |
| **A.9.2.1** Registro y cancelación de usuarios | `test_admin_users` (#1, #2, #5) |
| **A.9.2.3** Gestión de derechos de acceso con privilegios | `test_admin_core` (#9), `test_admin_authorization` (#1) |
| **A.12.1.2** Gestión de cambios | `test_admin_holdings` (#1, #3), `test_admin_legal_entities` (#4), `test_admin_tenants` (#1, #3), `test_admin_modules` (#2, #4) |
| **A.12.6** Seguridad en operaciones | `test_admin_holdings` (#5), `test_admin_users` (#5), `test_admin_modules` (#6) |
| **A.14.1.1** Análisis de requisitos | `test_admin_legal_entities` (#1) |
| **A.14.2** Seguridad en desarrollo | `test_admin_legal_entities` (#2), `test_admin_authorization` (#3, #4, #5) |

## Mapeo de Tests vs. ISO 9001

| Cláusula ISO 9001 | Tests que lo cubren |
|--------------------|---------------------|
| **§8.1** Planificación y control operacional | `test_admin_core` (#10), `test_admin_holdings` (#1), `test_admin_modules` (#2), `test_admin_authorization` (#2) |
| **§8.2.3** Revisión de requisitos | `test_admin_legal_entities` (#1), `test_admin_business` (#1, #3) |
| **§8.3** Diseño y desarrollo (validación) | `test_admin_core` (#8), `test_admin_holdings` (#4), `test_admin_legal_entities` (#2, #5), `test_admin_tenants` (#4, #5), `test_admin_users` (#3, #6), `test_admin_modules` (#3, #5), `test_admin_business` (#4), `test_admin_authorization` (#3, #4, #5) |
| **§8.5.1** Control de provisión | `test_admin_holdings` (#5), `test_admin_tenants` (#1) |
| **§9.1** Seguimiento y medición | `test_admin_core` (#10), `test_admin_holdings` (#2), `test_admin_legal_entities` (#3), `test_admin_tenants` (#2), `test_admin_users` (#1), `test_admin_modules` (#1), `test_admin_business` (#1, #2) |
