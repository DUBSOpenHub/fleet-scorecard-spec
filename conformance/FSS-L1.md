# FSS-L1: Basic Scorecard

FSS-L1 is the minimum useful Fleet Scorecard level.

## Requirements

An implementation is FSS-L1 conformant when it:

- Produces one final scorecard per completed run.
- Answers all four required questions:
  1. What changed?
  2. What won?
  3. What failed?
  4. Would I run it again?
- Uses one top-level status: `success`, `partial`, `failed`, or `running`.
- Uses one decision: `run again`, `run again with changes`,
  `wait for completion`, or `do not rerun`.
- Does not call partial evidence a success.

## Recommended artifacts

```text
scorecard.md
```

## Non-requirements

FSS-L1 does not require sealed rubrics, evidence indexes, or lifecycle
automation.
