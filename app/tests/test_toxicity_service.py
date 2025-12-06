# app/tests/test_toxicity_service.py

from app.services.toxicity_service import ToxicityService


class DummyModerationResponse:
    """Simple stand-in for the OpenAI moderation response."""
    def __init__(self, scores):
        self.category_scores = scores


class DummyScores:
    """Simulates the Pydantic-ish object returned by OpenAI."""
    def __init__(self, mapping):
        self._mapping = mapping

    def model_dump(self):
        return self._mapping


class DummyAdapter:
    """Minimal mock OpenAIAdapter."""
    def __init__(self, scores):
        self.scores = scores

    def moderate_text(self, text):
        return DummyModerationResponse(
            DummyScores(self.scores)
        )


def test_toxicity_low_score():
    # Very low toxicity mapping
    mock_scores = {"insult": 0.001, "hate": 0.002}

    svc = ToxicityService(adapter=DummyAdapter(mock_scores))

    state = {"llm_output": "Hello world"}
    updated = svc.score_toxicity(state)

    assert "toxicity_score" in updated
    assert updated["toxicity_score"] == 0.002


def test_toxicity_empty_output():
    svc = ToxicityService(adapter=DummyAdapter({"a": 0.5}))

    state = {"llm_output": ""}
    updated = svc.score_toxicity(state)

    assert updated["toxicity_score"] == 0.0