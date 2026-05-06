# Fleet Scorecard Spec

**Fleet Scorecard Spec (FSS)** is a portable protocol for judging agent-fleet
runs from the CLI. It answers one operational question:

> Was this fleet run useful enough to repeat?

Every conforming scorecard answers four questions:

1. What changed?
2. What won?
3. What failed?
4. Would I run it again?

Fleet Scorecard is intentionally not cost accounting. Cost, model mix, and
duration may appear as optional telemetry, but they are not required scorecard
questions in v0.1.

## Why this exists

Agent orchestration produces noisy artifacts: commander bundles, logs,
collaboration ledgers, run state, test output, diffs, and partial failures.
Fleet Scorecard turns that noise into one repeatable judgment.

| Problem | Fleet Scorecard answer |
|---|---|
| Runs are hard to compare | Use the same four questions every time |
| Successful-looking runs hide partials | Require explicit failure accounting |
| Best output gets lost in the swarm | Name what won and why |
| Operators rerun by vibes | End with a clear rerun decision |

## Relationship to Shadow Score

Fleet Scorecard complements, but does not replace, Shadow Score.

| Protocol | Primary question |
|---|---|
| Shadow Score | Was the final output good against sealed quality gates? |
| Fleet Scorecard | Was the fleet run useful, honest, and worth repeating? |

Shadow Score can be one evidence source inside a Fleet Scorecard.

## Conformance levels

| Level | Name | Requirement |
|---|---|---|
| FSS-L1 | Basic Scorecard | Produces the four-question scorecard |
| FSS-L2 | Sealed Rubric | Creates and hashes the rubric before final scoring |
| FSS-L3 | Evidence-linked | Links claims to run artifacts, ledgers, logs, diffs, or tests |
| FSS-L4 | Automated Lifecycle | Emits the scorecard automatically at finalization or teardown |

See [`conformance/`](conformance/) for the detailed checklists.

## Repository layout

```text
fleet-scorecard-spec/
  SPEC.md
  schemas/
    run-card.schema.json
    sealed-rubric.schema.json
    evidence-index.schema.json
    scorecard.schema.json
  examples/
    run-card.json
    sealed-rubric.json
    evidence-index.json
    scorecard.json
    basic-scorecard.md
    sealed-scorecard.md
  conformance/
    FSS-L1.md
    FSS-L2.md
    FSS-L3.md
    FSS-L4.md
```

## Reference implementation

The first implementation is Agent Orchestra's `bin/fleet-scorecard`, which
generates `.fleet-scorecards/<run-id>/scorecard.md` from `.stampede/<run-id>/`
artifacts.

## Status

This is a v0.1 draft. The four required questions, core status words, and
conformance levels are expected to stay stable; schemas may evolve before v1.0.
