import os
from dotenv import load_dotenv
from typing import Dict, Any
from utils.robust_json import extract_json_object


# Gemini SDK (Google GenAI)
import google.generativeai as genai

# Load environment variables (.env file)
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Choose model (you can upgrade later)
model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")


def scribe_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Scribe Agent:
    Converts raw patient input into structured medical data.
    """

    patient_text = state.get("patient_input", "")

    # 🧠 Prompt for structured clinical extraction
    prompt = f"""
You are a medical Scribe Agent in a Clinical Decision Support System.

Your job is to convert raw patient text into structured clinical data.

Return ONLY valid JSON (no explanations, no markdown).

Schema:
{{
  "symptoms": [],
  "history": {{
    "past_illness": [],
    "family_history": [],
    "lifestyle": ""
  }},
  "medications": [],
  "key_findings": [],
  "possible_red_flags": []
}}

Rules:
- Extract ONLY medically relevant information
- Do NOT hallucinate
- If missing info, return empty list or null
- Keep medical terminology normalized

Patient Input:
\"\"\"{patient_text}\"\"\"
"""

    # 🧠 Call Gemini
    response = model.generate_content(prompt)

    try:
        structured_output = response.text
        parsed_data = extract_json_object(structured_output)

    except Exception as e:
        # Fallback safety structure
        parsed_data = {
            "symptoms": [],
            "history": {
                "past_illness": [],
                "family_history": [],
                "lifestyle": ""
            },
            "medications": [],
            "key_findings": [],
            "possible_red_flags": [],
            "error": str(e)
        }

    # 🧠 Update LangGraph state
    return {
        "structured_data": parsed_data,
        "symptoms": parsed_data.get("symptoms", []),
        "history": parsed_data.get("history", {}),
        "medications": parsed_data.get("medications", [])
    }