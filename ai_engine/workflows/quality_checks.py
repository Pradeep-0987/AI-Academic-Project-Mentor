def validate_blueprint_consistency(blueprint: dict, duration_weeks: int) -> dict:
    errors, warnings = [], []
    for section in ("feasibility", "scope", "technology", "planning", "risk"):
        if not blueprint.get(section):
            errors.append(f"Missing section: {section}")
    planning = blueprint.get("planning") or {}
    if planning:
        if planning.get("total_duration_weeks") != duration_weeks:
            errors.append("Planning duration does not match requested duration.")
        phases = planning.get("phases") or []
        if not phases:
            errors.append("Planning has no phases.")
        for phase in phases:
            name = phase.get("phase_name", "Unnamed phase")
            start, length = phase.get("start_week", 0), phase.get("duration_weeks", 0)
            if start < 1 or length < 1 or start + length - 1 > duration_weeks:
                errors.append(f"Phase {name!r} has invalid or out-of-range week bounds.")
            if not phase.get("tasks"):
                warnings.append(f"Phase {name!r} has no tasks.")
            if not phase.get("deliverables"):
                warnings.append(f"Phase {name!r} has no deliverables.")
    for risk in (blueprint.get("risk") or {}).get("risks", []):
        if not risk.get("mitigation"):
            warnings.append(f"Risk {risk.get('risk', 'unknown')!r} has no mitigation.")
    return {"valid": not errors, "errors": errors, "warnings": warnings,
            "warning_count": len(warnings)}
