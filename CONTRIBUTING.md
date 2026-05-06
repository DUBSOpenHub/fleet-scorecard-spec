# Contributing

Fleet Scorecard is an open specification. Contributions are welcome.

## Contribution types

- **Spec changes**: Open an issue first for changes to required questions,
  status values, decision values, conformance levels, or schemas.
- **Validators**: Add validators for additional languages or CI systems.
- **Examples**: Add real scorecards, evidence indexes, and backend examples.
- **Adopters**: Add your project to the Adopters table in `README.md`.

## Local validation

```bash
python tests/conformance/run_conformance.py
python validators/fleet-scorecard-validate.py examples/scorecard.json
```

## Compatibility rules

- Keep the four required questions stable.
- Do not add cost accounting as a required question.
- Keep JSON schemas valid draft 2020-12.
- Update examples when schemas change.
- Preserve the distinction between Shadow Score and Fleet Scorecard.
