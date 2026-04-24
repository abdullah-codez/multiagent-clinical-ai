import json
import re


def extract_json_object(text: str):
    """
    Ultra-robust JSON extractor for LLM outputs.
    Handles:
    - markdown ```json blocks
    - extra explanation text
    - partial JSON
    - noisy responses
    """

    if not text:
        return {}

    # -----------------------------------
    # 1. Remove markdown code blocks
    # -----------------------------------
    text = text.replace("```json", "").replace("```", "").strip()

    # -----------------------------------
    # 2. Try direct parsing first
    # -----------------------------------
    try:
        return json.loads(text)
    except:
        pass

    # -----------------------------------
    # 3. Extract FIRST valid JSON object
    # -----------------------------------
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        candidate = match.group()

        try:
            return json.loads(candidate)
        except:
            pass

    # -----------------------------------
    # 4. Last resort → return safe empty
    # -----------------------------------
    return {}