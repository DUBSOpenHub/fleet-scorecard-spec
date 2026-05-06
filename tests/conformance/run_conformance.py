#!/usr/bin/env python3
"""Run Fleet Scorecard Spec conformance checks."""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys


ROOT = pathlib.Path(__file__).resolve().parents[2]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> int:
    for path in sorted(ROOT.glob("**/*.json")):
        json.loads(path.read_text())
        print(f"json_ok={path.relative_to(ROOT)}")

    validator = ROOT / "validators" / "fleet-scorecard-validate.py"
    examples = [
        ROOT / "examples" / "run-card.json",
        ROOT / "examples" / "sealed-rubric.json",
        ROOT / "examples" / "evidence-index.json",
        ROOT / "examples" / "scorecard.json",
    ]
    subprocess.run([sys.executable, str(validator), *(str(path) for path in examples)], check=True)

    readme = (ROOT / "README.md").read_text()
    spec = (ROOT / "SPEC.md").read_text()
    for question in ["What changed?", "What won?", "What failed?", "Would I run it again?"]:
        require(question in readme, f"README missing {question}")
        require(question in spec, f"SPEC missing {question}")

    require("Agent Orchestra" in readme, "README missing Agent Orchestra reference implementation")
    require("FSS-L4" in spec, "SPEC missing FSS-L4")
    print("conformance_ok=1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
