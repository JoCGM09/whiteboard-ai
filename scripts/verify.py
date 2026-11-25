#!/usr/bin/env python3
"""Script de verificacion automatica de la configuracion eg-es-opencode."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_AGENTS = {
    "elephant": "primary",
    "goldfish-architecture": "subagent",
    "goldfish-ux": "subagent",
    "goldfish-security": "subagent",
    "goldfish-testing": "subagent",
}

EXPECTED_COMMANDS = ("design", "review", "audit", "context")


def parse_frontmatter(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise AssertionError(f"Falta frontmatter YAML en {path}")
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        raise AssertionError(f"Frontmatter mal cerrado en {path}")
    return parts[1], parts[2].strip()


def verify_opencode_json() -> None:
    cfg_path = ROOT / "opencode.json"
    assert cfg_path.is_file(), "No existe opencode.json"
    data = json.loads(cfg_path.read_text(encoding="utf-8"))
    assert data.get("$schema") == "https://opencode.ai/config.json", "$schema invalido en opencode.json"
    assert data.get("default_agent") == "elephant", "default_agent debe ser 'elephant'"
    assert isinstance(data.get("skills", {}).get("paths"), list), "skills.paths debe ser una lista"


def verify_agents() -> None:
    agents_dir = ROOT / ".opencode" / "agents"
    for agent_name, expected_mode in EXPECTED_AGENTS.items():
        path = agents_dir / f"{agent_name}.md"
        assert path.is_file(), f"Falta el agente: {path}"
        fm, body = parse_frontmatter(path)
        assert re.search(rf"^mode:\s*{expected_mode}\s*$", fm, re.MULTILINE), (
            f"Agente {agent_name} debe tener mode: {expected_mode}"
        )
        assert re.search(r"^description:\s*.+$", fm, re.MULTILINE), (
            f"Agente {agent_name} debe tener description"
        )
        assert len(body) > 200, f"El prompt del agente {agent_name} esta vacio o incompleto"

        if expected_mode == "subagent":
            for denied_tool in ("edit: deny", "bash: deny", "task: deny", "grep: deny"):
                assert denied_tool in fm, f"Goldfish {agent_name} debe incluir '{denied_tool}'"
            assert '"*.env": deny' in fm, f"Goldfish {agent_name} debe bloquear lectura de *.env"


def verify_commands() -> None:
    commands_dir = ROOT / ".opencode" / "commands"
    for cmd in EXPECTED_COMMANDS:
        path = commands_dir / f"{cmd}.md"
        assert path.is_file(), f"Falta el comando /{cmd} en {path}"
        fm, body = parse_frontmatter(path)
        assert re.search(r"^description:\s*.+$", fm, re.MULTILINE), f"Falta description en /{cmd}"
        assert re.search(r"^agent:\s*elephant\s*$", fm, re.MULTILINE), f"/{cmd} debe apuntar a agent: elephant"
        assert "$ARGUMENTS" in body, f"El comando /{cmd} debe incluir $ARGUMENTS en su plantilla"


def verify_skills() -> None:
    skill_dir = ROOT / ".opencode" / "skills" / "egm-workflow"
    skill_md = skill_dir / "SKILL.md"
    template_md = skill_dir / "design_template.md"
    vectors_md = skill_dir / "security_vectors.md"
    testing_md = skill_dir / "testing_strategy.md"
    assert skill_md.is_file(), f"Falta {skill_md}"
    assert template_md.is_file(), f"Falta {template_md}"
    assert vectors_md.is_file(), f"Falta {vectors_md}"
    assert testing_md.is_file(), f"Falta {testing_md}"

    fm, body = parse_frontmatter(skill_md)
    assert re.search(r"^name:\s*egm-workflow\s*$", fm, re.MULTILINE), "name en SKILL.md debe coincidir con egm-workflow"
    assert re.search(r"^description:\s*.+$", fm, re.MULTILINE), "Falta description en SKILL.md"
    for agent_name in EXPECTED_AGENTS:
        if agent_name != "elephant":
            assert agent_name in body, f"SKILL.md debe referenciar al subagente {agent_name}"

    template_text = template_md.read_text(encoding="utf-8")
    for required_section in (
        "## 1. Problema, Objetivos y Alcance",
        "## 2. Experiencia de Usuario (UX/UI) e Historias de Usuario",
        "## 3. Diseño Técnico y Alternativas Descartadas",
        "## 4. Seguridad, Vectores (`V1`–`V7`) y Adaptación Retroactiva",
        "### 4.1. Vectores de Seguridad Clásicos y Mayores Aplicables",
        "### 4.2. Impacto Retroadaptativo sobre Módulos Ya Construidos (`R1`–`R5`)",
        "## 5. Plan de Archivos (Regla de Cero Decisiones)",
        "## 6. Plan de Pruebas y Matriz de Verificación (`N1`–`N5` y Playwright)",
    ):
        assert required_section in template_text, f"Falta seccion '{required_section}' en design_template.md"

    vectors_text = vectors_md.read_text(encoding="utf-8")
    for v_id in ("`V1`", "`V2`", "`V3`", "`V4`", "`V5`", "`V6`", "`V7`"):
        assert v_id in vectors_text, f"Falta vector {v_id} en security_vectors.md"
    for r_id in ("Disparo R1", "Disparo R2", "Disparo R3", "Disparo R4", "Disparo R5"):
        assert r_id in vectors_text, f"Falta regla retroadaptativa '{r_id}' en security_vectors.md"

    testing_text = testing_md.read_text(encoding="utf-8")
    for n_id in ("`N1`", "`N2`", "`N3`", "`N4`", "`N5`"):
        assert n_id in testing_text, f"Falta nivel de prueba {n_id} en testing_strategy.md"
    assert "Playwright" in testing_text, "Falta cobertura de Playwright en testing_strategy.md"


def main() -> int:
    try:
        verify_opencode_json()
        verify_agents()
        verify_commands()
        verify_skills()
    except AssertionError as exc:
        print(f"[ERROR DE VERIFICACION] {exc}", file=sys.stderr)
        return 1

    print("[OK] Verificacion completada con exito:")
    print(f"  - opencode.json valido (default_agent: elephant)")
    print(f"  - {len(EXPECTED_AGENTS)} agentes verificados (1 Elefante + 4 Goldfish read-only)")
    print(f"  - {len(EXPECTED_COMMANDS)} comandos verificados (/design, /review, /audit, /context)")
    print(f"  - Skill egm-workflow y plantilla design_template.md verificadas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
