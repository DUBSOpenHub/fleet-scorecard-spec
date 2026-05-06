# Agents

## Purpose

Fleet Scorecard Spec defines a portable protocol for evaluating multi-agent CLI
fleet runs. It is not an orchestrator. It is the judgment layer that turns run
artifacts into a repeatable decision.

Use this language consistently:

- **Fleet**: the group of agents, commanders, workers, or sub-agents that worked
  on one mission.
- **Run**: one bounded execution with a run ID and evidence.
- **Scorecard**: the final artifact answering the four required questions.
- **Sealed rubric**: the pre-run scoring criteria hash used for FSS-L2+.

## Rules

- Keep the four required questions stable:
  1. What changed?
  2. What won?
  3. What failed?
  4. Would I run it again?
- Do not add cost accounting as a required question.
- Keep schemas valid JSON Schema draft 2020-12.
- Examples must validate against their matching schemas.
- Preserve the distinction between Shadow Score and Fleet Scorecard:
  Shadow Score judges output quality; Fleet Scorecard judges run usefulness and
  repeatability.
