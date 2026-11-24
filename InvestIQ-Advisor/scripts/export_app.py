"""Build app/investiq_core.py from the notebook, so the notebook stays the single source of truth.

Keeps the sections the service needs (config, clients, retries, reports, index, search + reranker, answer checks,
LangGraph agents, FastAPI) and drops evaluation, demos, RAGAS, red-team runs and the Colab-only cells.
Usage:  python scripts/export_app.py notebooks/InvestIQ_Advisor_v3_22.ipynb app/investiq_core.py
"""
import json, re, sys
from pathlib import Path

KEEP = ("2.", "3.", "4.", "5.", "6.", "7.", "8.", "11.", "15.")   # section numbers to keep ("7b." etc. are skipped)
HEADER = '''# GENERATED from the InvestIQ Advisor notebook by scripts/export_app.py. Do not edit by hand.
# Configuration comes from environment variables: INVESTIQ_PROJECT_DIR, LLM_API_KEY, EMBED_API_KEY, RUN_BY.
try:
    from IPython.display import display, HTML, Image
except ImportError:            # running as a plain service: show nothing
    def display(*a, **k): pass
    HTML = Image = lambda *a, **k: None
'''

def main(src, dst):
    nb = json.loads(Path(src).read_text(encoding="utf-8"))
    section, out = None, [HEADER]
    for cell in nb["cells"]:
        text = "".join(cell["source"])
        if cell["cell_type"] == "markdown":
            m = re.match(r"\s*##\s+(\d+b?\.)", text)
            if m: section = m.group(1)
            continue
        if "def save_feedback(" in text:   # section 9: keep the feedback log writer, drop the notebook review widget
            text = text.split("def review(")[0]
        elif section not in KEEP:
            continue
        if "_api_server = uvicorn.Server" in text or "def show_agents(" in text:
            continue                     # notebook-only: background server start, notebook display helpers
        text = text.split("# check every endpoint inside the notebook")[0]   # drop the notebook self-test
        lines = [l for l in text.splitlines() if not l.lstrip().startswith(("%", "!"))]
        out.append(f"# ---- notebook section {section} ----\n" + "\n".join(lines))
    Path(dst).write_text("\n\n".join(out) + "\n", encoding="utf-8")
    print(f"wrote {dst} ({sum(len(x.splitlines()) for x in out)} lines)")

if __name__ == "__main__":
    main(*sys.argv[1:3])
