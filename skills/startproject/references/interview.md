# Harness initialization interview

Use this bank conversationally. Ask four to seven questions per round, summarize what you learned, and follow up only where an answer changes the scaffold. Do not present all questions at once.

## Round 1: Product intent

Ask:

1. What is the product's canonical name, and what does it do in one sentence?
2. Who are the primary users, and what problem are they trying to solve?
3. What are the first one to three user workflows the product must support?
4. What observable outcomes will show that each workflow works?
5. What is explicitly outside the first release?
6. Which decisions must remain human-owned even if agents implement the product?

Follow up when users, workflows, or success criteria are abstract. Convert “make it good” into observable behavior without inventing business goals.

## Round 2: Repository and initial scaffold

First use repository inspection to answer factual questions. Then ask:

1. Is this an empty repository, a new repository with a chosen stack, or an existing application?
2. Which application framework, language, and repository shape should the project use?
3. Which package manager and runtime versions should be pinned?
4. Which formatter, linter, type checker, test runner, and build command should be authoritative?
5. Which CI system should run the same checks, and which branches or pull requests should trigger it?
6. Are there existing templates, standard tools, or repository-embedded skills agents must use directly?

If the owner has no stack preference, ask about the product's runtime needs before proposing a small, stable, inspectable stack.

## Round 3: Architecture and taste

Ask:

1. What business domains exist now, and what responsibility belongs to each?
2. Should every domain use a fixed layer sequence? The article's example is Types → Config → Repo → Service → Runtime → UI; keep it, modify it, or define another sequence?
3. Which cross-cutting concerns must enter through a provider boundary (for example auth, connectors, telemetry, or feature flags)?
4. What data enters from users, APIs, files, queues, or databases, and where must its shape be parsed or validated?
5. Which dependency edges must be forbidden across layers or domains?
6. Which “taste” rules should be mechanical: structured logging, schema/type naming, file-size limits, platform reliability, shared utilities, or others?
7. What should each violation message tell an agent to do to fix it?

Distinguish a preference from an invariant. Only invariants become blocking checks.

## Round 4: Application legibility

Ask:

1. How should an agent boot one isolated application instance per git worktree?
2. Which user interfaces must agents inspect, and should they have DOM snapshots, screenshots, navigation, or video?
3. Where should isolated logs, metrics, and traces come from, and how should agents query them?
4. Which critical journeys should agents be able to drive end to end?
5. Which measurable targets matter, such as startup time, request latency, error rate, or maximum span duration?
6. Which external systems cannot be isolated, and what safe substitutes or fixtures are needed?

If a capability is premature, record “deferred,” why, and the trigger for adding it.

## Round 5: Work loop and autonomy

Ask:

1. What should agents own: product code, tests, CI, release tooling, docs, design history, evals, reviews, repository scripts, or deployment definitions?
2. Should the repository adopt the article's “no manually-written code” constraint, or may humans edit code directly?
3. What should humans own: prioritization, acceptance criteria, user feedback, architecture judgment, security, legal, or production approval?
4. What local and remote reviews should occur before a change is considered complete?
5. What evidence must an agent attach for bug fixes or UI changes?
6. What failures may be repaired automatically, and what conditions require human escalation?
7. What merge philosophy fits the expected throughput and risk: conservative gates, balanced gates, or short-lived PRs with cheap follow-up repair?
8. May agents commit, push, open PRs, merge, or deploy, and under what explicit limits?

Never infer publication or production authority from a desire for autonomy.

## Round 6: Product quality and garbage collection

Ask:

1. What product and interaction principles belong in `DESIGN.md` and `FRONTEND.md`?
2. Which quality areas should be graded, and what evidence makes a grade trustworthy?
3. What reliability promises, failure modes, and recovery expectations matter now?
4. What sensitive data, trust boundaries, and security rules must agents understand?
5. What are the repository's initial golden principles—the patterns agents should replicate everywhere?
6. How often should documentation and architecture be gardened, and what should the maintenance task inspect?
7. How should technical debt be recorded, prioritized, and converted into small repair work?
8. Is there a database schema now? If so, what is its authoritative source and generation command?

## Confirmation gate

Before writing files, summarize:

- product, users, workflows, outcomes, and non-goals;
- stack, repository shape, tools, commands, and CI;
- domains, layers, providers, boundary rules, and enforced invariants;
- worktree, UI, observability, journey, and performance capabilities;
- agent/human ownership, review, merge, escalation, and publication authority;
- design, quality, reliability, security, schema, golden principles, and maintenance cadence;
- every deferred item and its activation trigger.

Ask the owner to confirm or correct the summary. Missing answers are not confirmation.
