import os
from dotenv import load_dotenv
from typing import Dict, Any, List

import google.generativeai as genai
from utils.robust_json import extract_json_object

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")


def validator_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evidence & Safety Validator:
    Validates differential diagnosis using medical reasoning + safety constraints.
    """

    diagnosis = state.get("differential_diagnosis", [])
    structured_data = state.get("structured_data", {})

    symptoms = structured_data.get("symptoms", [])
    medications = structured_data.get("medications", [])

    prompt = f"""
You are a Clinical Evidence & Safety Validator AI.

Your job:
1. Evaluate each diagnosis for medical plausibility
2. Assign evidence strength score (0 to 1)
3. Detect safety risks (especially drug-related)
4. Flag contradictions or weak reasoning

Return ONLY valid JSON.

Schema:
{{
  "evidence_report": {{
    "DiseaseName": {{
      "evidence_score": 0.0,
      "supporting_factors": [],
      "weak_points": [],
      "confidence_level": "low|medium|high"
    }}
  }},
  "safety_report": {{
    "warnings": [],
    "drug_interactions": [],
    "red_flags": []
  }},
  "overall_validation_score": 0.0
}}

Rules:
- Be strict, not optimistic
- Penalize weak reasoning heavily
- If data is insufficient → lower score
- Prioritize patient safety over completeness

Input Data:

Diagnosis List:
{diagnosis}

Symptoms:
{symptoms}

Medications:
{medications}
"""

    response = model.generate_content(prompt)

    #  ROBUST PARSING
    data = extract_json_object(response.text)

    evidence_report = data.get("evidence_report", {})
    safety_report = data.get("safety_report", {})
    validation_score = data.get("overall_validation_score", 0.0)

    # fallback safety
    if not evidence_report:
        safety_report.setdefault("warnings", []).append("Weak or missing evidence")

    return {
        "evidence_report": evidence_report,
        "safety_report": safety_report,
        "validation_score": validation_score
    }