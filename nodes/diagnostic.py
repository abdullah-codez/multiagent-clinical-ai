import os
from dotenv import load_dotenv
from typing import Dict, Any, List

import google.generativeai as genai
from utils.robust_json import extract_json_object

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")


def diagnostic_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Diagnostic Agent:
    Generates ranked differential diagnosis based on structured patient data.
    """

    structured_data = state.get("structured_data", {})
    symptoms = structured_data.get("symptoms", [])
    history = structured_data.get("history", {})
    medications = structured_data.get("medications", [])

    prompt = f"""
You are a senior clinical diagnostic reasoning AI.

Your task is to generate a ranked Differential Diagnosis (DDx)
based ONLY on the provided structured patient data.

Return ONLY valid JSON.

Schema:
{{
  "differential_diagnosis": [
    {{
      "disease": "",
      "rank": 1,
      "reasoning": "",
      "supporting_symptoms": [],
      "contra_indicators": []
    }}
  ]
}}

Rules:
- Provide 3 to 6 possible diagnoses
- Rank them by probability (1 = most likely)
- Use medical reasoning, not guessing
- Do NOT give final diagnosis
- Be conservative and realistic
- If uncertainty is high, reflect it in reasoning

Patient Data:

Symptoms: {symptoms}
History: {history}
Medications: {medications}
"""

    response = model.generate_content(prompt)

    # ✅ ROBUST PARSING
    data = extract_json_object(response.text)

    diagnosis_list = data.get("differential_diagnosis", [])

    # fallback if model returns garbage
    if not diagnosis_list:
        diagnosis_list = [
            {
                "disease": "Unknown",
                "rank": 1,
                "reasoning": "Model returned unstructured output",
                "supporting_symptoms": symptoms,
                "contra_indicators": []
            }
        ]

    return {
        "differential_diagnosis": diagnosis_list
    }