"""Validate replayable eval inputs, never pretend to grade Agent output."""
import json
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent
SUITE = json.loads((REPO_ROOT / "evals/cases.json").read_text(encoding="utf-8"))
CASES = SUITE["cases"]
EVIDENCE_TYPES = {
    "activation_trace", "response", "tool_calls", "state_snapshot", "score_record"
}


def test_eval_entrypoints_exist_inside_repository():
    for relative in SUITE["entrypoints"].values():
        path = (REPO_ROOT / relative).resolve()
        assert path.is_relative_to(REPO_ROOT.resolve())
        assert path.is_file()


def test_eval_ids_are_unique():
    ids = [case["id"] for case in CASES]
    assert len(ids) == len(set(ids))


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["id"])
def test_eval_case_can_be_replayed_and_judged(case):
    assert case["kind"] in {"trigger", "execution"}
    assert case["expected_mode"] in {"none", "clarify", "interview", "coach"}
    for field in ("id", "prompt"):
        assert isinstance(case[field], str) and case[field].strip()
    for field in ("tags", "preconditions", "checks", "required_evidence"):
        assert isinstance(case[field], list) and case[field]
        assert all(isinstance(value, str) and value.strip() for value in case[field])
    assert set(case["required_evidence"]) <= EVIDENCE_TYPES
    assert "response" in case["required_evidence"]
    assert isinstance(case["context"], list)
    for message in case["context"]:
        assert message["role"] in {"user", "assistant"}
        assert isinstance(message["content"], str) and message["content"].strip()

    if case["kind"] == "trigger":
        assert case["entrypoints"] == ["auto"]
        assert not case["context"]
        assert "activation_trace" in case["required_evidence"]
    else:
        assert case["entrypoints"]
        assert set(case["entrypoints"]) <= SUITE["entrypoints"].keys()

    if "state" in case["tags"]:
        assert "state_snapshot" in case["required_evidence"]
        assert "tool_calls" in case["required_evidence"]
    if "scoring" in case["tags"]:
        assert "score_record" in case["required_evidence"]
        assert case["context"]


def test_suite_preserves_distinct_trigger_and_execution_coverage():
    trigger_cases = [case for case in CASES if case["kind"] == "trigger"]
    modes = {case["expected_mode"] for case in trigger_cases}
    assert {"none", "interview", "coach"} <= modes
    assert sum("trigger-positive" in case["tags"] for case in trigger_cases) >= 5
    assert sum("trigger-negative" in case["tags"] for case in trigger_cases) >= 5
    tags = {tag for case in CASES for tag in case["tags"]}
    assert {
        "trigger-positive", "trigger-negative", "entrypoint-parity", "code-only",
        "concept", "comparison", "followup", "oral-answer", "training", "scoring",
        "state", "exit", "fallback", "sources", "unknown-input", "ambiguous-input",
        "false-premise", "confirmation",
    } <= tags


def test_parity_cases_compare_multiple_explicit_entrypoints():
    for case in CASES:
        if "entrypoint-parity" in case["tags"]:
            assert case["kind"] == "execution"
            assert len(set(case["entrypoints"])) >= 2
