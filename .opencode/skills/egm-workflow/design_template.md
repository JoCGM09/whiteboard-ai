# [Nombre de la Funcionalidad]

* **Autor:** [Nombre o usuario]
* **Estado:** [Borrador | En Revisión Goldfish | Aprobado para Implementación | Implementado]
* **Fecha:** [YYYY-MM-DD]

---

## 1. Problema, Objetivos y Alcance

* **Problema a resolver:** [Descripción directa en 2-4 frases del problema real del usuario o del sistema.]
* **Objetivos (In-Scope):**
  * [Objetivo medible 1]
  * [Objetivo medible 2]
* **No-Objetivos (Out-of-Scope):**
  * [Qué queda explícitamente fuera para evitar sobreingeniería (YAGNI)]

---

## 2. Experiencia de Usuario (UX/UI) e Historias de Usuario

### Historias de Usuario y Viajes Críticos (CUJs)

#### HU-1: [Título de la historia de usuario]
* **Como** [tipo de usuario / actor], **quiero** [acción / objetivo], **para** [beneficio esperado].
* **Dado (Given):** [Estado inicial / precondiciones]
* **Cuando (When):** [Acción del usuario o evento del sistema]
* **Entonces (Then):** [Resultado observable, respuesta visual/CLI/API y postcondición]

### Estados de Interfaz, Ergonomía y Accesibilidad
* **Flujo de interacción / Contratos UI-CLI-API:** [Pantallas, componentes, comandos o endpoints que toca el usuario]
* **Estados límite obligatorios:**
  * *Estado vacío (Empty state):* [Qué ve el usuario cuando no hay datos]
  * *Estado de carga / latencia:* [Feedback visual o de progreso]
  * *Estado de error y recuperación:* [Mensajes claros y accionables ante fallos; cómo se recupera el usuario sin perder trabajo]
* **Accesibilidad y Usabilidad:** [Navegación por teclado, etiquetas/contraste, prevención de acciones destructivas accidentales]

---

## 3. Diseño Técnico y Alternativas Descartadas

### Arquitectura Propuesta
[Explicación en prosa clara de los componentes, flujo de datos, modelos/esquemas y reutilización de utilidades existentes en el repositorio.]

```text
[Diagrama ASCII o Mermaid opcional del flujo de componentes/datos]
```

### Alternativas Descartadas (Obligatorio)
* **Alternativa A ([Nombre]):** Descartada porque [razón técnica concreta: coste, acoplamiento, latencia, complejidad].

---

## 4. Seguridad, Vectores (`V1`–`V7`) y Adaptación Retroactiva

> Referencia obligatoria: `.opencode/skills/egm-workflow/security_vectors.md`

### 4.1. Vectores de Seguridad Clásicos y Mayores Aplicables
* **Superficie activa en esta iteración:** `[ej. API REST + Base de Datos + Auth Multi-Tenant + Subida de Archivos]`
* **Vectores activados (`V1`–`V7`):** `[ej. V1 Control de Acceso/BOLA, V2 Sesiones/Cripto, V3 Inyecciones/Path Traversal, V4 TOCTOU/Negocio, V5 SSRF/Uploads/CORS, V6 DoS/Logs/Timeouts, V7 Supply Chain/LLM]`

| Vector (`V1`–`V7`) | Amenaza Concreta (OWASP / STRIDE / CWE) | Superficie o Dato Afectado | Mitigación Exacta y Archivo Responsable |
| :--- | :--- | :--- | :--- |
| **`V1` Acceso / Autorización** | [BOLA/IDOR, BFLA, Mass Assignment, CORS] | [Endpoint, query o modelo] | [Filtro por `tenant_id`/`user_id`, allowlist DTO en `archivo.ext`] |
| **`V2` Auth / Sesiones / Cripto** | [JWT/Cookies, Argon2id, fuerza bruta, secretos] | [Flujo auth, tokens, `.env`] | [HttpOnly+Secure, comparación constante, rotación en `archivo.ext`] |
| **`V3` Inyecciones / Fronteras** | [SQLi/NoSQLi, XSS, Command Inj, Path Traversal, CSV] | [Inputs externos, rutas, exports] | [Queries parametrizadas, validación de esquema, `realpath` en `archivo.ext`] |
| **`V4` Lógica / TOCTOU / Flujo** | [Condición de carrera, doble gasto, falta idempotencia] | [Pagos, cuotas, estados, webhooks] | [Transacción atómica / bloqueo fila / `Idempotency-Key` en `archivo.ext`] |
| **`V5` Red / SSRF / Archivos** | [SSRF a IPs privadas, CSRF, upload sin magic bytes, CSP] | [Fetch URL, uploads, cabeceras] | [Bloqueo RFC1918/metadata, validación magic bytes en `archivo.ext`] |
| **`V6` DoS / Recursos / Logs** | [Sin paginación/timeout, ReDoS, PII/tokens en logs] | [Listados, llamadas HTTP, logger] | [Tope `limit`, timeout explícito, redacción en logs en `archivo.ext`] |
| **`V7` Supply Chain / IA-LLM** | [Prompt Injection indirecto, salida LLM sin sanitizar, deps] | [Prompts, herramientas agente, lockfile] | [Separación datos/instrucciones, allowlist de tools en `archivo.ext`] |

*(Conserva y completa todas las filas aplicables a la superficie del proyecto; marca `N/A` solo en vectores cuya superficie no exista en absoluto).*

### 4.2. Impacto Retroadaptativo sobre Módulos Ya Construidos (`R1`–`R5`)
> ¿Cómo cambia esta nueva pieza el modelo de amenazas, permisos, estados o fronteras de confianza de lo que YA se armó en iteraciones anteriores? (Si es el diseño inicial `00` desde cero, indica `"Iteración 00 fundacional — fija la línea base en docs/CONTEXT.md"`).

* **Disparos Retroadaptativos Activados (`R1` Auth/Multi-Tenant | `R2` Nueva Entrada Externa | `R3` Nuevo Rol/Estado | `R4` Nuevos Datos Sensibles | `R5` Concurrencia):**
  * **Módulo(s) previo(s) afectado(s):** `[ruta/modulo_anterior.ext]`
  * **Riesgo de regresión si no se adapta:** [Ej. Los endpoints creados en `00` no filtraban por `org_id` o una función interna ahora recibe datos de un webhook externo.]
  * **Adaptación retroactiva obligatoria:** [Cambio exacto que debe incluirse en la sección **5. Plan de Archivos** y en la sección **6. Plan de Pruebas**.]

---

## 5. Plan de Archivos (Regla de Cero Decisiones)

> Ninguna decisión arquitectónica, de UX o de seguridad puede quedar abierta al momento de programar. Enumera todos los archivos que se crearán o modificarán.

1. **`ruta/exacta/archivo1.ext`** (`[Crear | Modificar]`):
   * **Cambios:** [Firmas de funciones/componentes, estructuras de datos, validaciones y lógica exacta a implementar.]
2. **`ruta/exacta/archivo2.ext`** (`[Crear | Modificar]`):
   * **Cambios:** [Descripción precisa del cambio y por qué es necesario.]
3. **`ruta/exacta/test_archivo1.ext`** (`[Crear | Modificar]`):
   * **Cambios:** [Suites y casos de prueba concretos a implementar.]

---

## 6. Plan de Pruebas y Matriz de Verificación (`N1`–`N5` y Playwright)

> Referencia obligatoria: `.opencode/skills/egm-workflow/testing_strategy.md`

### 6.1. Comandos de Verificación por Nivel
* **`N1` Análisis Estático / Tipado / Lint:** `[ej. npm run typecheck && npm run lint | ruff check . && mypy .]`
* **`N2` Tests Unitarios y Valores Frontera:** `[ej. npx vitest run tests/unit | pytest tests/unit]`
* **`N3` Tests de Integración / API / BD:** `[ej. npx vitest run tests/integration | pytest tests/integration]`
* **`N4` Validación E2E / UI con Playwright (si hay interfaz Web):** `[ej. npx playwright test | N/A si es solo CLI/Backend puro]`
* **`N5` Tests de Seguridad (`V1`–`V7`) y Regresión Retroadaptativa (`R1`–`R5`):** `[ej. incluidos en suite de integración/E2E]`

### 6.2. Matriz de Casos de Prueba (Cero Tests Tautológicos)

| ID | Nivel (`N1`–`N5`) | Escenario de Prueba (Acción y Condición) | Historia o Vector Cubierto (`HU-X` / `V1..V7` / `R1..R5`) | Aserción Exacta y Resultado Esperado |
| :--- | :--- | :--- | :--- | :--- |
| **T-1** | `N2` (Unitario) | [Lógica pura + valores frontera: `0`, vacío, máximo, nulo] | `HU-1` (Dominio) | [Retorno o excepción exacta sin mockear la unidad bajo prueba] |
| **T-2** | `N3` (Integración) | [Endpoint/CLI + Persistencia transaccional real/efímera] | `HU-1` (Contrato/BD) | [Status HTTP/CLI exacto + verificación del estado real en BD] |
| **T-3** | `N4` (Playwright) | [Viaje completo en navegador + estado de carga y estado vacío] | `HU-1` (UX Feliz/Vacío) | [`await expect(page.getByRole(...)).toBeVisible()` + 0 errores de consola] |
| **T-4** | `N4` (Playwright) | [Simulación de fallo con `page.route` y recuperación en UI] | `HU-1` (UX Error) | [`getByRole('alert')` visible con mensaje accionable sin perder datos] |
| **T-5** | `N5` (Seguridad) | [Intento de abuso: BOLA/IDOR, inyección, archivo inválido o TOCTOU] | `V1..V7` / `R1..R5` | [Rechazo seguro (`403`/`400`/`422`) sin filtrar trazas ni alterar datos] |
