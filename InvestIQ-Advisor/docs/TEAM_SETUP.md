# InvestIQ Advisor: team setup (Colab)

Notebook: **`InvestIQ_Advisor_v3_22.ipynb`** in the shared **SPARTVIT-AI** Google Drive folder.
Everything runs in your own Colab session. Nothing depends on anyone's laptop.

## 1. What the shared SPARTVIT-AI folder must contain

```
SPARTVIT-AI/
├── InvestIQ_Advisor_v3_22.ipynb        ← the notebook to run
├── TEAM_SETUP.md                       ← this file
├── data/
│   ├── AAPL_10K_FY2025.pdf
│   ├── AAPL_10K_FY2026.pdf
│   ├── MSFT_10K_FY2025.pdf
│   └── MSFT_10K_FY2026.pdf             (other file names, e.g. JJ_IFRS(SAMPLE).pdf, are skipped)
├── chat-model/
│   └── vm04-ca.crt                     ← certificate for the Qwen3-8B chat endpoint
├── VM02_Embeddings_Access/
│   ├── vm02-ca.crt                     ← certificate for the embedding endpoint
│   └── shared-embedding-key.txt        ← team embedding key (team folder only; never share outside the team)
└── outputs/                            ← created automatically
    ├── cache/                          ← shared embedding index (built once, then reused by everyone)
    └── <your name>/                    ← your own feedback and evaluation results
```

Older notebooks (v2, v3–v3.21) can be moved to an `archive/` subfolder so nobody opens the wrong one.

## 2. One-time setup for each teammate (about 5 minutes)

1. **Add the folder to your Drive.** In Google Drive, open **Shared with me**, right-click **SPARTVIT-AI**, then **Organize → Add shortcut → My Drive**. The notebook finds the folder in My Drive, in a subfolder, or in a shared drive.
2. **Open the notebook** in Colab: double-click `InvestIQ_Advisor_v3_22.ipynb`, then choose **Open with → Google Colaboratory**.
3. **Add your Colab secrets.** Click the 🔑 icon in the left sidebar, then **+ Add new secret**:

   | Name | Value | Needed? |
   |---|---|---|
   | `qwen` | The Qwen3-8B chat API key (ask in the private team chat) | **Yes** |
   | `RUN_BY` | Your first name, letters only (e.g. `rohit`) | **Yes for everyone except Vivek** (without it, results go to Vivek's folder) |
   | `EMBED_API_KEY` | The embedding key | Optional (read from the team folder if missing) |

   Switch **Notebook access** on for each secret. Secrets belong to your Google account, not to the notebook, so keys are never stored in the shared file.

## 3. Run it

1. **Runtime → Run all.** If Colab asks for Drive access or secret access, click **Allow / Grant access**.
2. Section 2 prints a **pre-flight checklist**. Every line should show ✅ (➖ is fine for optional items). A ❌ means a file is missing from the shared folder.
3. If the LangGraph install in section 11 asks you to restart, choose **Runtime → Restart session**, then **Run all** again.
4. With `QUICK_MODE = True` (default, section 2), the evaluations use 6 demo questions and finish in about 10 minutes. Set it to `False` for all **60** questions (about 2 hours; keep the Colab tab open).
5. **If Colab disconnects** (laptop sleep, network): open the notebook again and **Run all**. With `RESUME = True` (section 2) every finished question was saved to `outputs/<your name>/checkpoints_v3_22.jsonl`, so it continues where it stopped. Delete that file to start from scratch. To avoid sleep on a Mac, plug in, keep the lid open and run `caffeinate -dims` in Terminal.
6. The first run downloads the reranker model (`BAAI/bge-reranker-base`, about 1 GB) once per session.

**What a run writes to `outputs/<your name>/`:** `retrieval_recall.csv` (recall@k), `eval_summary.csv` (baseline), `prompt_strategies*.csv`, `eval_agents.csv`, `eval_metrics_agents.json`, `failure_taxonomy.csv`, `direct_vs_decomposition.csv`, `ragas_official.csv`, `redteam_log.csv`, `traces.jsonl`, `run_log.csv`, `otel_spans.jsonl` (OpenTelemetry), **`trace_dashboard.html`** (open in a browser), `feedback.jsonl`.

## 4. Use the chatbot

- **Web app (section 15):** opens a chat page in a new browser tab (allow pop-ups for colab.research.google.com). Add `/docs` to the tab's address for the FastAPI page.
- **Notebook chat (section 14):** a chat box under the cell.
- Ask a question, then **Approve** or **Reject** the answer (a reason is required to reject). After a Reject, the agents revise the answer once using your reason and show it for review again. Decisions go to `outputs/<your name>/feedback.jsonl`.
- **✎ Edit** on a question puts it back in the box to change and ask again.
- **Follow-up questions** work in the web app (e.g. ask about Microsoft, then "And Apple?"). **New research** starts a fresh conversation.

Good test questions: see `ground_truth_questions_v4.csv` (60 questions), e.g. "Compare how full-time headcount changed at Microsoft and at Apple from fiscal year 2025 to fiscal year 2026."

## 5. Things to know

- Each teammate runs their **own** Colab session. The web app works only while your session is running; if Colab disconnects, run all again.
- One question at a time: every answer calls the upGrad API.
- Never paste keys into notebook cells, chat messages or files outside the team folder.

## 6. Troubleshooting

| Message | Fix |
|---|---|
| "Could not find the shared 'SPARTVIT-AI' folder" | Do step 2.1 (add the shortcut), then re-run section 2 |
| ❌ in the pre-flight checklist | The named file is missing from the shared folder; ask Vivek |
| Asked for "Qwen chat API key" | Add the `qwen` secret and switch on notebook access (step 2.3) |
| HTTP 401/403 | Key wrong or not for this endpoint; check the secret value |
| Chat tab does not open | Allow pop-ups, or use the copy shown under the section 15 cell |
| LangChain/LangGraph import error | Re-run the first cell of section 11 and restart the session once |
| HTTP 429 in the web app | Rate limit (10 questions per minute); wait a moment |
| "Reranker ... could not be loaded" | Search still works without it; re-run section 7 once the download succeeds |
