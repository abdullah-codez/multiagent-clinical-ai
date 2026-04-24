from typing import Dict, Any


def critic_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Critic + Router Agent:
    Evaluates system output quality and controls loop flow.
    """

    validation_score = state.get("validation_score", 0.0)
    iteration = state.get("iteration", 0)
    max_iterations = state.get("max_iterations", 3)

    # 🧠 Extract supporting signals
    diagnosis = state.get("differential_diagnosis", [])
    evidence_report = state.get("evidence_report", {})
    safety_report = state.get("safety_report", {})

    # -----------------------------
    # 🧠 QUALITY EVALUATION LOGIC
    # -----------------------------

    # Base score starts from validator output
    quality_score = validation_score

    # Penalize if no diagnosis exists
    if not diagnosis:
        quality_score -= 0.4

    # Penalize safety issues
    if safety_report.get("red_flags"):
        quality_score -= 0.3

    # Penalize weak evidence coverage
    if len(evidence_report.keys()) < 2:
        quality_score -= 0.2

    # Clamp score between 0 and 1
    quality_score = max(0.0, min(1.0, quality_score))

    # -----------------------------
    # 🔁 LOOP CONTROL LOGIC
    # -----------------------------

    if iteration >= max_iterations:
        decision = "approve"  # force stop to prevent infinite loop
    else:
        if quality_score >= 0.2:
            decision = "approve"
        else:
            decision = "refine"

    # -----------------------------
    # 🧠 RETURN UPDATED STATE
    # -----------------------------

    return {
        "quality_score": quality_score,
        "decision": decision,
        "iteration": iteration + 1
    }



