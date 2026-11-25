# Reglas del Proyecto — Modelo Ágil Elephant-Goldfish (`egm-es-opencode`)

Este repositorio implementa una versión minimalista, en español y nativa para **OpenCode** del **Elephant-Goldfish Model (EGM)**, ampliada con **UX/UI**, **Seguridad** y **Testing** en todo el ciclo de vida.

## Convenciones de Trabajo

1. **Directorio de Diseños (`docs/design/`)**:
   - Toda especificación de funcionalidad se guarda como un único documento vivo en `docs/design/<feature>.md` siguiendo `.opencode/skills/egm-workflow/design_template.md`.
   - No generes archivos temporales sueltos en la raíz del proyecto.
2. **Comandos Principales**:
   - `/design <idea>`: Co-diseña con **El Elefante** (`elephant`) mediante una breve entrevista socrática y genera `docs/design/<feature>.md`.
   - `/review [ruta]`: Lanza en paralelo a los **4 subagentes Goldfish** (`goldfish-architecture`, `goldfish-ux`, `goldfish-security`, `goldfish-testing`) sin memoria previa (`task` sin `task_id`) para validar el diseño.
   - `/audit [ruta]`: Ejecuta los tests del proyecto y lanza en paralelo a los **4 Goldfish** en `MODO: CODIGO` para auditar el `git diff` frente al diseño, detectar deriva, estados UX olvidados, vulnerabilidades OWASP/STRIDE y tests tautológicos.
   - `/context [directorio]`: Genera o actualiza el mapa de contexto del repositorio en `docs/CONTEXT.md`.
3. **Aislamiento de los Goldfish**:
   - Los 4 agentes `goldfish-*` son estrictamente de **solo lectura** y **memoria cero**. Nunca reutilices un `task_id` al invocarlos ni les pases el historial de conversación del Elefante.
