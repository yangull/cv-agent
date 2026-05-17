# main.py
from graph import build_graph

def main():
    # Build the compiled LangGraph pipeline
    graph = build_graph()

    # Define the initial state — these two paths are the only inputs we provide
    # Every node after this reads from and writes to this shared state
    initial_state = {
        "jd_path": "sample_jd.txt",       # the job description text file we created
        "cv_path": "Can_Ozer_Arpaci_CV_Parloa.pdf",  # your CV PDF
        "job_description": "",             # will be filled by read_jd node
        "cv_text": "",                     # will be filled by fetch_cv node
        "match_score": 0,                  # will be filled by score_match node
        "match_explanation": "",           # will be filled by score_match node
        "rewritten_bullets": [],           # will be filled by rewrite_bullets node
        "output_pdf_path": None            # will be filled by export_pdf node
    }

    print("🚀 Starting cv-agent pipeline...\n")

    # invoke() runs the graph synchronously from start to END
    # It returns the final state after all nodes have run
    final_state = graph.invoke(initial_state)

    print("\n✅ Pipeline complete!")
    print(f"   Match score: {final_state['match_score']}/100")
    print(f"   Bullets generated: {len(final_state['rewritten_bullets'])}")
    print(f"   Output PDF: {final_state['output_pdf_path']}")

if __name__ == "__main__":
    main()