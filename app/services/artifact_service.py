# app/services/artifact_service.py

import os
import json
import time
from datetime import datetime
from typing import Dict, Any


class ArtifactService:
    """
    Saves per-run artifacts and appends run history.
    Fully replaces the old artifact_node.
    """

    def __init__(self):
        base_dir = "app/storage"
        self.artifact_dir = os.path.join(base_dir, "artifacts")
        self.log_dir = os.path.join(base_dir, "logs")

        os.makedirs(self.artifact_dir, exist_ok=True)
        os.makedirs(self.log_dir, exist_ok=True)

        self.history_path = os.path.join(self.log_dir, "history.jsonl")

    def save_artifact(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Equivalent to the old artifact_node:
        - computes duration
        - writes JSON artifact
        - appends JSONL log
        - returns updated state
        """

        start = state.get("start_time", time.time())
        end = time.time()
        duration = end - start

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"run_{timestamp}.json"
        artifact_path = os.path.join(self.artifact_dir, filename)

        artifact = {
            "timestamp": timestamp,
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

        # Write JSON artifact file
        with open(artifact_path, "w") as f:
            json.dump(artifact, f, indent=4)

        # Append to history.jsonl
        history_entry = {**artifact, "artifact_path": artifact_path}

        with open(self.history_path, "a") as f:
            f.write(json.dumps(history_entry) + "\n")

        # Update state for downstream nodes
        state["artifact_path"] = artifact_path
        state["duration_seconds"] = round(duration, 4)

        return state