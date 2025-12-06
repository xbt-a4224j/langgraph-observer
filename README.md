# LangGraph Observer


<img width="1341" height="843" alt="Screenshot 2025-12-06 at 6 07 51 PM" src="https://github.com/user-attachments/assets/4fb9375c-69b4-45a4-8949-15d7c6e27b7c" />
----
<img width="971" height="416" alt="image" src="https://github.com/user-attachments/assets/ffe2bdb7-a535-42e1-a8a6-f7542167ca50" />


A compact environment for running and inspecting a LangGraph workflow. It includes:

- A FastAPI backend that executes the graph  
- A Streamlit dashboard for interactive prompting  
- Modular services for generation, “emoji mode,” toxicity, hallucination scoring, and artifact logging  
- A simple dict-based state passed between workflow nodes  

---

## Pipeline Overview

The workflow runs:

1. Generate LLM output  
2. Optionally apply a “emoji-fy” transformation  
3. Compute emoji-ness score  
4. Compute toxicity score  
5. Compute hallucination score  
6. Save an artifact and append run history  

Artifacts record output, scores, token usage, duration, and cost.

---

## Dashboard

Features:

- Prompt input + sample prompts  
- **Run Workflow** button  
- **Make More Emoji** button for iterative & interactive transformations  
- Sidebar with metrics (toxicity, hallucination, emoji score, duration)  
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
