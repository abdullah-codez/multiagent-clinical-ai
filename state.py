from typing import TypedDict, List, Optional, Dict, Any


class MediCrossState(TypedDict, total=False):
    """
    Global shared state for MediCross Multi-Agent Clinical Decision System
    """

    #  Raw Input
    patient_input: str

    #  Scribe Output (structured medical data)
    structured_data: Dict[str, Any]
    symptoms: List[str]
    history: Dict[str, Any]
    medications: List[str]

    #  Diagnostic Agent Output
    differential_diagnosis: List[Dict[str, Any]]
    # Example:
    # [{"disease": "Pneumonia", "reasoning": "...", "rank": 1}, ...]

    #  Evidence Validator Output
    evidence_report: Dict[str, Any]
    # Example:
    # {
    #   "Pneumonia": {"evidence_score": 0.85, "sources": ["WHO", "PubMed"]},
    # }

    safety_report: Dict[str, Any]
    # Drug contraindications, risk flags, warnings

    validation_score: float

    # Critic Output
    quality_score: float
    decision: str  # "approve" or "refine"

    #  Loop Control
    iteration: int
    max_iterations: int

    #  Final Output
    final_report: Dict[str, Any]