---
description: Co-disena una funcionalidad con El Elefante (entrevista socratica + especificacion completa en docs/design/ con UX/UI, Seguridad y Testing).
agent: elephant
---

Carga y aplica las reglas de `.opencode/skills/egm-workflow/SKILL.md` para ejecutar el comando **`/design`**.

Solicitud del usuario:
$ARGUMENTS

Instrucciones de ejecución:
1. **Regla Cero Código**: No escribas código fuente ni inicialices frameworks en esta fase.
2. Lee `.opencode/skills/egm-workflow/security_vectors.md` y `.opencode/skills/egm-workflow/testing_strategy.md`, y detecta si el proyecto se está creando **desde cero** (Iteración `00`, sin código de aplicación) o si ya cuenta con módulos construidos y `docs/CONTEXT.md` (Iteración `01..N`).
3. Si la solicitud aún tiene incógnitas críticas, haz **entre 2 y 4 preguntas directas y numeradas** en español (sin halagos ni relleno) sobre:
   - (1) Alcance, stack/arquitectura y (si ya hay módulos previos) qué piezas existentes se verán afectadas.
   - (2) Historias de usuario y estados límite de UX/UI (vacío/carga/error).
   - (3) Vectores de seguridad clásicos/mayores (`V1`–`V7`) y adaptaciones retroactivas (`R1`–`R5`) sobre lo ya armado.
   - (4) Estrategia de pruebas en los 5 niveles (`N1` Estático/Lint, `N2` Unitarios/Valores Frontera, `N3` Integración/BD, `N4` Validación E2E con Playwright si hay UI Web, y `N5` Pruebas negativas de abuso y regresión retroactiva).
   Espera la respuesta del usuario antes de redactar el documento.
4. Con las respuestas del usuario, redacta directamente el documento único en `docs/design/<slug>.md` (por ejemplo `docs/design/00-arquitectura-base.md` si es desde cero, o `docs/design/01-<funcionalidad>.md`) usando la estructura exacta de `.opencode/skills/egm-workflow/design_template.md`. Asegúrate de completar tanto los Vectores `V1`–`V7` (sección 4.1) como el Impacto Retroadaptativo `R1`–`R5` (sección 4.2), el Plan de Archivos (sección 5, incluyendo archivos de test unitarios, de integración y `.spec.ts` de Playwright) y la Matriz de Pruebas `N1`–`N5` (sección 6).
5. Comparte en el chat la ruta `docs/design/<slug>.md` con un resumen de 3 líneas e indica que el siguiente paso es ejecutar `/review docs/design/<slug>.md`.
