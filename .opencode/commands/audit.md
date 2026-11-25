---
description: Audita el codigo implementado (git diff y tests) lanzando los 4 Goldfish en paralelo para verificar deriva arquitectonica, fidelidad UX/UI, vulnerabilidades de seguridad y calidad de tests.
agent: elephant
---

Carga y aplica las reglas de `.opencode/skills/egm-workflow/SKILL.md` para ejecutar el comando **`/audit`**.

Argumentos o ruta del documento de diseño de referencia:
$ARGUMENTS

Instrucciones de ejecución:
1. Determina el documento de diseño de referencia en `docs/design/*.md` (si aplica o fue indicado en `$ARGUMENTS`) e inspecciona los cambios actuales del repositorio (`git status` y `git diff`).
2. **Verificación Multi-Nivel (`N1`–`N5`)**: Ejecuta los comandos de verificación configurados en el proyecto:
   - `N1`: Análisis estático, typecheck y linter (`tsc --noEmit`, `eslint`, `ruff`, `mypy`, `cargo clippy`, etc.).
   - `N2` y `N3`: Suite de tests unitarios (valores frontera) y de integración/persistencia.
   - `N4`: Si el proyecto tiene interfaz Web y tests de **Playwright**, ejecuta `npx playwright test` para validar en navegador real los viajes de usuario, selectores `getByRole` y estados vacío/carga/error.
   - `N5`: Tests negativos de seguridad (`V1`–`V7`) y regresión retroactiva (`R1`–`R5`).
3. **Despacho Paralelo Goldfish en Modo Código (Obligatorio)**: En un único turno, lanza en paralelo 4 tareas (`task`) **sin `task_id`**:
   - `subagent_type: "goldfish-architecture"` (audita deriva entre diseño y código, adaptaciones retroactivas y archivos fuera de alcance)
   - `subagent_type: "goldfish-ux"` (audita cumplimiento de historias de usuario, estados vacíos/carga/error, mensajes accionables y accesibilidad)
   - `subagent_type: "goldfish-security"` (audita vulnerabilidades `V1`–`V7` y cumplimiento de mitigaciones y parches retroactivos `R1`–`R5`)
   - `subagent_type: "goldfish-testing"` (audita los 5 niveles `N1`–`N5` según `.opencode/skills/egm-workflow/testing_strategy.md`, caza mocks tautológicos, aserciones débiles y antipatrones de Playwright como `waitForTimeout` o selectores CSS frágiles)
   Pasa a cada Goldfish: `MODO: CODIGO`, la ruta absoluta del documento de diseño en `docs/design/`, la lista exacta de archivos modificados/creados y el resultado de la ejecución de `N1`–`N5`.
4. Consolida el veredicto:
   - Si los 4 Goldfish responden `[✅ APROBADO...]` y todos los niveles de tests pasan en verde, emite **`[✅ AUDITORÍA COMPLETA: LISTO PARA PR]`**.
   - Si existen hallazgos `[BLOQUEANTE]` o `[IMPORTANTE]`, preséntalos numerados con archivo, línea y solución propuesta.
