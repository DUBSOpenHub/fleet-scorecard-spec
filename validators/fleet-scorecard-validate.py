#!/usr/bin/env python3
"""Validate Fleet Scorecard JSON artifacts against the v0.1 schemas."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCHEMA_BY_KIND = {
    "run-card": ROOT / "schemas" / "run-card.schema.json",
    "sealed-rubric": ROOT / "schemas" / "sealed-rubric.schema.json",
    "evidence-index": ROOT / "schemas" / "evidence-index.schema.json",
    "scorecard": ROOT / "schemas" / "scorecard.schema.json",
}
QUESTIONS = [
    "What changed?",
    "What won?",
    "What failed?",
    "Would I run it again?",
]


def detect_kind(path: pathlib.Path, data: dict) -> str:
    name = path.name.lower()
    if "run-card" in name:
        return "run-card"
    if "rubric" in name or "criteria" in name:
        return "sealed-rubric"
    if "evidence" in name:
        return "evidence-index"
    if "scorecard" in name:
        return "scorecard"
    if "answers" in data and "fleet_score" in data:
        return "scorecard"
    if "sources" in data and "scorecard_path" in data:
        return "evidence-index"
    if "dimensions" in data and "acceptance_checks" in data:
        return "sealed-rubric"
    if "questions" in data and "mission" in data:
        return "run-card"
    raise SystemExit(f"Could not detect Fleet Scorecard artifact type for {path}")


def fallback_validate(kind: str, data: dict) -> None:
    required = {
        "run-card": {"run_id", "mission", "backend", "created_at", "questions"},
        "sealed-rubric": {"schema_version", "run_id", "mission", "generated_at", "questions", "dimensions", "acceptance_checks"},
        "evidence-index": {"run_id", "backend", "status", "fleet_score", "decision", "scorecard_path", "sources", "caveats", "generated_at"},
        "scorecard": {"run_id", "status", "fleet_score", "decision", "backend", "mission", "questions", "answers", "evidence"},
    }[kind]
    missing = sorted(required - set(data))
    if missing:
        raise SystemExit(f"{kind} missing required fields: {', '.join(missing)}")
    if data.get("questions") != QUESTIONS:
        raise SystemExit(f"{kind} has invalid required questions")
    if "fleet_score" in data and not (0 <= int(data["fleet_score"]) <= 100):
        raise SystemExit(f"{kind} fleet_score must be 0-100")


def validate(path: pathlib.Path, explicit_kind: str | None) -> str:
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    kind = explicit_kind or detect_kind(path, data)

    try:
        import jsonschema
    except Exception:
        fallback_validate(kind, data)
        return kind

    schema = json.loads(SCHEMA_BY_KIND[kind].read_text())
    jsonschema.Draft202012Validator(schema).validate(data)
    return kind


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate Fleet Scorecard JSON artifacts.")
    parser.add_argument("paths", nargs="+", help="JSON artifact paths")
    parser.add_argument("--kind", choices=sorted(SCHEMA_BY_KIND), help="Force artifact kind")
    args = parser.parse_args(argv)

    for raw_path in args.paths:
        path = pathlib.Path(raw_path)
        kind = validate(path, args.kind)
        print(f"{kind}_ok={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
