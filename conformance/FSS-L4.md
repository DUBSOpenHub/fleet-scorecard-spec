# FSS-L4: Automated Lifecycle

FSS-L4 integrates Fleet Scorecard into the run lifecycle.

## Requirements

An implementation is FSS-L4 conformant when it satisfies FSS-L3 and:

- Creates or updates the run card automatically.
- Seals the rubric before fleet work begins, when possible.
- Emits the final scorecard during finalization or teardown.
- Links source run state to the generated scorecard.
- Produces an honest scorecard even when the run is partial or failed.
- Allows manual regeneration without launching new agents.

## Recommended lifecycle

```text
run card -> sealed rubric -> fleet work -> evidence index -> scorecard -> source run link
```

## Reference implementation behavior

Agent Orchestra's reference implementation:

- writes overlays under `.fleet-scorecards/<run-id>/`
- seals `sealed/criteria.json`
- verifies `sealed/seal.sha256`
- writes `evidence-index.json`
- writes `scorecard.md`
- links the scorecard path back into `.stampede/<run-id>/state.json`
