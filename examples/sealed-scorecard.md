# Fleet Scorecard: run-20260505-170318

## Verdict

| Field | Value |
|---|---|
| Status | partial |
| Fleet Score | 78/100 |
| Decision | run again with changes |
| Backend | Agent Conductor / Terminal Stampede |
| Fleet Scorecard seal | verified |
| Seal hash | `sha256:0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef` |

## Commander Status

| Commander | Status | Evidence | Caveat |
|---|---|---|---|
| commander-001 | success | 652 sub-agent ledger lines | none |
| commander-002 | partial | 297 sub-agent ledger lines | synthesized during teardown |
| commander-003 | success | 184 sub-agent ledger lines | none |
| commander-004 | partial | 31 sub-agent ledger lines | synthesized during teardown |
| commander-005 | success | 604 sub-agent ledger lines | none |

## 1. What changed?

The run created an evidence-backed hardening backlog. No code changes were left
in the working tree.

## 2. What won?

The winning recommendation was runtime hardening: cleanup traps, safer
interpolation, schema-driven tests, accurate final state, and evidence-linked
scorecards.

## 3. What failed?

The run was partial because two commanders did not produce full terminal
bundles before teardown.

## 4. Would I run it again?

Decision: run again with changes

Reason: the scorecard seal verified and the outputs were useful, but the next
run should be narrower and should finish all commanders before teardown.

Next run modification: focus only on implementing runtime hardening.

## Evidence

- `sealed/criteria.json`
- `sealed/seal.sha256`
- `evidence-index.json`
- `.stampede/run-20260505-170318/results/commander-001.json`
- `.stampede/run-20260505-170318/collab/consensus.jsonl`
