---
description: Genera o actualiza un mapa compacto de arquitectura, patrones UX/UI, invariantes de seguridad y comandos de pruebas en docs/CONTEXT.md para alimentar al Elefante.
agent: elephant
---

Carga y aplica las reglas de `.opencode/skills/egm-workflow/SKILL.md` para ejecutar el comando **`/context`**.

Directorio o alcance solicitado:
$ARGUMENTS

Instrucciones de ejecución:
1. Explora los manifiestos del repositorio (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `opencode.json`, etc.), la estructura de directorios y los puntos de entrada principales (respetando `.gitignore`).
2. No modifiques ningún archivo de código fuente.
3. Crea o actualiza `docs/CONTEXT.md` en español con una síntesis densa y libre de paja (pensada para que futuras sesiones del Elefante entiendan el sistema en segundos con el mínimo gasto de tokens):
   - **Visión General y Propósito del Sistema**
   - **Mapa de Arquitectura y Módulos Construidos** (tabla de directorios/archivos principales y su responsabilidad exacta)
   - **Patrones de UX/UI, CLI o Contratos de API**
   - **Perfil de Seguridad Retroadaptativo (según `.opencode/skills/egm-workflow/security_vectors.md`)**:
     - *Superficie Acumulada Activa*: qué capacidades tiene hoy el sistema (Auth, BD, Multi-tenant, Uploads, Pagos, Webhooks, LLMs, etc.).
     - *Vectores Clásicos y Mayores Activos (`V1`–`V7`)*: qué controles están implementados y dónde.
     - *Invariantes Retroactivos Obligatorios*: qué reglas de seguridad y aislamiento debe respetar cualquier nueva funcionalidad o módulo previo al evolucionar el sistema.
   - **Estrategia y Comandos de Verificación** (comandos exactos de build, lint y tests).
4. Informa en el chat que `docs/CONTEXT.md` ha sido actualizado con el mapa arquitectónico y el perfil retroadaptativo de seguridad.
