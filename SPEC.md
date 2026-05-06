# Fleet Scorecard Spec v0.1

## 1. Overview

Fleet Scorecard Spec (FSS) defines a portable artifact format and conformance
model for evaluating multi-agent fleet runs.

A fleet run is any bounded execution where one or more agents, commanders,
workers, or sub-agents work toward a shared mission and leave evidence.

The scorecard MUST answer:

1. What changed?
2. What won?
3. What failed?
4. Would I run it again?

## 2. Goals

FSS exists to make fleet runs:

- comparable across time and backends
- honest about partial and failed work
- evidence-linked rather than vibes-based
- reusable as operating history
- easy to teach from the CLI

## 3. Non-goals

FSS v0.1 does not require:

- cost accounting
- provider billing details
- model token accounting
- a hosted service
- a specific orchestrator
- a specific agent framework

Implementations MAY include optional operational telemetry, but they MUST NOT
add "what did it cost?" as a required v0.1 scorecard question.

## 4. Required terms

| Term | Definition |
|---|---|
| Run | One bounded execution with a run ID and mission |
| Fleet | The set of agents, commanders, workers, or sub-agents participating in the run |
| Run card | The pre-run or early-run metadata describing mission, backend, and expected output |
| Sealed rubric | A pre-finalization criteria document hashed before scoring |
| Evidence index | A machine-readable list of files, logs, ledgers, diffs, tests, or bundles used by the scorecard |
| Scorecard | The final human-readable and/or machine-readable judgment artifact |

## 5. Status values

Implementations MUST use one of these top-level run statuses:

| Status | Meaning |
|---|---|
| `success` | Expected outputs exist and no critical fleet failures are present |
| `partial` | Useful evidence exists, but outputs, commanders, tests, or proof are incomplete |
| `failed` | No reliable outcome was produced or the launch/finalization failed |
| `running` | The run is not final and should not be treated as a completed scorecard |

Implementations MUST NOT label a partial run as `success`.

## 6. Decision values

Implementations MUST use one of these rerun decisions:

| Decision | Meaning |
|---|---|
| `run again` | The pattern is strong enough to repeat as-is |
| `run again with changes` | The run was useful, but the next run needs a modification |
| `wait for completion` | The run is still active or final evidence is incomplete |
| `do not rerun` | The run should be redesigned before another attempt |

## 7. Score model

Fleet Score is a 0-100 integer.

| Dimension | Points |
|---|---:|
| Change clarity | 25 |
| Winner confidence | 25 |
| Failure accounting | 25 |
| Repeat decision | 25 |

Score bands:

| Score | Meaning |
|---:|---|
| 85-100 | Strong run; repeatable pattern |
| 70-84 | Useful run; minor changes before repeating |
| 50-69 | Partial value; repeat only with changes |
| 0-49 | Weak run; redesign before repeating |

## 8. Required scorecard sections

A human-readable scorecard MUST include:

```markdown
# Fleet Scorecard: RUN_ID

## Verdict

## Commander Status

## 1. What changed?

## 2. What won?

## 3. What failed?

## 4. Would I run it again?

## Evidence
```

`Commander Status` MAY be renamed for non-commander systems, but it MUST still
show the participating fleet units and their statuses.

## 9. Sealed rubric

FSS-L2 and higher implementations MUST create a sealed rubric before final
scoring. For fully automated runs, the rubric SHOULD be created before the
fleet starts.

The rubric MUST include:

- schema version
- run ID
- mission
- generated timestamp
- the four required questions
- scoring dimensions
- acceptance checks

The implementation MUST hash the rubric with SHA-256 and store the hash beside
the rubric. During final scoring, the implementation MUST recompute the hash and
record whether the seal verified.

The sealed rubric MAY be visible after the run. Unlike Shadow Score, FSS does
not require hidden criteria; the important property is pre-finalization
immutability.

## 10. Evidence index

FSS-L3 and higher implementations MUST produce a machine-readable evidence
index. It MUST include:

- run ID
- backend
- repository or workspace path
- source run path
- final status
- Fleet Score
- decision
- seal verification result when applicable
- scorecard path
- evidence sources
- caveats

Evidence sources SHOULD identify their kind, such as:

- `run_state`
- `commander_bundle`
- `collab_ledger`
- `git_diff`
- `test_output`
- `shadow_score`
- `log`
- `scorecard`

## 11. Automation lifecycle

FSS-L4 implementations MUST integrate with the run lifecycle:

1. Generate or update the run card.
2. Create and hash the sealed rubric.
3. Collect run evidence.
4. Generate the final scorecard at finalization or teardown.
5. Link the source run state to the scorecard.

The scorecard generator MUST tolerate partial evidence and still produce an
honest `partial` or `failed` result.

## 12. File layout

Recommended layout:

```text
.fleet-scorecards/
  RUN_ID/
    run-card.json
    sealed/
      criteria.json
      seal.sha256
    evidence-index.json
    scorecard.md
```

This layout is recommended, not required. Implementations MAY use another path
if they expose equivalent artifacts.

## 13. Security and safety

Implementations MUST:

- avoid exposing secrets from logs or command output
- avoid treating heartbeat/preflight success as final success evidence
- preserve partial and failed statuses
- avoid mutating source run evidence while scoring, except to link generated
  scorecard metadata

Implementations SHOULD:

- redact token-like strings from log snippets
- write JSON atomically
- keep generated scorecards out of source commits by default

## 14. Conformance summary

| Level | Requires |
|---|---|
| FSS-L1 | Required questions and status/decision language |
| FSS-L2 | FSS-L1 plus sealed rubric and hash verification |
| FSS-L3 | FSS-L2 plus evidence index and cited claims |
| FSS-L4 | FSS-L3 plus automatic lifecycle integration |
