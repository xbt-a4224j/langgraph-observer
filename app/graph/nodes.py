# app/graph/nodes.py

import json
import os
import time
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI

from .state import GraphState

load_dotenv()
client = OpenAI()

# -------------------------
# LLM GENERATION NODE
# -------------------------
def llm_generate_node(state: GraphState) -> GraphState:
    """
    Calls the OpenAI Responses API to generate text.
    """

    # Start timing
    state["start_time"] = time.time()

    user_msg = state["user_input"]

    response = client.responses.create(
        model="gpt-4o-mini",
        input=user_msg
    )

    llm_text = response.output_text

    # Token usage (new Responses API)
    usage = response.usage
    input_tokens = usage.input_tokens
    output_tokens = usage.output_tokens
    total_tokens = usage.total_tokens

    # Cost estimation for gpt-4o-mini
    input_cost = input_tokens / 1000 * 0.00015
    output_cost = output_tokens / 1000 * 0.00060
    total_cost = input_cost + output_cost

    return {
        **state,
        "llm_output": llm_text,
        "token_usage": {
            "input": input_tokens,
            "output": output_tokens,
            "total": total_tokens,
        },
        "cost": round(total_cost, 6),
    }


# -------------------------
# EVALUATION NODE
# -------------------------
def explanation_node(state: GraphState) -> GraphState:
    """
    Ask the LLM to critique its own output.
    """

    prompt = f"""
    Evaluate the following model output on clarity, correctness,
    and helpfulness. Respond with a score (0-100) and a brief explanation.

    Output:
    {state['llm_output']}
    """

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    text = response.output_text.strip()

    # Extract score (very basic)
    score = None
    for token in text.split():
        if token.strip().isdigit():
            score = int(token)
            break

    return {
        **state,
        "explanation": text,
        "score": score,
    }


# -------------------------
# ARTIFACT + LOGGING NODE
# -------------------------

LOG_DIR = "app/storage/logs"
ARTIFACT_DIR = "app/storage/artifacts"
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(ARTIFACT_DIR, exist_ok=True)

def artifact_node(state: GraphState) -> GraphState:
    """
    Save artifacts, compute timing, write history, return enriched state.
    """

    # -------------------------
    # 1. Timing
    # -------------------------
    start = state.get("start_time", time.time())
    end = time.time()
    duration = end - start

    # -------------------------
    # 2. Save artifact
    # -------------------------
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    artifact_filename = f"run_{ts}.json"
    artifact_path = os.path.join(ARTIFACT_DIR, artifact_filename)

    artifact = {
        "timestamp": ts,
        "input": state.get("user_input"),
        "output": state.get("llm_output"),
        "explanation": state.get("explanation"),
        "score": state.get("score"),
        "token_usage": state.get("token_usage"),
        "cost": state.get("cost"),
        "duration_seconds": round(duration, 4),
    }

    with open(artifact_path, "w") as f:
        json.dump(artifact, f, indent=4)

    # -------------------------
    # 3. History Logging (JSONL)
    # -------------------------
    history_path = os.path.join(LOG_DIR, "history.jsonl")

    history_entry = {
        **artifact,
        "artifact_path": artifact_path,
    }

    with open(history_path, "a") as f:
        f.write(json.dumps(history_entry) + "\n")

    # -------------------------
    # 4. Update state + return
    # -------------------------
    return {
        **state,
        "artifact_path": artifact_path,
        "duration_seconds": round(duration, 4),
    }