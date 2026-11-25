# Catálogo de Estrategia de Pruebas (`N1`–`N5`), Calidad de Código y Validación con Playwright

Este documento es la referencia obligatoria para **El Elefante** (`elephant`) y el **Goldfish de Pruebas** (`goldfish-testing`) durante `/design`, `/review`, `/audit` y `/context`.

---

## Parte 1: Los 5 Niveles de Verificación y Testing (`N1` – `N5`)

### `N1` — Análisis Estático, Tipado y Calidad de Código (Static & Code Verification)
* **Objetivo:** Detectar errores de tipos, contratos rotos, código muerto, variables no usadas y complejidad excesiva antes de ejecutar un solo test dinámico.
* **Herramientas estándar según stack:**
  * *TypeScript / JS:* `tsc --noEmit`, `eslint`, `biome check`.
  * *Python:* `pyrefly` / `pyright` / `mypy`, `ruff check`.
  * *Rust / Go:* `cargo check`, `cargo clippy -- -D warnings`, `go vet`, `golangci-lint`.
* **Invariantes que audita `goldfish-testing`:**
  * Prohibido silenciar errores de tipos o linter con `@ts-ignore`, `any` injustificado o `# type: ignore` sin comentario técnico que lo justifique.
  * El comando de verificación estática debe estar definido explícitamente en la sección **6. Plan de Pruebas**.

### `N2` — Testing Unitario y de Lógica de Dominio (Unit & Boundary Testing)
* **Objetivo:** Verificar en milisegundos y con determinismo total (`100%` reproducible sin red, sin disco real y sin depender de la hora del sistema) toda la lógica de negocio, cálculos, máquinas de estados, parsers y validadores.
* **Herramientas estándar:** `vitest`, `jest`, `pytest`, `cargo test`, `go test`.
* **Invariantes que audita `goldfish-testing`:**
  * **Cobertura de Valores Frontera (*Boundary Value Analysis*):** Todo test unitario debe cubrir caso feliz + valores límite (`0`, `-1`, vacío `""`/`[]`, `null`/`undefined`, longitud máxima, caracteres especiales/Unicode).
  * **Regla de Oro de Mocks (Anti-Tautología):** Solo se permite usar *mocks/stubs* en fronteras externas (reloj del sistema, APIs de terceros, pasarelas de pago, correo). **Está estrictamente prohibido mockear la clase o función interna que es objeto de la prueba** (*Mock-testing-Mock* = `[BLOQUEANTE]`).
  * **Aserciones Exactas:** Prohibidas las aserciones débiles (`assert res is not None`, `expect(result).toBeDefined()`). Se debe verificar el valor, estado o excepción exacta producida.

### `N3` — Testing de Integración, Contratos de API y Persistencia (Integration & Contract Testing)
* **Objetivo:** Probar que los módulos ensamblados funcionan juntos de verdad: rutas HTTP/CLI, middlewares, validación de esquemas (Zod/Pydantic), transacciones de base de datos y serialización de respuestas.
* **Herramientas estándar:** `supertest`, `httpx` / `FastAPI TestClient`, `pytest` con BD efímera/transaccional (SQLite in-memory, Testcontainers o rollback por test).
* **Invariantes que audita `goldfish-testing`:**
  * Verifica códigos de estado reales (`200`, `201`, `400`, `401`, `403`, `404`, `409`, `422`), estructura exacta del payload JSON y efectos reales en la base de datos (que el registro realmente se creó, actualizó o hizo rollback ante fallo).
  * Cada test debe limpiar o aislar su estado (transacción con rollback o base limpia) para evitar *flaky tests* dependientes del orden de ejecución.

### `N4` — Validación End-to-End (E2E) y de Interfaz Real con Playwright (`@playwright/test`)
* **Objetivo:** Cuando el proyecto tiene interfaz Web / Frontend / Fullstack, validar los **Viajes Críticos de Usuario (CUJs / Historias `Dado-Cuando-Entonces`)** en un navegador headless real (`chromium`, `firefox`, `webkit`) con **Playwright**.
* **Invariantes de Playwright que audita `goldfish-testing`:**
  1. **Selectores Semánticos y de Accesibilidad (Prohibido CSS frágil):**
     - Exigir el uso de locators centrados en el usuario: `page.getByRole()`, `page.getByLabel()`, `page.getByPlaceholder()`, `page.getByText()` (o `page.getByTestId()` solo cuando no aplique un rol semántico).
     - Marcar como `[IMPORTANTE]` el uso de selectores acoplados al DOM interno (ej. `page.locator('div.card > span:nth-child(2)')`).
  2. **Verificación de la Tríada de Estados UX en Navegador Real:**
     - **Estado Vacío (*Empty State*):** Verificar qué renderiza la pantalla cuando no hay datos iniciales.
     - **Estado de Carga / Transición:** Verificar que durante la petición el botón se deshabilita o muestra indicador de carga (previniendo doble envío).
     - **Estado de Error y Recuperación:** Simular fallo de validación o error de red (`page.route('**/api/**', route => route.fulfill({ status: 500 }))`) y verificar con `await expect(page.getByRole('alert')).toBeVisible()` que el usuario recibe un mensaje claro y puede reintentar sin perder sus datos.
  3. **Web-First Assertions y Cero `waitForTimeout` Arbitrarios (`[BLOQUEANTE]`):**
     - Prohibido usar `page.waitForTimeout(2000)` o `sleep()`. Toda espera debe basarse en aserciones auto-reintentables de Playwright (`await expect(locator).toBeVisible()`, `await expect(page).toHaveURL()`, `page.waitForResponse()`).
  4. **Vigilancia de Errores Silenciosos de Consola y Página:**
     - Los tests de Playwright deben escuchar `page.on('pageerror', ...)` y errores críticos de consola o respuestas `500` inesperadas para que ningún fallo JS silencioso pase desapercibido.

### `N5` — Testing de Seguridad, Abuso y Regresión Retroadaptativa (AppSec & Retro-Regression)
* **Objetivo:** Demostrar empíricamente que las mitigaciones de seguridad (`V1`–`V7`) y las adaptaciones retroactivas (`R1`–`R5`) funcionan frente a entradas hostiles.
* **Invariantes que audita `goldfish-testing`:**
  * **Pruebas Negativas de Seguridad (`V1`–`V7`):**
    - Si aplica `V1` (BOLA/IDOR / Roles): Test donde el `Usuario A` intenta leer/editar/borrar el recurso del `Usuario B` (o un rol básico invoca ruta de `admin`) y verifica respuesta `403` o `404` sin modificar la BD.
    - Si aplica `V3` (Inyección / Path Traversal / CSV): Test que envía payloads maliciosos (`../.env`, `<script>`, `' OR 1=1--`, `=CMD|...`) y verifica rechazo o sanitización segura.
    - Si aplica `V4` (Condición de Carrera / TOCTOU): Test que lanza `N` peticiones simultáneas (`Promise.all` / `asyncio.gather`) contra un recurso limitado (cupón, saldo, stock) y verifica que solo una tenga éxito.
  * **Tests de Regresión Retroadaptativa (`R1`–`R5`):**
    - Cuando una nueva funcionalidad activa un disparo retroadaptativo sobre módulos previos, la suite de tests de esos módulos anteriores debe ampliarse y ejecutarse para confirmar que cumplen la nueva restricción sin romper su funcionalidad original.

---

## Parte 2: Matriz de Activación Retroadaptativa de Pruebas (Según lo que se va Armando)

El Elefante y `goldfish-testing` determinan qué niveles `N1`–`N5` son obligatorios en cada iteración según las piezas que existen o se agregan al proyecto:

| Tipo de Componente o Iteración que se Está Armando | Niveles Obligatorios en Diseño (`/review`) y Código (`/audit`) |
| :--- | :--- |
| **Librería, Algoritmo, Parser o Utilidad Interna** | **`N1`** (Tipado/Lint) + **`N2`** (Unitarios + Valores Frontera) + **`N5`** (Inputs malformados / ReDoS). |
| **CLI (Herramienta de Línea de Comandos)** | **`N1`** + **`N2`** (Lógica desacoplada) + **`N3`** (Ejecución de comandos CLI con argumentos válidos, inválidos, `--help` y códigos de salida) + **`N5`** (Path Traversal / Command Injection). |
| **API Backend / Microservicio / Base de Datos** | **`N1`** + **`N2`** (Servicios/Dominio) + **`N3`** (Endpoints HTTP + Transacciones BD reales/efímeras) + **`N5`** (BOLA/IDOR, Auth, SQLi, TOCTOU, Rate Limit y Regresión `R1`–`R5`). |
| **Frontend Web / Aplicación Fullstack (UI en Navegador)** | **`N1`** + **`N2`** (Hooks/Estado/Utils) + **`N3`** (API/Contratos) + **`N4` (Playwright E2E validando Historias `HU-X`, accesibilidad `getByRole` y estados vacío/carga/error)** + **`N5`** (XSS, CSRF, rutas protegidas). |
