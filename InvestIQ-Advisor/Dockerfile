# InvestIQ Advisor: FastAPI web app + LangGraph agents, as one container.
# Build:  docker build -t investiq-advisor .
# Run:    docker compose up            (see docker-compose.yml and .env.example)
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 \
    INVESTIQ_PROJECT_DIR=/project PORT=8000 HF_HOME=/opt/hf

WORKDIR /app
# CPU-only PyTorch first (the reranker needs it; the CUDA build is ~10x larger)
RUN pip install --index-url https://download.pytorch.org/whl/cpu torch
COPY requirements.txt .
RUN pip install -r requirements.txt
# bake the reranker model into the image so the container starts without downloading it
RUN python -c "from sentence_transformers import CrossEncoder; CrossEncoder('BAAI/bge-reranker-base')"

COPY app/ /app/
# reports, certificates and outputs are mounted at /project at run time (never baked into the image);
# keys come from environment variables (LLM_API_KEY, EMBED_API_KEY), never from files in the image
RUN useradd --create-home investiq && mkdir -p /project && chown -R investiq /project /opt/hf
USER investiq
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=120s --retries=3 \
  CMD python -c "import urllib.request,os; urllib.request.urlopen(f'http://localhost:{os.environ.get(\"PORT\",\"8000\")}/health', timeout=4)"
CMD ["python", "serve.py"]
