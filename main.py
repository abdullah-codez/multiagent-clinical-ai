
from graph.workflow import build_medicross_graph


def run_medicross():
    """
    Entry point for MediCross system execution.
    """

    # -----------------------------
    # Build LangGraph system
    # -----------------------------
    app = build_medicross_graph()

    # -----------------------------
    #  Example Patient Input
    # -----------------------------
    initial_state = {
    "patient_input": """
    Patient is a 62-year-old male.

    Chief complaints:
    - Severe chest pain radiating to left arm
    - Shortness of breath
    - Sweating and nausea
    - Pain started suddenly while resting

    Medical history:
    - Hypertension (10 years)
    - Type 2 diabetes

    Medications:
    - Metformin
    - Amlodipine

    Lifestyle:
    - Smoker for 30 years
    """,

    "iteration": 0,
    "max_iterations": 3
    }

    # -----------------------------
    #  Run the Graph
    # -----------------------------
    final_state = app.invoke(initial_state)

    # -----------------------------
    #  Output Results
    # -----------------------------

    print("\n==============================")
    print(" MEDICROSS FINAL REPORT")
    print("==============================\n")

    print(" Final Diagnosis (Differential):")

    for d in final_state.get("differential_diagnosis", []):
        print(f"- {d.get('disease')} (Rank {d.get('rank')})")
        print(f"  Reasoning: {d.get('reasoning')}\n")

    print(" Evidence Report:")

    print(final_state.get("evidence_report", {}))

    print("\n Safety Report:")

    print(final_state.get("safety_report", {}))

    print("\n Quality Score:", final_state.get("quality_score"))
    
    print(" Iterations:", final_state.get("iteration"))


# -----------------------------
#  RUN SCRIPT
# -----------------------------
if __name__ == "__main__":
    run_medicross()