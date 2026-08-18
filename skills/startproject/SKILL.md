---
name: startproject
description: >-
  Interview a product owner and initialize an agent-first software repository
  using the practices described in OpenAI's Harness Engineering article. Use
  when starting a new product, onboarding an existing repository for Codex-led
  development, or creating the repository map, structured knowledge base,
  architecture constraints, application-legibility tools, plans, quality
  grades, review loop, and recurring entropy controls needed for reliable agent
  execution. Ask the interview before scaffolding; do not infer product choices
  that the owner has not made.
---

# Start Project

Build the repository harness from the owner's answers. Treat [OpenAI's Harness Engineering article](https://openai.com/index/harness-engineering/) as the sole design source for this skill.

Read [references/interview.md](references/interview.md) before asking questions. Read [references/document-contracts.md](references/document-contracts.md) before creating files.

## 1. Inspect without deciding

Inspect the target directory, git status, manifests, lockfiles, framework configuration, existing agent instructions, CI, test commands, and source layout. Use observable facts to avoid asking questions the repository already answers. Do not treat existing project conventions as harness requirements unless the owner confirms them.

If the target does not exist, ask where to create it. Do not initialize a framework, install packages, or write files before the interview is confirmed.

## 2. Run the interview

Ask the question bank in six short rounds:

1. product intent and first user workflows;
2. repository, framework, package manager, CI, and formatting;
3. domains, layers, providers, boundaries, and taste invariants;
4. worktree boot, UI inspection, logs, metrics, traces, and measurable journeys;
5. agent/human responsibilities, review loop, merge policy, and escalation;
6. design, quality, reliability, security, golden principles, and garbage collection.

Ask four to seven related questions per message, then wait. Adapt follow-ups to the answers. Explain unfamiliar terms in one sentence. Offer examples as examples, never defaults.

Do not answer subjective product questions on the owner's behalf. If the owner explicitly delegates a choice, propose the smallest option that makes the environment legible and enforceable. Mark deferred capabilities as deferred with an activation trigger.

After the final round, return a concise structured summary covering every field in the answer contract. Identify contradictions, unresolved required fields, and decisions that would create irreversible or security-sensitive infrastructure. Ask the owner to confirm or correct the summary. Do not scaffold before confirmation.

## 3. Create the answer artifact

Translate the confirmed interview into the JSON contract in [references/document-contracts.md](references/document-contracts.md). Keep the working JSON in a temporary directory unless the owner asks to preserve it. Never place secrets, tokens, credentials, private keys, or production data in it.

For a new or documentation-empty repository:

```bash
python3 <skill-dir>/scripts/init_harness.py \
  --answers /absolute/path/to/answers.json \
  --root /absolute/path/to/project \
  --dry-run
```

Review the planned paths, then rerun without `--dry-run`.

For an existing repository, generate into a temporary empty directory first. Compare the generated artifacts with existing instructions and merge them deliberately. Never overwrite an existing `AGENTS.md` or `ARCHITECTURE.md` without showing the owner the conflict and receiving explicit approval.

## 4. Initialize the article's knowledge topology

Create this structure from the confirmed answers:

```text
AGENTS.md
ARCHITECTURE.md
docs/
├── design-docs/
│   ├── index.md
│   └── core-beliefs.md
├── exec-plans/
│   ├── active/
│   ├── completed/
│   └── tech-debt-tracker.md
├── generated/
│   └── db-schema.md
├── product-specs/
│   ├── index.md
│   └── <one spec per initial workflow>.md
├── references/
│   └── harness-engineering.md
├── DESIGN.md
├── FRONTEND.md
├── PLANS.md
├── PRODUCT_SENSE.md
├── QUALITY_SCORE.md
├── RELIABILITY.md
└── SECURITY.md
```

Keep `AGENTS.md` near 100 lines and use it as a table of contents. Put durable detail in the linked documents. Make every document specific to the interview; do not leave generic filler disguised as policy.

## 5. Build the executable scaffold

After the knowledge base exists, implement the repository structure, application framework, package-manager setup, formatting rules, and CI configuration selected in the interview. For existing applications, preserve the framework unless the owner requested a migration.

Turn the confirmed architecture into mechanical constraints:

- divide each business domain into the chosen fixed layers;
- permit dependencies only in the confirmed forward direction;
- route cross-cutting concerns through the confirmed provider interface;
- parse external data shapes at boundaries;
- add custom lint or structural checks for architecture and taste invariants;
- write failures with concrete remediation instructions for the next agent.

Do not micromanage implementation style beyond the confirmed invariants. Enforce boundaries, correctness, reproducibility, and legibility; allow local freedom inside them.

## 6. Make the application legible to agents

Implement only the capabilities selected in the interview, and record deferred capabilities with activation triggers:

- one bootable application instance per worktree;
- agent-accessible DOM snapshots, screenshots, navigation, and recordings;
- isolated logs, metrics, and traces that are torn down with the worktree;
- commands or skills for querying those signals;
- executable performance and critical-journey assertions.

Do not claim end-to-end autonomy until the repository can validate, reproduce, inspect, repair, and review its own work with evidence.

## 7. Encode the work loop

Make plans first-class. Use ephemeral plans for small work and checked-in execution plans with progress and decision logs for complex work. Establish this loop:

```text
validate current state → reproduce → implement → inspect and test
→ self-review → request targeted agent reviews → repair → repeat
→ escalate only when judgment is required
```

Configure merge gates according to the confirmed throughput and risk tolerance. The article's minimal-gate approach is context-dependent; never copy it without an explicit owner decision.

## 8. Install entropy controls

Encode confirmed golden principles in `docs/design-docs/core-beliefs.md` and in checks where practical. Set up the selected recurring maintenance mechanism to:

- detect stale or contradictory documentation;
- verify indexes and cross-links;
- update quality grades from evidence;
- find deviations from architecture and taste invariants;
- open or propose small targeted repairs;
- keep technical debt concrete and co-located with plans.

Treat repeated agent failures as missing capabilities. Add the missing tool, abstraction, documentation, or guardrail instead of merely retrying the same prompt.

## 9. Validate and hand off

Run formatting, lint, architecture, test, build, CI-equivalent, and documentation checks. Exercise at least one deliberately broken invariant to confirm that its failure message teaches remediation. Test the selected UI/observability path when configured.

Report:

- interview decisions and explicitly deferred items;
- files and executable tooling created or merged;
- validation evidence and remaining gaps;
- the current autonomy level the harness actually supports;
- the next missing capability that would unlock more reliable work.

Do not commit, push, open a pull request, merge, or deploy unless the owner separately requests it.
