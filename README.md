# Special Skills

**Graph engineering and bounded-behavior plugins for coding agents.**

Special Skills is a maintained collection of agent plugins for Claude Code, Codex, and any agent that reads the [Agent Skills](https://agentskills.io) format. Every package makes agent behavior more reliable, bounded, inspectable, or repeatable, and every claim of that kind is backed by something you can run: a hook, a validator, a test, or an eval.

## Start here

| If you want to | Install |
| --- | --- |
| Decide whether a workflow needs a graph at all, then design, validate, compile, audit, or evolve one as a versioned artifact | [`graph-engineering`](./plugins/graph-engineering/) |
| Stop an agent from looping on the same failed fix and force an evidence-backed handoff | [`anti-loop`](./plugins/anti-loop/) |
| Get a receipt after every change and a verification gate before "done" | [`cleancoding`](./plugins/cleancoding/) |
| Treat fetched pages, files, and tool output as data instead of instructions | [`untrusted-content`](./plugins/untrusted-content/) |

`graph-engineering` covers execution graphs: agents, tools, typed state, edges, checkpoints, and approvals as one validated artifact. It is not a knowledge-graph or GraphRAG tool; it says so and routes those requests elsewhere.

## Install

Any agent that supports Agent Skills (Claude Code, Codex, Cursor, Copilot, Gemini CLI, and others):

```text
npx skills add MTEnt/special-skills --skill graph-engineering
```

Plugins that ship lifecycle hooks (`cleancoding`, `anti-loop`, `anti-amnesia`, `temporal-tasks`) need the plugin route so the hooks install with the skill. Add the marketplace once, then install what you need.

Claude Code:

```text
/plugin marketplace add MTEnt/special-skills
/plugin install graph-engineering@special-skills
```

Codex:

```text
codex plugin marketplace add MTEnt/special-skills
codex plugin add graph-engineering@special-skills
```

Every plugin installs the same way; substitute the name from the tables below. Plugins that ship lifecycle hooks say so in their README; review a hook before trusting it (`/hooks` in Codex). Start a new conversation after installing.

### Updating an existing installation

The repository and marketplace were renamed from `speshul-skills` to `special-skills` on 2026-09-23. Before replacing an old registration, note which plugins you installed and their installation scopes.

Claude Code: remove the former marketplace with `/plugin marketplace remove speshul-skills`, then run the new marketplace and plugin install commands above for each plugin you want. [Removing a marketplace also uninstalls its plugins](https://code.claude.com/docs/en/discover-plugins#manage-marketplaces); reinstall in the same user, project, or local scope.

Codex: run `codex plugin list --marketplace speshul-skills` to review the old plugins. For each installed plugin, run `codex plugin remove PLUGIN@speshul-skills` (replace `PLUGIN` with its name), then remove the old registration with `codex plugin marketplace remove speshul-skills`. Add the new marketplace and reinstall the plugins you want using `@special-skills` as shown above.

Update any project or managed settings that explicitly reference the old marketplace, including Claude Code's `extraKnownMarketplaces`, `enabledPlugins`, and `pluginConfigs`. Keep only the intended installation of each plugin enabled.

Start a new conversation after updating. Anti Loop and CleanCoding now use `special-` temporary-state directories; existing temporary state is not migrated.

## Packages

### Agent engineering

| Plugin | Status | What it does | Enforcement |
| --- | --- | --- | --- |
| [`graph-engineering`](./plugins/graph-engineering/) | stable | Seven modes for executable agent and workflow graphs: `select` (decide whether a graph is justified), `design`, `compile` (LangGraph, AutoGen GraphFlow, Google ADK, Microsoft Agent Framework, OpenAI Agents SDK, Claude Code `Workflow`), `audit`, `diagnose`, `optimize`, `evolve`. Framework-neutral GraphSpec with typed state, bounded cycles, approval bindings, and three assurance profiles. | Seven JSON Schemas, deterministic validator, unit tests, behavior suite with recorded results. |
| [`cleancoding`](./plugins/cleancoding/) | stable | Evidence-backed engineering: task contracts, root-cause fixes, DRY/KISS/YAGNI, the shared three-loop stop rule, receipt-based completion. | `Stop` hook requires a receipt after file changes; behavior eval suite with fixture repos. |
| [`anti-loop`](./plugins/anti-loop/) | stable | Keeps work scoped to the requested outcome and stops repeated failed attempts. | `PreToolUse` advisory on control files; stateful `PostToolUse` loop counter that enforces the stop rule. |
| [`anti-amnesia`](./plugins/anti-amnesia/) | stable | Answers "what did you just do" from the record and closes work with the shared receipt. | `SessionStart` policy hook. |
| [`untrusted-content`](./plugins/untrusted-content/) | stable | Treats fetched, file, tool, and agent content as data, never as instructions; reports injection attempts. | Prose only, by design. |
| [`temporal-tasks`](./plugins/temporal-tasks/) | stable | Difficulty scores, active-work budgets, and deterministic elapsed-time and repeated-call signals. | Four lifecycle hooks with SQLite state; tests with injected clocks. |
| [`skill-authoring`](./plugins/skill-authoring/) | stable | Writes and audits skills and plugins to this repository's standards. | `skill_lint.py`, the same linter the repository CI runs. |
| [`ai-native-sdlc`](./plugins/ai-native-sdlc/) | experimental | Coordinates software delivery across lifecycle stages using existing records and provider-neutral capability mapping. | Advisory instructions; package validation and behavior scenarios. No runtime enforcement. |

### Content and media

| Plugin | Status | What it does | Enforcement |
| --- | --- | --- | --- |
| [`marketing-hub`](./plugins/marketing-hub/) | stable | One orchestrator and 43 specialist marketing skills organized by the decision each answers, sharing a truth file and deliverable contracts. | Description-overlap check, routing scenarios, script tests. |
| [`facebook-content-studio`](./plugins/facebook-content-studio/) | experimental | Plans, packages, and approval-gates Facebook Page content with routing to Higgsfield media workflows and the Pages MCP. | Package and post-package validators in CI. |
| [`video-to-particle-field`](./plugins/video-to-particle-field/) | experimental | Reconstructs video and images as live particle or ASCII fields with stable particle identity and scroll-driven transitions. | Media inspection script; React asset. |

MCP server, installed separately:

| Tool | What it does |
| --- | --- |
| [`facebook-pages-mcp`](./facebook-pages-mcp/) | Local stdio MCP server for safely previewing, publishing, scheduling, and verifying allowlisted Facebook Page posts. Own README, tests, CI, and security policy. |

## Shared contracts

Rules that more than one package enforces live once under [`contracts/`](./contracts/) and are embedded verbatim, between marker comments, by each package that uses them. The repository validator fails when an embedded copy drifts.

| Contract | What it fixes | Used by |
| --- | --- | --- |
| [Task contract](./contracts/task-contract.schema.json) | One field set for the acceptance contract, task anchor, and budget line. | `cleancoding`, `anti-loop`, `temporal-tasks` |
| [Repeated-attempt stop rule](./contracts/loop-limit.md) | One definition of a loop and one `LOOP LIMIT REACHED` receipt. | `cleancoding`, `anti-loop` (hook-enforced) |
| [Handoff receipt](./contracts/handoff-receipt.md) | One `RECEIPT` block that closes work and that later recall reads from. | `cleancoding` (hook-enforced), `anti-amnesia` |

## Repository standards

Every package has:

- a `SKILL.md` under 10 KB with a description written as a routing key, and references loaded on demand;
- manifests for both runtimes with the same name and version, a README, and a dated CHANGELOG;
- explicit permissions, side effects, failure behavior, and safety limits;
- deterministic scripts or hooks where prompt text alone would not hold, and tests for them;
- no committed credentials, private data, generated artifacts, or machine-specific configuration.

The full standard, with layout and cross-runtime hook conventions, is in [`skill-authoring`](./plugins/skill-authoring/skills/skill-authoring/references/package-standards.md).

## Verify locally

```text
python scripts/validate_repo.py --strict-overlap
python -m unittest discover -s scripts/tests
for p in plugins/*/; do [ -d "$p/tests" ] && (cd "$p" && python -m unittest discover -s tests); done
```

CI runs the same commands on Linux and Windows for each pull request, plus the package-specific suites listed in [`.github/workflows/ci.yml`](./.github/workflows/ci.yml).

## Contributing

- Use lowercase, hyphen-separated package and skill names; the skill name equals its directory name.
- Keep packages self-contained; the only cross-package dependency allowed is a verbatim contract embed.
- Document every external side effect and deliberately unsupported operation.
- Test executable code without calling live production APIs.
- Run the validator and the affected test suites before opening a pull request.

Before using any package with sensitive data, credentials, external messaging, destructive operations, or production systems, inspect its instructions and executable components yourself.

## License

MIT. See [LICENSE](./LICENSE).
