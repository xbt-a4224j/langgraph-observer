# tests/test_artifact_service.py

import os
import json
from app.services.artifact_service import ArtifactService


def test_artifact_service_writes_file(tmp_path, monkeypatch):
    service = ArtifactService()

    # Redirect real paths
    monkeypatch.setattr(service, "artifact_dir", tmp_path)
    monkeypatch.setattr(service, "history_path", tmp_path / "history.jsonl")

    state = {"user_input": "hi", "llm_output": "hello", "start_time": 0}

    updated = service.save_artifact(state)

    assert os.path.exists(updated["artifact_path"])

    with open(updated["artifact_path"]) as f:
        data = json.load(f)

    assert data["input"] == "hi"