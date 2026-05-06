# FSS-L2: Sealed Rubric

FSS-L2 adds a sealed rubric to the basic scorecard.

## Requirements

An implementation is FSS-L2 conformant when it satisfies FSS-L1 and:

- Creates a rubric before final scoring.
- Includes the four required questions in the rubric.
- Includes scoring dimensions and acceptance checks.
- Hashes the rubric with SHA-256.
- Recomputes the hash during final scoring.
- Records whether the seal verified.

## Recommended artifacts

```text
sealed/
  criteria.json
  seal.sha256
scorecard.md
```

## Notes

FSS-L2 sealing is about immutability and timing. It does not require the rubric
to stay hidden from the operator after the run.
