# FSS-L3: Evidence-linked Scorecard

FSS-L3 links scorecard claims to run evidence.

## Requirements

An implementation is FSS-L3 conformant when it satisfies FSS-L2 and:

- Produces an `evidence-index.json` or equivalent machine-readable evidence map.
- Lists the source run path or artifact location.
- Cites sources for winner claims and failure claims.
- Distinguishes heartbeats/preflights from final success evidence.
- Records caveats, partial commanders, missing outputs, or failed tests.

## Recommended artifacts

```text
run-card.json
sealed/
  criteria.json
  seal.sha256
evidence-index.json
scorecard.md
```

## Evidence source examples

- commander bundle
- worker result
- collaboration ledger
- run state
- git diff
- test output
- Shadow Score scorecard
- log excerpt
