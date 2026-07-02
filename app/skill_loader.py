"""Load a local Agent Skill folder into Google ADK skill models."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType
from typing import Any, Callable

import yaml
from google.adk.skills.models import Frontmatter, Resources, Script, Skill


def _read_text_resources(
    directory: Path,
    allowed_suffixes: set[str],
) -> dict[str, str]:
    """Read files below a resource directory using stable relative keys."""
    if not directory.exists():
        return {}
    return {
        file.relative_to(directory).as_posix(): file.read_text(encoding="utf-8")
        for file in directory.rglob("*")
        if file.is_file()
        and file.suffix.lower() in allowed_suffixes
        and "__pycache__" not in file.parts
    }


def load_local_skill(skill_dir: Path) -> Skill:
    """Parse a standard local skill folder into an ADK ``Skill`` model."""
    skill_file = skill_dir / "SKILL.md"
    raw = skill_file.read_text(encoding="utf-8")
    if not raw.startswith("---\n"):
        raise ValueError(f"Missing YAML frontmatter in {skill_file}.")

    _, frontmatter_text, instructions = raw.split("---", maxsplit=2)
    metadata = yaml.safe_load(frontmatter_text)
    frontmatter = Frontmatter(
        name=metadata["name"],
        description=metadata["description"],
    )

    script_sources = _read_text_resources(skill_dir / "scripts", {".py"})
    resources = Resources(
        references=_read_text_resources(
            skill_dir / "references", {".json", ".md", ".txt", ".yaml", ".yml"}
        ),
        assets=_read_text_resources(
            skill_dir / "assets", {".json", ".md", ".txt", ".yaml", ".yml"}
        ),
        scripts={name: Script(src=source) for name, source in script_sources.items()},
    )
    return Skill(
        frontmatter=frontmatter,
        instructions=instructions.strip(),
        resources=resources,
    )


def load_skill_function(
    skill_dir: Path,
    relative_script: str,
    function_name: str,
) -> Callable[..., Any]:
    """Load one trusted callable from a bundled Python skill script."""
    script_path = (skill_dir / "scripts" / relative_script).resolve()
    scripts_dir = (skill_dir / "scripts").resolve()
    if not script_path.is_relative_to(scripts_dir):
        raise PermissionError("Skill script is outside the allowlisted scripts directory.")

    spec = importlib.util.spec_from_file_location(
        f"vietlearn_skill_{script_path.stem}", script_path
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load skill script: {script_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, function_name)
