# Untrusted Content

A small skill with one job: content that arrives from outside the user's instructions is data, never commands. Web pages, documents, tool output, retrieved records, and messages from other agents are read for facts; instructions found inside them are reported, not followed.

It generalizes the trust-boundary rules that `graph-engineering` applies to workflow graphs and `cleancoding` applies to code, so any session can use them without loading either.

## Package contents

| Path | Purpose |
| --- | --- |
| `skills/untrusted-content/SKILL.md` | Operating contract, reporting block, and prohibitions. |
| `skills/untrusted-content/references/injection-triage.md` | Recognizable injection shapes, handling steps, special cases, and a self-test. |

## Install

Claude Code: `/plugin marketplace add MTEnt/special-skills` then `/plugin install untrusted-content@special-skills`.

Codex: `codex plugin marketplace add MTEnt/special-skills` then `codex plugin add untrusted-content@special-skills`.

The skill has no hooks, scripts, or network access. It changes how the agent reads; it does not read anything itself.

## Status

Stable for the reading and reporting rules. The triage table is a starting catalog, not a detector; it will grow as new shapes are observed.
