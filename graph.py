# graph.py
from langgraph.graph import StateGraph, END
from state import AgentState
from nodes.read_jd import read_jd
from nodes.fetch_cv import fetch_cv
from nodes.score_match import score_match
from nodes.rewrite_bullets import rewrite_bullets
from nodes.export_pdf import export_pdf

def build_graph():
    # Create a StateGraph — this is the container for all nodes and edges
    # AgentState is passed in so LangGraph knows the shape of the shared state
    graph = StateGraph(AgentState)

    # Register each node with a name and the function that runs it
    graph.add_node("read_jd", read_jd)
    graph.add_node("fetch_cv", fetch_cv)
    graph.add_node("score_match", score_match)
    graph.add_node("rewrite_bullets", rewrite_bullets)
    graph.add_node("export_pdf", export_pdf)

    # Define the entry point — this is the first node that runs
    graph.set_entry_point("read_jd")

    # Add edges — each edge says "when this node finishes, run that node next"
    graph.add_edge("read_jd", "fetch_cv")
    graph.add_edge("fetch_cv", "score_match")
    graph.add_edge("score_match", "rewrite_bullets")
    graph.add_edge("rewrite_bullets", "export_pdf")

    # END is a special LangGraph constant meaning "the graph is done after this node"
    graph.add_edge("export_pdf", END)

    # Compile turns the graph definition into a runnable object
    return graph.compile()