# 📋 Fleet Scorecard Spec

[![Spec Version](https://img.shields.io/badge/spec-v0.1.0-blue.svg)](SPEC.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Conformance Levels](https://img.shields.io/badge/conformance-FSS--L1%20%7C%20FSS--L2%20%7C%20FSS--L3%20%7C%20FSS--L4-green.svg)](SPEC.md#6-conformance-levels)

**A framework-agnostic protocol for judging whether an agent-fleet run was useful enough to repeat.**

---

## The Problem

Agent fleets produce a lot of activity: commander bundles, worker logs,
collaboration ledgers, dashboards, diffs, tests, partials, and synthesized
teardown artifacts. A run can look impressive while hiding the answer operators
actually need:

> Was this fleet run worth repeating?

Without a standard scorecard, teams rerun by vibes, bury partial failures, and
lose the best findings inside swarm noise.

## The Solution

```text
Fleet Score = change_clarity + winner_confidence + failure_accounting + repeat_decision
```

Each dimension is worth 25 points. Every conforming scorecard answers:

1. What changed?
2. What won?
3. What failed?
4. Would I run it again?

Fleet Scorecard is intentionally not cost accounting. Cost, model mix, duration,
and token use can be optional telemetry, but they are not required scorecard
questions in v0.1.

## Interpretation Scale

| Score | Level | Meaning |
|---:|---|---|
| 85-100 | ✅ Strong | Repeatable pattern |
| 70-84 | 🟢 Useful | Minor changes before repeating |
| 50-69 | 🟡 Partial | Repeat only with changes |
| 0-49 | 🔴 Weak | Redesign before repeating |

## Why "Fleet Scorecard"?

Fleet Scorecard is the after-action report for agent orchestration.

It sticks because it maps to something operators already understand: a
scorecard turns many signals into one accountable judgment. The fleet may be a
swarm, stampede, conductor, hackathon, or manual collection of Copilot CLI
sessions. The scorecard answers what happened and whether the pattern should be
used again.

## Quick Start: Add Fleet Scorecard in 5 Minutes

### Option A: Use the reference validator

```bash
python validators/fleet-scorecard-validate.py examples/scorecard.json
```

### Option B: Produce the artifacts yourself

1. **Write a run card** — run ID, mission, backend, source path.
2. **Seal the rubric** — hash the four-question criteria before final scoring.
3. **Collect evidence** — commander bundles, logs, ledgers, tests, diffs, Shadow Score.
4. **Write the scorecard** — answer the four required questions.
5. **Report the decision** — `run again`, `run again with changes`, `wait for completion`, or `do not rerun`.

Framework, model provider, and orchestration backend do not matter.

## The Fleet Scorecard Protocol

```text
 RUN CARD ──► SEAL GENERATION ──► FLEET EXECUTION ──► EVIDENCE INDEX ──► SCORECARD
               (rubric hash,       (agents,          (bundles,          (four questions,
                before final        commanders,       logs, ledgers,      score, decision)
                scoring)            workers)          tests, diffs)
```

**The critical rule:** a partial run stays partial. Heartbeats, preflights, and
dashboards are useful telemetry, but they are not proof that the fleet produced
a complete outcome.

Full protocol details: [**SPEC.md §4**](SPEC.md#4-fleet-scorecard-protocol)

## Conformance Levels

| Level | What's Required | Use Case |
|---|---|---|
| **FSS-L1** — Basic Scorecard | Four questions + status + rerun decision | Retrofitting onto any run |
| **FSS-L2** — Sealed Rubric | L1 + rubric hash verification | Agent pipelines that need anti-vibes scoring |
| **FSS-L3** — Evidence-linked | L2 + machine-readable evidence index | Auditable fleet retrospectives |
| **FSS-L4** — Automated Lifecycle | L3 + automatic finalization/teardown emission | Production agent orchestration |

## Reference Implementation

The reference Level 4 implementation is
**[Agent Orchestra](https://github.com/DUBSOpenHub/agent-orchestra)** — a
multi-agent fleet conductor for the GitHub Copilot CLI. Agent Orchestra seals a
Fleet Scorecard rubric before commander launch and writes
`.fleet-scorecards/<run-id>/scorecard.md` during teardown.

## Worked Examples

| Example | Conformance | What It Shows |
|---|---|---|
| [Basic Scorecard](examples/basic-scorecard.md) | FSS-L1 | Four-question scorecard for a partial run |
| [Sealed Scorecard](examples/sealed-scorecard.md) | FSS-L2/FSS-L3 | Seal verification plus evidence links |
| [Scorecard JSON](examples/scorecard.json) | FSS-L1 | Machine-readable answer format |
| [Evidence Index](examples/evidence-index.json) | FSS-L3 | Source map for run claims |

## Reporting Format

Fleet Scorecards can be produced in Markdown for humans and JSON for tools.

**JSON schemas:** [`schemas/`](schemas/)

```json
{
  "schema_version": "fleet-scorecard-v0.1.0",
  "run_id": "run-20260505-170318",
  "status": "partial",
  "fleet_score": 78,
  "decision": "run again with changes",
  "questions": [
    "What changed?",
    "What won?",
    "What failed?",
    "Would I run it again?"
  ],
  "answers": {
    "what_changed": "The run produced commander bundles and a hardening backlog.",
    "what_won": "Runtime hardening was the strongest consensus.",
    "what_failed": "Two commanders were partial.",
    "would_run_again": "Run again with a narrower mission."
  }
}
```

Full schema details: [**SPEC.md §5**](SPEC.md#5-reporting-format)

## Adopters

| Project | Conformance | Description |
|---|---|---|
| [Agent Orchestra](https://github.com/DUBSOpenHub/agent-orchestra) | FSS-L4 | Reference implementation — emits sealed Fleet Scorecards on teardown |

*Using Fleet Scorecard? [Open a PR](https://github.com/DUBSOpenHub/fleet-scorecard-spec/pulls) to add your project.*

## Full Specification

📄 **[Read the full spec →](SPEC.md)**

Covers: definitions, formula, protocol phases, reporting formats, conformance
levels, reference implementation, security guidance, and FAQ.

## Contributing

Fleet Scorecard is an open specification. Contributions welcome:

- **Spec changes**: Open an issue to discuss before submitting a PR.
- **New validators**: PRs for additional language validators are welcome.
- **Adopter listings**: Add your project to the Adopters table.

## License

[MIT](LICENSE) © 2026 DUBSOpenHub

Let's orchestrate! 🎼
