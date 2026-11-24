"""Start the InvestIQ Advisor web app and API (FastAPI + uvicorn)."""
import os
import uvicorn
import investiq_core   # loads the reports, builds or loads the index, compiles the LangGraph agents

if __name__ == "__main__":
    uvicorn.run(investiq_core.api, host="0.0.0.0", port=int(os.environ.get("PORT", "8000")), log_level="info")
