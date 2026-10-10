
import re
from typing import Any


def _collect_text(value: Any) -> list[str]:
    """Collect text recursively from a blueprint dictionary."""
    texts = []

    if isinstance(value, dict):
        for key, item in value.items():
            texts.append(str(key).replace("_", " "))
            texts.extend(_collect_text(item))

    elif isinstance(value, (list, tuple)):
        for item in value:
            texts.extend(_collect_text(item))

    elif isinstance(value, str):
        texts.append(value)

    return texts


def validate_blueprint_consistency(
    blueprint: dict,
    duration_weeks: int,
) -> dict:
    """
    Run deterministic quality checks on a generated blueprint.
    Warnings do not reject an otherwise valid blueprint.
    """
    warnings = []
    checks = []

    # 1. Confirm all expected sections exist.
    required_sections = [
        "project_idea",
        "feasibility",
        "scope",
        "technology",
        "planning",
        "risk_assessment",
    ]

    missing = [
        section
        for section in required_sections
        if section not in blueprint or blueprint[section] is None
    ]

    if missing:
        warnings.append(
            "Missing blueprint sections: " + ", ".join(missing)
        )
        checks.append({
            "name": "required_sections",
            "passed": False,
        })
    else:
        checks.append({
            "name": "required_sections",
            "passed": True,
        })

    # 2. Check that the plan fits the requested duration.
    planning = blueprint.get("planning") or {}

    if isinstance(planning, dict):
        total_days = planning.get("total_duration_days")
        phases = planning.get("phases", [])

        if isinstance(total_days, (int, float)):
            if total_days > duration_weeks * 7:
                warnings.append(
                    f"Plan duration ({total_days} days) exceeds "
                    f"the requested {duration_weeks}-week limit."
                )

            if isinstance(phases, list) and phases:
                phase_days = [
                    phase.get("duration_days")
                    for phase in phases
                    if isinstance(phase, dict)
                    and isinstance(
                        phase.get("duration_days"), (int, float)
                    )
                ]

                if len(phase_days) == len(phases):
                    if sum(phase_days) != total_days:
                        warnings.append(
                            "The sum of phase durations does not "
                            "match total_duration_days."
                        )

                    checks.append({
                        "name": "phase_duration_sum",
                        "passed": sum(phase_days) == total_days,
                    })

            checks.append({
                "name": "requested_timeline",
                "passed": total_days <= duration_weeks * 7,
            })
        else:
            warnings.append(
                "Could not verify the plan timeline because "
                "total_duration_days is missing or invalid."
            )
            checks.append({
                "name": "requested_timeline",
                "passed": False,
            })

    # 3. Look for common technology-stack conflicts.
    full_text = " ".join(_collect_text(blueprint)).lower()

    if "streamlit" in full_text and "tailwind css" in full_text:
        warnings.append(
            "Review the technology stack: Streamlit and Tailwind CSS "
            "are not normally integrated as a standard frontend stack. "
            "Confirm whether a separate web frontend is intended."
        )

    # 4. Flag statements that may confuse proposed work with
    # completed experiments or verified results.
    claim_patterns = [
        (
            r"\b(?:achieved|attained|obtained)\s+"
            r"(?:an?\s+)?\d+(?:\.\d+)?\s*%?",
            "A numerical achievement is mentioned. Verify that "
            "it is supported by actual experimental results.",
        ),
        (
            r"\b(?:trained|fine[- ]tuned)\s+"
            r"(?:our|the|a|an|custom|proprietary)\s+"
            r"(?:own\s+)?(?:machine learning\s+|deep learning\s+)?"
            r"model\b",
            "A trained or fine-tuned model is mentioned. Verify "
            "that the training or fine-tuning was actually performed.",
        ),
        (
            r"\b(?:achieved|recorded|measured)\s+"
            r"(?:a\s+)?(?:mape|rmse|mae|accuracy)\b",
            "A measured model result is mentioned. Verify it against "
            "actual evaluation results.",
        ),
    ]

    for pattern, message in claim_patterns:
        if re.search(pattern, full_text):
            warnings.append(message)

    # Remove duplicate warnings while preserving order.
    warnings = list(dict.fromkeys(warnings))

    return {
        "passed": len(warnings) == 0,
        "checks": checks,
        "warnings": warnings,
        "warning_count": len(warnings),
        "note": (
            "Automated checks identify potential issues; "
            "they do not prove that every AI-generated claim is true."
        ),
    }
