"""Candidate manifest and release gate for prompt updates."""

from __future__ import annotations

from typing import Any, Dict


def build_candidate_manifest(
    optimization: Dict[str, Any], learning_signal: Dict[str, Any]
) -> Dict[str, Any]:
    return {
        "artifact_type": "system_prompt_patch",
        "source_case_ids": list(learning_signal.get("source_case_ids", [])),
        "scope": learning_signal.get("scope", "system_prompt"),
        "rationale": optimization.get("rationale") or learning_signal.get("diagnosis", ""),
        "diff": optimization.get("diff", ""),
        "edits": list(optimization.get("edits", [])),
        "target_rule": "transfer only on explicit human request or urgent safety event; otherwise explain policy and seek compliant alternatives",
        "status": "candidate",
    }


def evaluate_release_gate(
    before: Dict[str, Any], after: Dict[str, Any], manifest: Dict[str, Any]
) -> Dict[str, Any]:
    h_b = before.get("holdout") if isinstance(before, dict) else None
    h_a = after.get("holdout") if isinstance(after, dict) else None
    b_b = before.get("boundary") if isinstance(before, dict) else None
    b_a = after.get("boundary") if isinstance(after, dict) else None
    holdout_before, holdout_total = h_b if isinstance(h_b, (list, tuple)) and len(h_b) == 2 else (0, 0)
    holdout_after, _ = h_a if isinstance(h_a, (list, tuple)) and len(h_a) == 2 else (0, 0)
    boundary_before, boundary_total = b_b if isinstance(b_b, (list, tuple)) and len(b_b) == 2 else (0, 0)
    boundary_after, _ = b_a if isinstance(b_a, (list, tuple)) and len(b_a) == 2 else (0, 0)
    valid_metrics = (
        isinstance(h_b, (list, tuple)) and len(h_b) == 2
        and isinstance(h_a, (list, tuple)) and len(h_a) == 2
        and isinstance(b_b, (list, tuple)) and len(b_b) == 2
        and isinstance(b_a, (list, tuple)) and len(b_a) == 2
    )

    checks = {
        "valid_metrics": valid_metrics,
        "patch_is_nonempty": bool(manifest.get("diff", "").strip()) if isinstance(manifest, dict) else False,
        "patch_is_auditable_old_to_new_edit": bool(manifest.get("edits")) and all(
            isinstance(edit, dict)
            and isinstance(edit.get("old_str"), str) and bool(edit["old_str"])
            and isinstance(edit.get("new_str"), str) and bool(edit["new_str"])
            for edit in manifest.get("edits", [])
        ) if isinstance(manifest, dict) else False,
        "source_cases_are_recorded": bool(manifest.get("source_case_ids")),
        "holdout_did_not_regress": holdout_after >= holdout_before,
        "boundary_improved": boundary_after > boundary_before,
    }
    accepted = all(checks.values())
    return {
        "decision": "release_to_canary" if accepted else "reject_candidate",
        "accepted": accepted,
        "checks": checks,
        "metrics": {
            "holdout_before": [holdout_before, holdout_total],
            "holdout_after": [holdout_after, holdout_total],
            "boundary_before": [boundary_before, boundary_total],
            "boundary_after": [boundary_after, boundary_total],
        },
    }
