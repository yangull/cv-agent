import argparse
from graph import build_graph

def main():
    parser = argparse.ArgumentParser(description="Tailor your CV to a job description using Claude.")
    parser.add_argument("--cv", required=True, help="Path to your CV PDF file")
    parser.add_argument("--jd", default="sample_jd.txt", help="Path to the job description text file")
    args = parser.parse_args()

    graph = build_graph()

    initial_state = {
        "jd_path": args.jd,
        "cv_path": args.cv,
        "job_description": "",
        "cv_text": "",
        "match_score": 0,
        "match_explanation": "",
        "rewritten_bullets": [],
        "output_pdf_path": None
    }

    print("Starting cv-agent pipeline...\n")

    # invoke() runs the graph synchronously from start to END
    final_state = graph.invoke(initial_state)

    print("\nPipeline complete!")
    print(f"  Match score: {final_state['match_score']}/100")
    print(f"  Bullets generated: {len(final_state['rewritten_bullets'])}")
    print(f"  Output PDF: {final_state['output_pdf_path']}")

if __name__ == "__main__":
    main()
