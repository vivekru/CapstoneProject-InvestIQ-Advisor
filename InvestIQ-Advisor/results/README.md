# Results: final run, 24 November 2026

Real Qwen3-8B (upGrad endpoint), notebook v3.22, `QUICK_MODE = False` (all 60 questions). Every file here is written by the notebook.

| File | Notebook section | What it holds |
|---|---|---|
| `trace_dashboard.html` | 13c | **Trace dashboard**: open in a browser. Status, failure taxonomy, time by step, and a span waterfall per query |
| `retrieval_recall.csv` | 7b | recall@1/3/5/8 and hit@k for dense, BM25, hybrid and hybrid + reranker (52 answerable questions) |
| `eval_summary.csv`, `eval_results.json` | 10 | Single-agent baseline on 60 questions |
| `prompt_strategies.csv`, `prompt_strategies_summary.csv` | 10b | Zero-shot, few-shot, chain-of-thought and decomposition, with how the model breaks |
| `eval_agents.csv`, `eval_agents_results.json` | 12 | LangGraph agents on 60 questions, one failure category per question |
| `eval_metrics_agents.json` | 12 | Track B metrics: accuracy, task completion, tool calls, tokens, latency |
| `failure_taxonomy.csv` | 12 | Failure taxonomy counts |
| `direct_vs_decomposition.csv` | 12 | Direct retrieval vs agent decomposition on 28 multi-hop and calculation questions |
| `ragas_official.csv` | 13 | RAGAS 0.4.4: faithfulness, answer relevancy, context precision, context recall |
| `ragas_own_prompts.csv` | 13 | The same four metrics with our own judge prompts (cross-check) |
| `redteam_log.csv` | 13b | 20 red-team tests (prompt injection, PII, refusals, human-in-the-loop) |
| `traces.jsonl`, `run_log.csv` | 12 | Each agent run (trail, verdicts, citations) and each model call (latency, tokens) |
| `otel_spans.jsonl` | 11 | OpenTelemetry spans for every query, agent node, tool and model call |

Headline: agents 35/60 correct (0.71 with partial = 0.5) vs baseline 25/60 (0.60); recall@8 0.85 with the reranker; red team 20/20.
Note: agent questions Q01–Q48 ran with 3 parallel sub-agents, Q49–Q60 with 1 after an API concurrency limit (HTTP 429); this affects latency only.
Note on traces: OpenTelemetry spans cover 54 of the 60 agent queries and all 20 red-team tests. The six quick-run questions (Q01, Q08, Q12, Q13, Q14, Q19) were answered in an earlier Colab session and restored from its checkpoints, so their spans were not kept; their agent trail, citations and model-call log are in `traces.jsonl` and `run_log.csv`.
