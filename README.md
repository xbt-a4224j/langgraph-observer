# LangGraph Observer

A compact environment for running and inspecting a LangGraph workflow. It includes:

- A FastAPI backend that executes the graph  
- A Streamlit dashboard for interactive prompting  
- Modular services for generation, “silly mode,” toxicity, hallucination scoring, and artifact logging  
- A simple dict-based state passed between workflow nodes  

---

## Pipeline Overview

The workflow runs:

1. Generate LLM output  
2. Optionally apply a “silly” transformation  
3. Compute silly score  
4. Compute toxicity score  
5. Compute hallucination score  
6. Save an artifact and append run history  

Artifacts record output, scores, token usage, duration, and cost.

---

## Dashboard

Features:

- Prompt input + sample prompts  
- **Run Workflow** button  
- **Make More Silly** button for iterative transformations  
- Sidebar with metrics (toxicity, hallucination, silly score, duration)  
- Recent runs table  
- Full-state JSON output  

Launch:

```bash
uv run streamlit run app/dashboard/ui.py
```

---

## Backend

FastAPI provides two endpoints:

- `POST /run-graph` — executes the full workflow  
- `GET /health` — basic status check  

Start the API server:

```bash
uvicorn app.api.server:app --reload
```

---

## Project Structure

```
app/
  api/
  adapters/
  dashboard/
  domain/
  services/