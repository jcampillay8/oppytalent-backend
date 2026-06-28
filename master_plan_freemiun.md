# Plan Maestro: Estrategia B2C Freemium & Product-Led Growth (PLG)

## 1. Visión General de la Estrategia
El objetivo principal de esta estrategia es utilizar el inmenso valor de OppyTalent (El Asistente IA 24/7 y la capacidad de parsear un CV en segundos) como el principal motor de crecimiento de la plataforma. 

En lugar de cobrar a los usuarios B2C con dinero, se cobrará con **"Moneda Social" (Likes, Reseñas, Referidos)**. Esto crea un ciclo viral impulsado por el producto, garantizando cero fricción inicial (Zero Time-To-Value) y usando el Efecto Dotación para motivar a los usuarios a mejorar de nivel.

## 2. Definición de Niveles Freemium (Tiers)

### Nivel 1: Freemium Básico (Por Defecto)
* **Objetivo:** Enganchar al usuario permitiéndole probar la magia de la plataforma.
* **Mochila Base (Créditos IA):** 30 por mes.
* **Skills Permitidos:** 0 (La IA no se especializa).
* **Portafolio:** Escaneo ilimitado, pero **solo permite editar los primeros 3 elementos** de cada categoría (Proyectos, Experiencias, Estudios, etc.).

### Nivel 2: Freemium Pro
* **Misión de Desbloqueo:** Dar 1 "Like" o "Seguir" en LinkedIn (Muy baja fricción).
* **Mochila Base (Créditos IA):** 40 por mes.
* **Skills Permitidos:** 2.
* **Portafolio:** Permite editar hasta **4 elementos** por categoría.

### Nivel 3: Freemium Premium
* **Misión de Desbloqueo:** Escribir una reseña/testimonio real dentro de la plataforma (Se usa para Marketing).
* **Mochila Base (Créditos IA):** 50 por mes.
* **Skills Permitidos:** 3.
* **Portafolio:** Permite editar hasta **6 elementos** por categoría.

### Nivel 4: Freemium Embajador
* **Misión de Desbloqueo:** El usuario invita a colegas usando su enlace de referido.
* **Premio Consumible:** **+50 Créditos Bono** por CADA referido que se cree una cuenta.
* **Premio Permanente (Basta con 1 referido exitoso):** 
  * **Skills Permitidos:** Sube a 5 para siempre.
  * **Portafolio:** Permite editar hasta **10 elementos** por categoría para siempre.

---

## 3. Lógica del Sistema de Créditos (La Doble Bolsa)

El sistema de créditos operará con dos "bolsas" independientes para proteger los beneficios ganados por el usuario y crear un sentido de justicia:

1. **Bolsa de Créditos Base (Mensuales):** 
   * Está atada al Nivel (Tier) del usuario (30, 40 o 50).
   * **Se resetea a tope el día 1 de cada ciclo mensual**. No se acumulan si no se usan.
2. **Bolsa de Créditos Bono (Acumulables):**
   * Son ganados exclusivamente a través de referencias (+50 por referido).
   * **No caducan nunca y se acumulan infinitamente.**
   * **Lógica de consumo:** La plataforma SIEMPRE descontará primero de la "Bolsa Base". Solo cuando la Bolsa Base llegue a 0 en el mes actual, comenzará a consumir los Créditos Bono. Al mes siguiente, la Bolsa Base se recarga, protegiendo los Créditos Bono restantes.

---

## 4. Experiencia de Usuario (UI/UX) y El "Embudo"

* **El Momento "Wow" (Sin restricción de subida):** Cuando el usuario arrastra su PDF para escanear, el sistema debe parsear e ingresar el 100% de la información (aunque tenga 12 experiencias laborales). El usuario verá su portafolio gigante e impecable.
* **Aplicación de Límites (Los Candados):** En la interfaz del portafolio, las tarjetas de elementos que superen el límite del plan actual (por ejemplo, de la 4ta experiencia en adelante para un usuario Básico) mostrarán su información en modo solo lectura, y el botón de "Editar" tendrá un ícono de **Candado (🔒)**. Los botones para "Añadir Nuevo Manualmente" también tendrán el candado si ya superaron el límite.
* **El Pop-up de Gamificación:** Al hacer clic en un Candado, se abrirá un Modal estilizado que diga:
  > *"¡Qué gran trayectoria! Tu plan te permite editar hasta X elementos. Desbloquea la capacidad de edición completando esta rápida misión sin costo."* (Con botones claros a las misiones).
* **UI de Créditos:** El Dashboard (Sidebar o Navbar) debe mostrar un indicador tipo batería o barra de progreso separando claramente los Créditos del Mes de los Créditos de Reserva (Bono).

---

## 5. Implementación Técnica (Paso a Paso)

### Fase 1: Base de Datos (Backend - SQLAlchemy)
Modificar el modelo `User` para soportar la economía Freemium:
* `freemium_tier`: Enum (`BASIC`, `PRO`, `PREMIUM`, `AMBASSADOR`). Default: `BASIC`.
* `base_credits_balance`: Integer. (Se reinicia mes a mes).
* `bonus_credits_balance`: Integer. (Nunca caduca).
* `credit_cycle_start_date`: DateTime. (Para calcular cuándo resetear los créditos base).
* `has_liked_linkedin`: Boolean.
* `has_left_review`: Boolean.
* `referral_code`: String (Único para cada usuario, generado al registrarse).
* `referred_by_id`: ForeignKey (Si un usuario entra invitado, guardar quién lo invitó para darle el bono).

### Fase 2: Lógica del Ciclo de Créditos (Backend)
* **Consumo (Chat API):**
  Modificar el endpoint del chat IA. Antes de responder:
  1. Si `base_credits_balance > 0`, restar 1.
  2. Si no, si `bonus_credits_balance > 0`, restar 1.
  3. Si ambas están en 0, devolver error (HTTP 402 Payment Required / Forbidden) con mensaje claro: "Sin créditos".
* **Reseteo Mensual:**
  Existen dos opciones: 
  * Un cronjob/worker que corra a medianoche y actualice el `base_credits_balance` de todos los usuarios cuyo ciclo de 30 días se haya cumplido.
  * *Mejor enfoque (Lazy Evaluation)*: Cada vez que el usuario intenta gastar un crédito, se revisa su `credit_cycle_start_date`. Si la fecha de hoy supera en un mes a la fecha guardada, se le resetea el saldo base, se actualiza la fecha, y se efectúa el cobro. Esto ahorra procesamiento.

### Fase 3: Validadores de Edición en APIs (Backend)
* Crear una función utilitaria `check_portfolio_limit(user_id, category_type)`.
* Antes de hacer un `UPDATE` o `INSERT` en Proyectos, Experiencias, etc., el endpoint llamará a esta función.
* La función revisa cuántos elementos de esa categoría tiene el usuario y lo compara con el límite de su `freemium_tier`.
* Si intenta editar el elemento en la posición "4" (ordenados cronológicamente) y su límite es 3, lanzará un error HTTP 403 Forbidden. *(Nota: Siempre permitir el DELETE).*

### Fase 4: Integración Visual y Componentes (Frontend)
* **Stores Pinia:** Actualizar el store de autenticación para descargar y reaccionar a los nuevos datos (`tier`, `base_credits`, `bonus_credits`, `referral_code`).
* **Componente de Bloqueo (`FeatureLock.vue`):** Un componente tipo "Wrapper" que envuelva botones (como el de Editar). Si la condición de bloqueo se cumple, deshabilita el click real y abre el **UpgradeModal**.
* **Modal de Misiones (`UpgradeModal.vue`):** Una ventana atractiva que ofrezca las opciones de "Dar Like" o "Dejar Reseña", conectadas a endpoints simples en el backend que actualicen el estado y recarguen los límites.
* **Componente de Referidos:** Una pestaña nueva en el Dashboard donde el usuario pueda copiar su link único de invitación (`oppytalent.com/register?ref=AB123`) y ver cuántos Créditos Bono ha ganado históricamente.

---
*Documento creado para la planificación estratégica y técnica del sistema Freemium.*
