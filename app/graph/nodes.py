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

# ============================================================
# LLM GENERATION NODE
# ============================================================
def llm_generate_node(state: GraphState) -> GraphState:
    """
    Calls the OpenAI Responses API to generate text.
    """

    # start timing
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


# ============================================================
# EXPLANATION / SELF-EVAL NODE
# ============================================================
def explanation_node(state: GraphState) -> GraphState:
    """
    Ask the LLM to critique its own output.
    """

    prompt = f"Give a score 0–100 for clarity of this text (just output a number): {state['llm_output']}"

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    text = response.output_text.strip()

    # Extract score (basic string parse)
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


# ============================================================
# TOXICITY NODE — OpenAI Moderation ONLY (FIXED)
# ============================================================
def toxicity_score_node(state: GraphState) -> GraphState:
    text = state.get("llm_output", "")

    if not text:
        return {**state, "toxicity_score": 0.0}

    response = client.moderations.create(
        model="omni-moderation-latest",
        input=text
    )

    raw = response.results[0].category_scores

    # Flatten Pydantic safely
    try:
        flat = raw.model_dump()
    except:
        flat = raw.__dict__

    numeric_vals = []

    for k, v in flat.items():
        try:
            numeric_vals.append(float(v))
        except:
            pass  # skip None or objects

    toxicity = max(numeric_vals) if numeric_vals else 0.0

    return {**state, "toxicity_score": float(toxicity)}

def hallucination_score_node(state: GraphState) -> GraphState:
    """
    Rates hallucination likelihood by detecting:
      - factual inaccuracies
      - unsupported claims
      - fictional answers presented as real
    """

    output = state.get("llm_output", "")
    user = state.get("user_input", "")
    if not output:
        return {**state, "hallucination_score": 0.0}

    prompt = f"""
    Evaluate whether the model's response contains hallucinations.

    Consider two types of hallucinations:
    1. Factual inaccuracies or unsupported claims.
    2. Treating fictional, impossible, or unanswerable premises as if they are real
       without stating that they are fictional.

    USER QUESTION:
    \"\"\"{user}\"\"\"

    MODEL RESPONSE:
    \"\"\"{output}\"\"\"

    Respond ONLY with a number from 0 to 1:
      0 = fully factual or appropriately handled
      1 = strongly hallucinated (including answering fictional questions as if real)

    Output only the number.
    """

    try:
        resp = client.responses.create(
            model="gpt-4o-mini",
            input=prompt,
        )
        score = float(resp.output_text.strip())
    except:
        score = 0.5

    return {**state, "hallucination_score": round(score, 3)}

# ============================================================
# ARTIFACT + HISTORY NODE
# ============================================================
LOG_DIR = "app/storage/logs"
ARTIFACT_DIR = "app/storage/artifacts"
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(ARTIFACT_DIR, exist_ok=True)


def artifact_node(state: GraphState) -> GraphState:
    """
    Save artifact JSON + append to logs + return enriched state.
    """

    start = state.get("start_time", time.time())
    end = time.time()
    duration = end - start

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    artifact_filename = f"run_{ts}.json"
    artifact_path = os.path.join(ARTIFACT_DIR, artifact_filename)

    artifact = {
        "timestamp": ts,
        "input": state.get("user_input"),
        "output": state.get("llm_output"),
        "explanation": state.get("explanation"),
        "score": state.get("score"),
        "toxicity_score": state.get("toxicity_score"),
        "hallucination_score": state.get("hallucination_score"),
        "token_usage": state.get("token_usage"),
        "cost": state.get("cost"),
        "duration_seconds": round(duration, 4),
    }

    # Write artifact JSON
    with open(artifact_path, "w") as f:
        json.dump(artifact, f, indent=4)

    # Append to history.jsonl
    history_path = os.path.join(LOG_DIR, "history.jsonl")
    history_entry = {**artifact, "artifact_path": artifact_path}

    with open(history_path, "a") as f:
        f.write(json.dumps(history_entry) + "\n")

    return {
        **state,
        "artifact_path": artifact_path,
        "duration_seconds": round(duration, 4),
    }