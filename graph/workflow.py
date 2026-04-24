from langgraph.graph import StateGraph, END

from state import MediCrossState

from nodes.scribe import scribe_node
from nodes.diagnostic import diagnostic_node
from nodes.validator import validator_node
from nodes.critic import critic_node


# -----------------------------
# 🧠 BUILD GRAPH
# -----------------------------

def build_medicross_graph():

    # Create state graph
    graph = StateGraph(MediCrossState)

    # -------------------------
    # 1. Add Nodes (Agents)
    # -------------------------

    graph.add_node("scribe", scribe_node)
    graph.add_node("diagnostic", diagnostic_node)
    graph.add_node("validator", validator_node)
    graph.add_node("critic", critic_node)

    # -------------------------
    # 2. Define Flow Edges
    # -------------------------

    # Entry point
    graph.set_entry_point("scribe")

    # Linear pipeline first
    graph.add_edge("scribe", "diagnostic")
    graph.add_edge("diagnostic", "validator")
    graph.add_edge("validator", "critic")

    # -------------------------
    # 3. Conditional Routing (CRITICAL PART)
    # -------------------------

    def critic_router(state):
        """
        Decides whether to loop or finish system
        """

        decision = state.get("decision", "refine")

        if decision == "approve": #approve or refine
            return "end"
        else:
            return "diagnostic"  # loop back for refinement

    # Add conditional edges from critic
    graph.add_conditional_edges(
        "critic",
        critic_router,
        {
            "end": END,
            "diagnostic": "diagnostic"
        }
    )

    # -------------------------
    # 4. Compile Graph
    # -------------------------

    return graph.compile()