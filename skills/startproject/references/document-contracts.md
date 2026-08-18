# Answer and document contracts

## Contents

- [Answer JSON](#answer-json)
- [Generated files](#generated-files)
- [Post-generation implementation](#post-generation-implementation)

## Answer JSON

Create UTF-8 JSON with these top-level objects. Strings may say `Deferred: <reason>; trigger: <condition>` when the owner deliberately postpones a capability. Do not use empty strings for required decisions.

```json
{
  "project": {
    "name": "Product name",
    "summary": "One-sentence purpose",
    "users": ["Primary user"],
    "problem": "Problem being solved",
    "success": ["Observable outcome"],
    "workflows": [
      {
        "name": "Workflow name",
        "user": "Who performs it",
        "outcome": "Successful result",
        "acceptance_criteria": ["Observable criterion"],
        "failure_modes": ["Known failure"]
      }
    ],
    "non_goals": ["Explicit non-goal"]
  },
  "repository": {
    "state": "empty | new | existing",
    "shape": "Repository/application shape",
    "framework": "Framework",
    "language": "Language",
    "runtime": "Pinned runtime",
    "package_manager": "Package manager",
    "format_command": "Command",
    "lint_command": "Command",
    "typecheck_command": "Command or not applicable",
    "test_command": "Command",
    "build_command": "Command",
    "ci": "CI system and triggers",
    "agent_tools": ["Standard tool or repository skill"]
  },
  "architecture": {
    "domains": [{"name": "Domain", "responsibility": "Responsibility"}],
    "layers": ["Types", "Config", "Repo", "Service", "Runtime", "UI"],
    "providers": ["Cross-cutting provider"],
    "boundary_rule": "How external shapes are parsed",
    "forbidden_edges": ["Forbidden dependency"],
    "invariants": ["Mechanical architecture rule"],
    "taste_rules": ["Mechanical taste rule with remediation intent"]
  },
  "legibility": {
    "worktree_boot": "Command/process or deferred statement",
    "isolation": "How instances and data are isolated",
    "ui_tools": ["DOM snapshots", "screenshots"],
    "logs": "Source and query method or deferred statement",
    "metrics": "Source and query method or deferred statement",
    "traces": "Source and query method or deferred statement",
    "journeys": ["Critical journey"],
    "performance_targets": ["Measurable target"],
    "external_system_fixtures": ["Fixture or safe substitute"]
  },
  "workflow": {
    "generation_policy": "Whether all repository changes must be agent-generated",
    "agent_responsibilities": ["Responsibility"],
    "human_responsibilities": ["Responsibility"],
    "review_loop": ["Review step"],
    "required_evidence": ["Evidence"],
    "automatic_repairs": ["Automatically repairable failure"],
    "escalation_conditions": ["Human escalation condition"],
    "merge_policy": "Risk- and throughput-specific policy",
    "publication_authority": "Commit/push/PR/merge/deploy limits"
  },
  "design": {
    "principles": ["Product/design principle"],
    "frontend_rules": ["Frontend rule"],
    "accessibility": ["Accessibility requirement"]
  },
  "quality": {
    "areas": [{"name": "Area", "grade": "Green | Yellow | Red | Unknown", "evidence": "Evidence or gap"}],
    "required_checks": ["Executable check"]
  },
  "reliability": {
    "promises": ["Reliability promise"],
    "failure_modes": ["Failure mode"],
    "recovery": ["Recovery expectation"]
  },
  "security": {
    "sensitive_data": ["Data class or none"],
    "trust_boundaries": ["Trust boundary"],
    "rules": ["Security rule"]
  },
  "maintenance": {
    "golden_principles": ["Pattern to replicate"],
    "doc_gardening_cadence": "Cadence and owner/automation",
    "cleanup_checks": ["Recurring scan"],
    "debt_policy": "How debt becomes bounded repair work"
  },
  "data": {
    "schema_source": "Authoritative source or no database",
    "generation_command": "Command or not applicable",
    "entities": [{"name": "Entity", "purpose": "Purpose", "fields": ["field: type"]}]
  }
}
```

The initializer validates the presence and basic type of every top-level section. The agent remains responsible for checking that the contents faithfully represent the confirmed interview.

## Generated files

`AGENTS.md` is a compact map with the product purpose, authoritative commands, work loop, escalation route, and links to deeper documents.

`ARCHITECTURE.md` records domains, fixed layers, forward dependency direction, providers, boundary parsing, forbidden edges, and mechanically enforced invariants.

`docs/design-docs/index.md` catalogs durable design decisions and verification state. `core-beliefs.md` stores the golden principles agents should reproduce.

`docs/PLANS.md` defines when to use ephemeral versus checked-in plans and requires progress and decision logs. Active and completed plan directories are initialized, and the debt tracker stays beside them.

`docs/generated/db-schema.md` names its source and generation command. It must say explicitly when no schema exists; never invent one.

`docs/product-specs/index.md` catalogs initial workflows. One spec is generated per workflow with user, outcome, acceptance criteria, and failure modes.

`docs/references/harness-engineering.md` links to the OpenAI article and records which practices were selected or deferred. It summarizes; it does not copy the article.

`docs/DESIGN.md`, `FRONTEND.md`, `PRODUCT_SENSE.md`, `QUALITY_SCORE.md`, `RELIABILITY.md`, and `SECURITY.md` are filled exclusively from confirmed answers.

## Post-generation implementation

The documents are the system of record, not the entire harness. After generation, implement the selected framework, package manager, formatting, CI, structural lints, worktree boot, browser tooling, observability, and recurring cleanup mechanism. Use current official documentation for the selected technologies; the Harness Engineering article supplies principles, not provider-specific setup instructions.
