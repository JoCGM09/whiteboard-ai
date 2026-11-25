---
description: Lanza los 4 subagentes Goldfish (Arquitectura, UX/UI, Seguridad y Pruebas) en paralelo y sin memoria previa para validar un documento en docs/design/.
agent: elephant
---

Carga y aplica las reglas de `.opencode/skills/egm-workflow/SKILL.md` para ejecutar el comando **`/review`**.

Documento objetivo o argumentos del usuario:
$ARGUMENTS

Instrucciones de ejecución:
1. Determina el documento de diseño objetivo (si `$ARGUMENTS` está vacío, selecciona el archivo más reciente en `docs/design/*.md`).
2. Lee el documento de diseño y extrae la lista de archivos existentes del repositorio que son referenciados en él.
3. **Despacho Paralelo Goldfish (Obligatorio)**: En un único turno, lanza en paralelo 4 tareas (`task`) **sin `task_id`** y sin pasar el historial de conversación previa:
   - `subagent_type: "goldfish-architecture"`
   - `subagent_type: "goldfish-ux"`
   - `subagent_type: "goldfish-security"`
   - `subagent_type: "goldfish-testing"`
   En el `prompt` de cada tarea indica explícitamente:
   - `MODO: DISENO`
   - La ruta absoluta del documento en `docs/design/`
   - La lista de rutas de los archivos fuente referenciados.
4. Cuando los 4 Goldfish terminen:
   - Muestra primero la **Paráfrasis de Comprensión** devuelta por `goldfish-architecture` para que el usuario confirme si el documento se explica por sí solo.
   - Consolida y deduplica todos los hallazgos `[BLOQUEANTE]` e `[IMPORTANTE]` de las 4 áreas (Arquitectura, UX/UI, Seguridad, Pruebas), clasificándolos como **`[CORREGIR]`** (con el cambio concreto propuesto) o **`[IMPUGNAR]`** (con evidencia verificable en código o documento).
   - Pregunta al usuario qué correcciones desea aplicar sobre el archivo `docs/design/<feature>.md`.
