# Catálogo de Vectores de Seguridad (Mayores y Clásicos) + Motor Retroadaptativo

Este documento es la referencia obligatoria para **El Elefante** (`elephant`) y el **Goldfish de Seguridad** (`goldfish-security`) durante `/design`, `/review`, `/audit` y `/context`.

---

## Parte 1: Los 7 Vectores de Seguridad Mayores y Clásicos (`V1` – `V7`)

### `V1` — Control de Acceso, Autorización y Aislamiento (OWASP A01 / CWE-284, CWE-639)
* **BOLA / IDOR (Broken Object Level Authorization):** Acceso, modificación o borrado de registros cambiando un `id` en la URL/payload sin verificar en servidor que el recurso pertenece al usuario o a su organización (*tenant*).
* **BFLA (Broken Function Level Authorization):** Endpoints administrativos, acciones internas o mutaciones invocables por usuarios con roles inferiores o no autenticados.
* **Escalada de Privilegios y Mass Assignment (CWE-915):** Aceptar directamente del payload del cliente campos privilegiados (`role`, `isAdmin`, `orgId`, `plan`, `balance`, `permissions`) sin lista blanca (*allowlist*) explícita en el DTO/esquema.
* **Bypass de Rutas y CORS:** Middlewares de autorización aplicados solo en algunas rutas o métodos HTTP; CORS configurado con `Access-Control-Allow-Origin: *` o reflejando el header `Origin` junto con `Allow-Credentials: true`.

### `V2` — Autenticación, Sesiones, Criptografía y Secretos (OWASP A02, A07 / CWE-287, CWE-798)
* **Gestión de Tokens y JWT:** Aceptar algoritmo `none`, confusión `RS256`/`HS256`, secretos de firma débiles, tokens sin expiración (`exp`) corta, sin rotación de *refresh tokens* ni mecanismo de revocación ante logout o compromiso.
* **Seguridad de Cookies y Sesiones:** Cookies de sesión sin banderas `HttpOnly`, `Secure` y `SameSite=Lax|Strict`; fijación de sesión (*Session Fixation*) al no regenerar el ID tras autenticarse.
* **Almacenamiento de Credenciales y Criptografía:** Contraseñas sin hash adaptativo fuerte (`Argon2id`, `bcrypt`, `scrypt`); uso de algoritmos rotos (`MD5`, `SHA1`, `ECB`); generación de tokens/códigos con PRNG no criptográfico (`Math.random()`, `random.random()`); comparación de firmas/tokens sin tiempo constante (`hmac.compare_digest` / `crypto.timingSafeEqual`).
* **Fuerza Bruta y Exposición de Secretos:** Ausencia de bloqueo/backoff en login, recuperación de contraseña o códigos OTP/Magic Link; enumeración de usuarios por diferencias en mensajes o tiempos de respuesta; claves o `.env` hardcodeados en código o historial Git.

### `V3` — Inyecciones y Validación en Fronteras de Confianza (OWASP A03 / CWE-79, CWE-89, CWE-78, CWE-22)
* **SQL / NoSQL / ORM Injection:** Interpolación o concatenación de strings en consultas SQL, filtros dinámicos (`$where`, operadores JSON/NoSQL inyectados en objetos de query) o `orderBy` sin lista blanca.
* **OS Command & Code Injection:** Uso de `shell=True`, `os.system`, `child_process.exec`, `eval()`, `Function()` o interpolación de argumentos de usuario en comandos de sistema.
* **XSS (Cross-Site Scripting) y SSTI:** Renderizado de HTML/Markdown sin sanitizar (`innerHTML`, `dangerouslySetInnerHTML`, `v-html`), URLs con esquema `javascript:` o `data:`, e inyección de plantillas en servidor (SSTI).
* **Path Traversal y Manipulación de Archivos (CWE-22):** Construcción de rutas de archivo con entrada de usuario sin resolver la ruta real (`realpath` / `resolve`) ni verificar que permanezca estrictamente dentro del directorio base permitido, o seguimiento inseguro de enlaces simbólicos (*symlinks*).
* **Inyección en Exportaciones y Deserialización (CSV / XXE / Pickle):** *CSV Formula Injection* (celdas que inician con `=`, `+`, `-`, `@`, `\t`, `\r`); parseo XML con entidades externas habilitadas (XXE); deserialización de formatos ejecutables (`pickle`, `yaml.load` sin `SafeLoader`, `unserialize`).

### `V4` — Lógica de Negocio, Integridad de Flujo y Condiciones de Carrera (OWASP A04, A08 / CWE-362, CWE-840)
* **Condiciones de Carrera / TOCTOU (Time-of-Check to Time-of-Use):** Peticiones concurrentes que leen un estado (saldo, stock, cupón de un solo uso, límite de cuota) antes de que la primera petición actualice el valor, permitiendo doble gasto o superar límites por falta de transacciones atómicas, `SELECT ... FOR UPDATE` o restricciones `UNIQUE` en base de datos.
* **Manipulación de Flujo y Estado:** Saltarse pasos obligatorios en flujos multi-etapa (ej. confirmar pedido sin pasar por validación de pago o MFA); confiar en precios, descuentos o estados calculados en el frontend.
* **Falta de Idempotencia y Replay Attacks:** Webhooks o transacciones financieras sin clave de idempotencia (`Idempotency-Key`), sin validación de firma criptográfica (`HMAC`) o sin ventana de timestamp para impedir ataques de repetición (*replay*).

### `V5` — Red, SSRF, Subida de Archivos y Configuración (OWASP A05, A10 / CWE-918, CWE-434, CWE-352)
* **SSRF (Server-Side Request Forgery):** El servidor descarga URLs, webhooks, avatares o PDFs proporcionados por el usuario sin bloquear rangos internos (`127.0.0.0/8`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.169.254` de metadatos cloud, `::1`) ni validar redirecciones HTTP posteriores.
* **CSRF (Cross-Site Request Forgery):** Peticiones que mutan estado basadas en cookies sin token anti-CSRF o validación estricta de `Origin`/`Referer`.
* **Subida de Archivos Insegura (Unrestricted File Upload):** Confiar solo en la extensión o `Content-Type` del cliente sin verificar *magic bytes*, tamaño máximo, renombrado con UUID, almacenamiento fuera de la raíz pública y cabecera `Content-Disposition: attachment` / `X-Content-Type-Options: nosniff`.
* **Cabeceras y Superficie de Depuración:** Ausencia de `Content-Security-Policy (CSP)`, `Strict-Transport-Security (HSTS)`, `X-Frame-Options`; modos `DEBUG=True`, introspección GraphQL abierta o rutas `/metrics`/`/admin` expuestas en producción.

### `V6` — Disponibilidad (DoS), Límites de Recursos y Observabilidad Segura (OWASP A09 / CWE-400, CWE-532)
* **Agotamiento de Recursos y DoS Algorítmico:** Consultas a base de datos o APIs sin paginación ni tope máximo (`limit`); carga de archivos completos en RAM en vez de *streaming*; expresiones regulares vulnerables a *catastrophic backtracking* (ReDoS); payloads JSON/multipart sin límite de bytes ni profundidad de anidamiento.
* **Ausencia de Timeouts y Rate Limiting:** Llamadas HTTP/DB/cola externas sin `timeout` explícito (que bloquean *workers* indefinidamente); endpoints costosos sin *rate limiting* por IP/usuario.
* **Fuga de Información en Logs y Errores (CWE-532, CWE-209):** Imprimir contraseñas, tokens, cabeceras `Authorization`, tarjetas o PII en logs; devolver *stack traces*, consultas SQL o rutas internas del servidor en respuestas HTTP de error.
* **Falta de Trazabilidad de Seguridad (Audit Trail):** Operaciones sensibles (inicio de sesión fallido, cambio de rol/contraseña, exportación masiva, borrado de cuenta) que no quedan registradas con actor, timestamp y resultado.

### `V7` — Cadena de Suministro y Seguridad de IA / LLMs (OWASP A06 & OWASP LLM01–LLM10)
* **Seguridad de Dependencias y Supply Chain:** Instalación de paquetes innecesarios o no auditados, ausencia de archivo de bloqueo (*lockfile*), scripts post-install arbitrarios o vulnerabilidades conocidas (CVEs).
* **Prompt Injection Directo e Indirecto (LLM01):** Concatenar texto no confiable (documentos, correos, páginas web, inputs de usuario) dentro de instrucciones del sistema permitiendo que el contenido secuestre el flujo del agente.
* **Manejo Inseguro de Salidas del Modelo (LLM02):** Ejecutar código, consultas SQL, comandos bash o renderizar HTML generado por un LLM sin sanitización ni validación estructural previa.
* **Agencia Excesiva y Denial of Wallet (LLM08, LLM10):** Dar a un agente herramientas destructivas o de escritura/red sin confirmación ni lista blanca de permisos; llamadas a modelos sin límite de tokens, presupuesto o concurrencia.

---

## Parte 2: Motor de Seguridad Retroadaptativa (En Función de lo que se va Armando)

La seguridad de un proyecto **no es estática**: cada vez que se añade una pieza nueva en la iteración `N`, **cambia el modelo de amenazas de las piezas construidas en las iteraciones `0 .. N-1`**.

El Elefante y los Goldfish deben ejecutar siempre el **Análisis Retroadaptativo en 3 pasos**:

### Paso 1: Detección de Superficie Acumulada y Activación de Vectores
A medida que el proyecto crece, se activan dinámicamente los vectores obligatorios según las capacidades presentes:

| Qué se está armando o ya existe en el proyecto | Vectores que se Activan Automáticamente |
| :--- | :--- |
| **Esqueleto inicial / CLI / Librería local** | `V3` (Validación de entradas, Path Traversal, Command Injection), `V6` (Límites de memoria/ReDoS, errores limpios), `V7` (Dependencias mínimas con lockfile). |
| **Base de Datos / Persistencia** | `V3` (SQL/NoSQL Injection), `V4` (Transacciones atómicas, constraints UNIQUE), `V6` (Paginación obligatoria, índices, timeouts de conexión). |
| **API Web / Frontend / Formularios** | `V3` (XSS, validación de esquemas), `V5` (CORS, CSP, HSTS, CSRF), `V6` (Límite de tamaño de payload, Rate Limiting). |
| **Autenticación / Usuarios / Sesiones** | `V1` (Guardas de ruta), `V2` (Argon2id/bcrypt, JWT/Cookies seguras, fuerza bruta, anti-enumeración), `V6` (Redacción de tokens/passwords en logs + Audit Trail). |
| **Multi-Usuario / Roles / Organizaciones (Multi-Tenant)** | `V1` (**BOLA/IDOR obligatorio en cada query**, BFLA por rol, prohibición de Mass Assignment), `V4` (Aislamiento transaccional por tenant). |
| **Subida/Descarga de Archivos o Exportaciones (CSV/PDF)** | `V3` (Path Traversal, CSV Formula Injection, XXE), `V5` (Magic bytes, UUID filename, almacenamiento fuera de webroot, `nosniff`), `V6` (Streaming, cuota de disco). |
| **Pagos, Créditos, Cupones, Inventario o Cuotas** | `V4` (**Condiciones de carrera / TOCTOU con bloqueo atómico**, idempotencia, validación de importes en servidor, firma HMAC de webhooks). |
| **Webhooks Salientes, Scrapers o Fetch de URLs** | `V5` (**Protección SSRF** bloqueando IPs privadas/metadatos cloud y re-validando en redirecciones), `V6` (Timeouts estrictos y Circuit Breaker). |
| **Agentes IA / LLMs / RAG** | `V7` (**Prompt Injection indirecto**, validación de salida del LLM antes de ejecutar/renderizar, permisos mínimos en herramientas, tope de tokens/coste). |

### Paso 2: Reglas de Disparo Retroadaptativo (Cómo lo nuevo obliga a adaptar lo ya construido)

Cada vez que una nueva funcionalidad introduce un cambio arquitectónico, **`/design` debe incluir en el Plan de Archivos los ajustes retroactivos sobre los módulos anteriores**, y **`/review` + `/audit` deben verificar que ningún módulo viejo haya quedado desprotegido**:

1. **Disparo R1 — "De Abierto/Monousuario a Autenticado o Multi-Tenant"**:
   - *Cuando:* Se añade autenticación, roles o soporte de múltiples equipos/organizaciones a un proyecto que ya tenía endpoints, tablas o vistas creadas en fases previas.
   - *Adaptación Retroactiva Obligatoria:* Todos los endpoints, consultas a BD y tests de las fases previas deben actualizarse para exigir sesión válida y filtrar por `user_id` / `tenant_id` (prevención retroactiva de BOLA/IDOR y BFLA).
2. **Disparo R2 — "De Datos Internos Confiables a Entrada Externa / Asíncrona"**:
   - *Cuando:* Una función, cola o servicio interno construido en una fase anterior pasa a ser alimentado por un webhook externo, un archivo subido, una API pública o la salida de un LLM.
   - *Adaptación Retroactiva Obligatoria:* La frontera de confianza se desplazó. El módulo previo debe endurecerse con validación estricta de esquema, sanitización (`V3`), límites de tamaño/timeout (`V6`) y manejo de errores aislados.
3. **Disparo R3 — "Nuevo Rol, Estado de Negocio o Flujo de Pago"**:
   - *Cuando:* Se añade un nuevo estado (ej. *cuenta suspendida*, *suscripción expirada*, *recurso archivado*) o un nuevo rol intermedio.
   - *Adaptación Retroactiva Obligatoria:* Revisar las acciones creadas en fases previas para que respeten el nuevo estado (ej. un usuario suspendido no puede seguir usando endpoints de escritura o tokens emitidos antes de la suspensión).
4. **Disparo R4 — "Nuevos Datos Sensibles (PII / Secretos) en Modelos Existentes"**:
   - *Cuando:* Se añaden campos sensibles (teléfono, documento, token de integración, API key) a una entidad que ya tenía endpoints de listado, exportación, búsqueda o logging.
   - *Adaptación Retroactiva Obligatoria:* Actualizar los serializadores/DTOs previos, exportadores y loggers ya existentes para que no filtren automáticamente los nuevos campos sensibles (`V1` / `V6`).
5. **Disparo R5 — "De Operación Síncrona Simple a Concurrencia / Escala"**:
   - *Cuando:* Una operación creada antes pasa a ejecutarse en paralelo (workers, colas, múltiples instancias o peticiones batch).
   - *Adaptación Retroactiva Obligatoria:* Revisar el código previo contra condiciones de carrera (`V4` TOCTOU), bloqueos de base de datos e idempotencia.
