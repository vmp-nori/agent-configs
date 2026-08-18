#!/usr/bin/env python3
"""Generate an interview-filled harness knowledge base from a JSON answer file."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED_SECTIONS = {
    "project": ["name", "summary", "users", "problem", "success", "workflows", "non_goals"],
    "repository": [
        "state", "shape", "framework", "language", "runtime", "package_manager",
        "format_command", "lint_command", "typecheck_command", "test_command",
        "build_command", "ci", "agent_tools",
    ],
    "architecture": [
        "domains", "layers", "providers", "boundary_rule", "forbidden_edges",
        "invariants", "taste_rules",
    ],
    "legibility": [
        "worktree_boot", "isolation", "ui_tools", "logs", "metrics", "traces",
        "journeys", "performance_targets", "external_system_fixtures",
    ],
    "workflow": [
        "generation_policy", "agent_responsibilities", "human_responsibilities", "review_loop",
        "required_evidence", "automatic_repairs", "escalation_conditions",
        "merge_policy", "publication_authority",
    ],
    "design": ["principles", "frontend_rules", "accessibility"],
    "quality": ["areas", "required_checks"],
    "reliability": ["promises", "failure_modes", "recovery"],
    "security": ["sensitive_data", "trust_boundaries", "rules"],
    "maintenance": [
        "golden_principles", "doc_gardening_cadence", "cleanup_checks", "debt_policy",
    ],
    "data": ["schema_source", "generation_command", "entities"],
}


def clean(value: Any) -> str:
    return " ".join(str(value).split())


def slugify(value: str) -> str:
    value = value.encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-") or "workflow"


def md_list(values: list[Any], empty: str = "None recorded.") -> str:
    cleaned = [clean(value) for value in values if clean(value)]
    return "\n".join(f"- {value}" for value in cleaned) if cleaned else f"- {empty}"


def md_table(headers: list[str], rows: list[list[Any]]) -> str:
    head = "| " + " | ".join(headers) + " |"
    rule = "| " + " | ".join("---" for _ in headers) + " |"
    body = ["| " + " | ".join(clean(cell).replace("|", "\\|") for cell in row) + " |" for row in rows]
    return "\n".join([head, rule, *body])


def code_or_text(value: Any) -> str:
    text = clean(value)
    return f"`{text}`" if text and text.lower() not in {"not applicable", "n/a"} else text


def validate(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["answer file must contain a JSON object"]
    for section, fields in REQUIRED_SECTIONS.items():
        value = data.get(section)
        if not isinstance(value, dict):
            errors.append(f"missing object: {section}")
            continue
        for field in fields:
            if field not in value:
                errors.append(f"missing field: {section}.{field}")
    list_fields = {
        "project": ["users", "success", "workflows", "non_goals"],
        "repository": ["agent_tools"],
        "architecture": ["domains", "layers", "providers", "forbidden_edges", "invariants", "taste_rules"],
        "legibility": ["ui_tools", "journeys", "performance_targets", "external_system_fixtures"],
        "workflow": [
            "agent_responsibilities", "human_responsibilities", "review_loop",
            "required_evidence", "automatic_repairs", "escalation_conditions",
        ],
        "design": ["principles", "frontend_rules", "accessibility"],
        "quality": ["areas", "required_checks"],
        "reliability": ["promises", "failure_modes", "recovery"],
        "security": ["sensitive_data", "trust_boundaries", "rules"],
        "maintenance": ["golden_principles", "cleanup_checks"],
        "data": ["entities"],
    }
    for section, fields in list_fields.items():
        value = data.get(section, {})
        if not isinstance(value, dict):
            continue
        for field in fields:
            if field in value and not isinstance(value[field], list):
                errors.append(f"{section}.{field} must be an array")
    project = data.get("project", {})
    if isinstance(project, dict):
        if not clean(project.get("name", "")):
            errors.append("project.name must not be empty")
        workflows = project.get("workflows")
        if not isinstance(workflows, list) or not workflows:
            errors.append("project.workflows must contain at least one workflow")
        else:
            for index, workflow in enumerate(workflows):
                if not isinstance(workflow, dict):
                    errors.append(f"project.workflows[{index}] must be an object")
                    continue
                for field in ["name", "user", "outcome", "acceptance_criteria", "failure_modes"]:
                    if field not in workflow:
                        errors.append(f"missing field: project.workflows[{index}].{field}")
    for section, field in [("architecture", "domains"), ("quality", "areas"), ("data", "entities")]:
        section_value = data.get(section, {})
        values = section_value.get(field, []) if isinstance(section_value, dict) else []
        if isinstance(values, list):
            for index, value in enumerate(values):
                if not isinstance(value, dict):
                    errors.append(f"{section}.{field}[{index}] must be an object")
    return errors


def build_files(data: dict[str, Any]) -> dict[str, str]:
    project = data["project"]
    repo = data["repository"]
    architecture = data["architecture"]
    legibility = data["legibility"]
    workflow = data["workflow"]
    design = data["design"]
    quality = data["quality"]
    reliability = data["reliability"]
    security = data["security"]
    maintenance = data["maintenance"]
    data_model = data["data"]
    name = clean(project["name"])

    commands = [
        ["Format", code_or_text(repo["format_command"])],
        ["Lint", code_or_text(repo["lint_command"])],
        ["Type check", code_or_text(repo["typecheck_command"])],
        ["Test", code_or_text(repo["test_command"])],
        ["Build", code_or_text(repo["build_command"])],
    ]
    domain_rows = [[item.get("name", ""), item.get("responsibility", "")] for item in architecture["domains"]]
    quality_rows = [[item.get("name", ""), item.get("grade", ""), item.get("evidence", "")] for item in quality["areas"]]
    entity_rows = [[item.get("name", ""), item.get("purpose", ""), ", ".join(item.get("fields", []))] for item in data_model["entities"]]
    workflow_rows = [[item.get("name", ""), item.get("user", ""), item.get("outcome", "")] for item in project["workflows"]]
    layer_path = " → ".join(clean(layer) for layer in architecture["layers"])

    files: dict[str, str] = {}
    files["AGENTS.md"] = f"""# {name} repository map

{clean(project['summary'])}

## Start here

- `ARCHITECTURE.md` — domains, layers, providers, boundaries, and enforced invariants
- `docs/PRODUCT_SENSE.md` — users, problem, workflows, outcomes, and non-goals
- `docs/DESIGN.md` and `docs/FRONTEND.md` — product and interface rules
- `docs/PLANS.md` and `docs/exec-plans/` — planning, decisions, progress, and debt
- `docs/QUALITY_SCORE.md` — evidence-backed quality grades
- `docs/RELIABILITY.md` and `docs/SECURITY.md` — runtime and trust expectations
- `docs/product-specs/` — initial workflow specifications
- `docs/design-docs/` — durable decisions and golden principles
- `docs/generated/` and `docs/references/` — generated facts and external context

## Authoritative commands

{md_table(['Purpose', 'Command'], commands)}

CI: {clean(repo['ci'])}
Worktree boot: {code_or_text(legibility['worktree_boot'])}

## Agent loop

Validate current state → reproduce → implement → inspect and test → self-review → request targeted reviews → repair → repeat.

Escalate when:

{md_list(workflow['escalation_conditions'])}

Publication authority: {clean(workflow['publication_authority'])}
"""

    files["ARCHITECTURE.md"] = f"""# {name} architecture

## Repository shape

{clean(repo['shape'])}; {clean(repo['framework'])}; {clean(repo['language'])}; {clean(repo['runtime'])}; {clean(repo['package_manager'])}.

## Domains

{md_table(['Domain', 'Responsibility'], domain_rows)}

## Layer direction

```text
{layer_path}
```

Dependencies may move only forward through this sequence unless an explicit design document changes the rule.

## Providers

Cross-cutting concerns enter through the provider boundary:

{md_list(architecture['providers'])}

## Boundary parsing

{clean(architecture['boundary_rule'])}

## Forbidden edges

{md_list(architecture['forbidden_edges'])}

## Mechanical invariants

{md_list(architecture['invariants'])}

## Mechanical taste rules

{md_list(architecture['taste_rules'])}

Custom checks must explain how an agent should remediate each violation.
"""

    files["docs/PRODUCT_SENSE.md"] = f"""# Product sense

## Product

{clean(project['summary'])}

## Users and problem

Users:

{md_list(project['users'])}

Problem: {clean(project['problem'])}

## Initial workflows

{md_table(['Workflow', 'User', 'Outcome'], workflow_rows)}

## Success

{md_list(project['success'])}

## Non-goals

{md_list(project['non_goals'])}

Humans steer priorities and acceptance; agents execute within the repository harness described by this knowledge base.
"""

    files["docs/DESIGN.md"] = f"""# Design

## Product and interaction principles

{md_list(design['principles'])}

## Accessibility

{md_list(design['accessibility'])}

Review feedback that recurs must become a durable rule, check, or design document.
"""

    files["docs/FRONTEND.md"] = f"""# Frontend

Framework: {clean(repo['framework'])}

## Rules

{md_list(design['frontend_rules'])}

## Agent-visible UI

Tools:

{md_list(legibility['ui_tools'])}

Critical journeys:

{md_list(legibility['journeys'])}

Required evidence:

{md_list(workflow['required_evidence'])}
"""

    files["docs/PLANS.md"] = f"""# Plans

Use lightweight ephemeral plans for small, local work. Check complex work into `exec-plans/active/`; move it to `completed/` when its acceptance criteria pass.

Every checked-in plan contains:

- outcome and acceptance criteria;
- progress log;
- decision log with alternatives;
- implementation slices;
- validation evidence;
- risks, escalation points, and deferred work.

Generation policy: {clean(workflow['generation_policy'])}

## Review and repair loop

{md_list(workflow['review_loop'])}

## Automatic repair

{md_list(workflow['automatic_repairs'])}

## Merge policy

{clean(workflow['merge_policy'])}
"""

    files["docs/QUALITY_SCORE.md"] = f"""# Quality score

Grades must cite current evidence or a concrete gap.

{md_table(['Area', 'Grade', 'Evidence or gap'], quality_rows)}

## Required checks

{md_list(quality['required_checks'])}

Update grades during recurring repository maintenance and after material product changes.
"""

    files["docs/RELIABILITY.md"] = f"""# Reliability

## Promises

{md_list(reliability['promises'])}

## Known failure modes

{md_list(reliability['failure_modes'])}

## Recovery expectations

{md_list(reliability['recovery'])}

## Agent-legible runtime

- Worktree boot: {clean(legibility['worktree_boot'])}
- Isolation: {clean(legibility['isolation'])}
- Logs: {clean(legibility['logs'])}
- Metrics: {clean(legibility['metrics'])}
- Traces: {clean(legibility['traces'])}

Performance targets:

{md_list(legibility['performance_targets'])}

External-system fixtures:

{md_list(legibility['external_system_fixtures'])}
"""

    files["docs/SECURITY.md"] = f"""# Security

## Sensitive data

{md_list(security['sensitive_data'])}

## Trust boundaries

{md_list(security['trust_boundaries'])}

## Rules

{md_list(security['rules'])}

Security, legal, and other judgment-heavy decisions follow the human escalation rules in `AGENTS.md`.
"""

    files["docs/design-docs/index.md"] = """# Design documents

Catalog durable architecture, product, and interaction decisions here. Each entry records status, verification evidence, and the condition for revisiting it.

| Document | Status | Verification |
| --- | --- | --- |
| `core-beliefs.md` | Active | Enforced through review and selected mechanical checks |
"""

    files["docs/design-docs/core-beliefs.md"] = f"""# Core beliefs

These golden principles are patterns agents should reproduce throughout the repository:

{md_list(maintenance['golden_principles'])}

When a principle is objective and recurrent, promote it into a lint, structural test, or repository tool.
"""

    files["docs/exec-plans/active/.gitkeep"] = ""
    files["docs/exec-plans/completed/.gitkeep"] = ""
    files["docs/exec-plans/tech-debt-tracker.md"] = f"""# Technical debt tracker

Policy: {clean(maintenance['debt_policy'])}

| Item | Impact | Evidence | Trigger | Owner/status |
| --- | --- | --- | --- | --- |
| None recorded | — | — | — | Open |

Maintenance cadence: {clean(maintenance['doc_gardening_cadence'])}

Recurring checks:

{md_list(maintenance['cleanup_checks'])}
"""

    files["docs/generated/db-schema.md"] = f"""# Database schema

Authoritative source: {clean(data_model['schema_source'])}

Generation command: {code_or_text(data_model['generation_command'])}

{md_table(['Entity', 'Purpose', 'Fields'], entity_rows) if entity_rows else 'No database entities were selected during initialization. Do not invent a schema.'}

This file is generated. Change the authoritative source and regenerate it instead of editing derived facts by hand.
"""

    files["docs/product-specs/index.md"] = f"""# Product specifications

{md_table(['Workflow', 'User', 'Outcome'], workflow_rows)}
"""

    used_slugs: set[str] = set()
    for index, item in enumerate(project["workflows"], start=1):
        base = slugify(clean(item["name"]))
        slug = base
        if slug in used_slugs:
            slug = f"{base}-{index}"
        used_slugs.add(slug)
        files[f"docs/product-specs/{slug}.md"] = f"""# {clean(item['name'])}

## User

{clean(item['user'])}

## Outcome

{clean(item['outcome'])}

## Acceptance criteria

{md_list(item['acceptance_criteria'])}

## Failure modes

{md_list(item['failure_modes'])}
"""

    files["docs/references/harness-engineering.md"] = f"""# Harness Engineering reference

Source: [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/), OpenAI, February 11, 2026.

Selected practices:

- Repository knowledge is the versioned system of record; `AGENTS.md` is a map.
- Architecture and taste invariants are mechanically enforced.
- Application UI and operational signals are made legible to agents as selected below.
- Plans, review/repair loops, and recurring garbage collection are first-class.

Selected application-legibility capabilities:

{md_list(legibility['ui_tools'])}

Observability decisions:

- Logs: {clean(legibility['logs'])}
- Metrics: {clean(legibility['metrics'])}
- Traces: {clean(legibility['traces'])}

This repository adapts the article's ideas to its confirmed product decisions. The article reports one experiment, not a universal performance guarantee or automatic grant of production authority.
"""

    return {path: content.rstrip() + "\n" for path, content in files.items()}


def write_files(
    root: Path,
    files: dict[str, str],
    dry_run: bool,
    overwrite: bool,
    overwrite_root: bool,
) -> list[str]:
    results: list[str] = []
    protected = {"AGENTS.md", "ARCHITECTURE.md"}
    for relative, content in files.items():
        path = root / relative
        if path.exists() and not overwrite:
            results.append(f"SKIP {relative} (already exists)")
            continue
        if path.exists() and relative in protected and not overwrite_root:
            results.append(f"SKIP {relative} (protected; add --overwrite-root only after explicit approval)")
            continue
        if dry_run:
            results.append(f"PLAN {relative}")
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        results.append(f"WRITE {relative}")
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--answers", required=True, help="Confirmed interview answers as JSON")
    parser.add_argument("--root", required=True, help="Target project root")
    parser.add_argument("--dry-run", action="store_true", help="Print planned writes")
    parser.add_argument("--overwrite", action="store_true", help="Replace existing generated documents except protected root maps")
    parser.add_argument("--overwrite-root", action="store_true", help="Also replace AGENTS.md and ARCHITECTURE.md")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    answers_path = Path(args.answers).expanduser().resolve()
    root = Path(args.root).expanduser().resolve()
    if not answers_path.is_file():
        print(f"error: answers file not found: {answers_path}", file=sys.stderr)
        return 2
    if not root.is_dir():
        print(f"error: target root is not a directory: {root}", file=sys.stderr)
        return 2
    try:
        data = json.loads(answers_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"error: could not read answers JSON: {error}", file=sys.stderr)
        return 2
    errors = validate(data)
    if errors:
        print("answer validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 2
    files = build_files(data)
    print("\n".join(write_files(root, files, args.dry_run, args.overwrite, args.overwrite_root)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
