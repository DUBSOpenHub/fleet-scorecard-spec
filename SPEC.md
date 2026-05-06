# Fleet Scorecard Specification

**Version:** 0.1.0  
**Status:** Draft  
**Date:** 2026-05-06  
**Authors:** DUBSOpenHub  
**License:** MIT

---

## 1. Abstract

**Fleet Scorecard** is a framework-agnostic protocol for judging whether an
agent-fleet run was useful enough to repeat. It converts run artifacts,
commander bundles, logs, collaboration ledgers, tests, diffs, and partial
failures into one accountable scorecard.

Every conforming scorecard answers four questions:

1. What changed?
2. What won?
3. What failed?
4. Would I run it again?

---

## 2. Motivation

### The Swarm Noise Problem

Multi-agent orchestration can generate impressive volume without a clear
decision. A run may launch many agents, write many logs, and update dashboards,
yet still leave the operator unsure whether the run should be trusted or
repeated.

### What's Missing

The industry lacks a standardized artifact for answering:

> Was this agent-fleet run useful, honest, and repeatable?

Existing signals fall short:

| Signal | Limitation |
|---|---|
| Heartbeats | Prove liveness, not outcome quality |
| Preflights | Prove launch readiness, not run usefulness |
| Dashboards | Show activity, but not final judgment |
| Commander bundles | Useful individually, hard to compare as a run |
| LLM summaries | Can hide partials unless constrained by a rubric |

### Fleet Scorecard Solves This

Fleet Scorecard introduces a repeatable after-action protocol. It forces every
run to name what changed, identify what won, preserve what failed, and decide
whether the pattern should be used again.

---

## 3. Definitions

### 3.1 Roles

| Role | Responsibility | Information Access |
|---|---|---|
| **Operator** | Defines the mission and decides whether to rerun | Full context |
| **Fleet** | Performs the work through agents, commanders, workers, or sub-agents | Mission and assigned context |
| **Evaluator** | Reads evidence and writes the scorecard | Run artifacts and scoring rubric |
| **Validator** | Verifies schema, seal, and evidence links | Scorecard artifacts and source run files |

### 3.2 Artifacts

| Artifact | Description |
|---|---|
| **Run card** | Pre-run or early-run metadata: run ID, mission, backend, source path |
| **Sealed rubric** | Pre-finalization criteria document hashed before scoring |
| **Evidence index** | Machine-readable map of source files, logs, ledgers, tests, and bundles |
| **Scorecard** | Final human-readable and/or machine-readable judgment artifact |

### 3.3 Fleet Score Formula

```text
Fleet Score = change_clarity + winner_confidence + failure_accounting + repeat_decision
```

Each dimension is worth 25 points.

| Dimension | Points | Meaning |
|---|---:|---|
| Change clarity | 25 | The scorecard explains concrete artifacts, code, decisions, or knowledge produced |
| Winner confidence | 25 | The scorecard names a winning output, idea, commander, or recommendation with evidence |
| Failure accounting | 25 | The scorecard honestly labels partials, missing outputs, weak evidence, and failures |
| Repeat decision | 25 | The scorecard gives a clear rerun decision and next-run modification |

### 3.4 Interpretation Scale

| Score | Level | Indicator | Meaning |
|---:|---|---|---|
| 85-100 | Strong | ✅ | Repeatable pattern |
| 70-84 | Useful | 🟢 | Minor changes before repeating |
| 50-69 | Partial | 🟡 | Repeat only with changes |
| 0-49 | Weak | 🔴 | Redesign before repeating |

### 3.5 Required Status Values

| Status | Meaning |
|---|---|
| `success` | Expected outputs exist and no critical fleet failures are present |
| `partial` | Useful evidence exists, but outputs, commanders, tests, or proof are incomplete |
| `failed` | No reliable outcome was produced or launch/finalization failed |
| `running` | The run is not final and should not be treated as a completed scorecard |

Implementations MUST NOT label a partial run as `success`.

### 3.6 Required Decision Values

| Decision | Meaning |
|---|---|
| `run again` | The pattern is strong enough to repeat as-is |
| `run again with changes` | The run was useful, but the next run needs modification |
| `wait for completion` | The run is still active or final evidence is incomplete |
| `do not rerun` | The run should be redesigned before another attempt |

---

## 4. Fleet Scorecard Protocol

The Fleet Scorecard Protocol is the lifecycle methodology that produces a valid
Fleet Scorecard.

### 4.1 Run Card

**Input:** Mission, backend, repository or workspace path.  
**Output:** Run card.

Requirements:

1. The run card MUST identify the run ID.
2. The run card MUST include the mission.
3. The run card SHOULD include backend, repo path, source run path, and expected
   scorecard questions.

### 4.2 Seal Generation

**Input:** Mission and scorecard questions.  
**Output:** Sealed rubric and SHA-256 hash.

Requirements for FSS-L2+:

1. The rubric MUST include the four required questions.
2. The rubric MUST include scoring dimensions and acceptance checks.
3. The rubric MUST be hashed with SHA-256.
4. The final scorecard MUST record whether the seal verified.

Unlike Shadow Score, Fleet Scorecard does not require the rubric to stay hidden
after the run. The core invariant is pre-finalization immutability.

### 4.3 Fleet Execution

**Input:** Mission and orchestrator-specific manifests.  
**Output:** Run artifacts.

Fleet execution is backend-agnostic. Valid backends include:

- Agent Orchestra
- Agent Conductor
- Terminal Stampede
- Swarm Command
- HiveSwarm / Hive1K
- manual Copilot CLI fleet sessions

### 4.4 Evidence Collection

**Input:** Run artifacts.  
**Output:** Evidence index.

FSS-L3+ implementations MUST collect evidence from the run. Evidence MAY
include:

- run state
- commander bundles
- worker results
- collaboration ledgers
- git diffs
- test output
- Shadow Score reports
- logs
- final synthesis documents

Heartbeats and preflights MAY be included as context, but MUST NOT be treated as
proof of final success by themselves.

### 4.5 Scorecard Generation

**Input:** Run card, rubric, evidence index, source artifacts.  
**Output:** Final scorecard.

The scorecard MUST answer all four required questions and MUST produce:

- status
- Fleet Score
- decision
- caveats
- evidence references

When evidence is incomplete, the implementation MUST still produce an honest
`partial` or `failed` scorecard.

### 4.6 Lifecycle Automation

FSS-L4 implementations MUST integrate with the run lifecycle:

1. Generate or update the run card.
2. Create and hash the sealed rubric.
3. Collect run evidence.
4. Generate the final scorecard at finalization or teardown.
5. Link the source run state to the scorecard.

---

## 5. Reporting Format

Implementations SHOULD produce both Markdown and JSON-compatible artifacts.

### 5.1 Markdown Format

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

`Commander Status` MAY be renamed for non-commander systems, but the scorecard
MUST show the participating fleet units and their statuses.

### 5.2 JSON Format

```json
{
  "schema_version": "fleet-scorecard-v0.1.0",
  "run_id": "run-20260505-170318",
  "status": "partial",
  "fleet_score": 78,
  "decision": "run again with changes",
  "backend": "Agent Conductor / Terminal Stampede",
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

### 5.3 Required Schemas

This repository defines JSON Schema draft 2020-12 schemas for:

- `run-card.schema.json`
- `sealed-rubric.schema.json`
- `evidence-index.schema.json`
- `scorecard.schema.json`

---

## 6. Conformance Levels

| Level | Name | Requires |
|---|---|---|
| **FSS-L1** | Basic Scorecard | Four questions, status, Fleet Score, rerun decision |
| **FSS-L2** | Sealed Rubric | FSS-L1 plus rubric hash and seal verification |
| **FSS-L3** | Evidence-linked | FSS-L2 plus evidence index and cited claims |
| **FSS-L4** | Automated Lifecycle | FSS-L3 plus automatic scorecard emission at finalization/teardown |

Detailed checklists live in [`conformance/`](conformance/).

---

## 7. Reference Implementations and Adopters

| Project | Conformance | Description |
|---|---|---|
| [Agent Orchestra](https://github.com/DUBSOpenHub/agent-orchestra) | FSS-L4 | Reference implementation — emits sealed Fleet Scorecards on teardown |

---

## 8. Relationship to Shadow Score

Fleet Scorecard complements [Shadow Score](https://github.com/DUBSOpenHub/shadow-score-spec).

| Protocol | Primary question |
|---|---|
| Shadow Score | Was the final output good against sealed quality gates? |
| Fleet Scorecard | Was the fleet run useful enough to repeat? |

Shadow Score MAY be an evidence source inside Fleet Scorecard. Fleet Scorecard
MUST NOT replace Shadow Score when the goal is sealed output-quality validation.

---

## 9. Security and Safety

Implementations MUST:

- avoid exposing secrets from logs or command output
- preserve partial and failed statuses
- avoid treating heartbeat/preflight success as final success evidence
- avoid mutating source run evidence while scoring, except to link generated
  scorecard metadata

Implementations SHOULD:

- redact token-like strings from log snippets
- write JSON atomically
- keep generated scorecards out of source commits by default

---

## 10. FAQ

### Is Fleet Scorecard a replacement for Shadow Score?

No. Shadow Score judges output quality against sealed tests. Fleet Scorecard
judges whether the fleet run was useful, honest, and repeatable.

### Is cost part of the required scorecard?

No. Cost can be optional telemetry, but v0.1 intentionally keeps the required
questions focused on outcome quality and repeatability.

### Can a run with partial commanders score well?

Yes, but it must remain `partial`. A partial run can produce useful evidence,
but the status must not be upgraded to `success`.

### Does FSS require Agent Orchestra?

No. Agent Orchestra is the first reference implementation, but the spec is
backend-agnostic.
