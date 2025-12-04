import pytest
from app.graph.state import GraphState
from app.graph.nodes import (
    llm_generate_node,
    explanation_node,
    toxicity_score_node,
    hallucination_score_node,
    combine_scores_node,
    artifact_node
)

# ---------------------------------------------------------------------
# MOCKING openai responses (monkeypatch)
# ---------------------------------------------------------------------
class MockOpenAIResponse:
    def __init__(self, text):
        self.output_text = text


@pytest.fixture
def mock_llm(monkeypatch):
    def fake_create(*args, **kwargs):
        return MockOpenAIResponse("This is a harmless explanation.")
    monkeypatch.setattr("app.graph.nodes.client.responses.create", fake_create)


@pytest.fixture
def base_state():
    return GraphState(
        user_input="Explain LangGraph",
        llm_output=None,
        explanation=None,
        toxicity_score=None,
        hallucination_score=None,
        overall_score=None,
        artifacts=[],
        start_time=0.0,
    )


# ---------------------------------------------------------------------
# TEST GENERATE NODE
# ---------------------------------------------------------------------
def test_generate_node(mock_llm, base_state):
    new = llm_generate_node(base_state)
    assert new["llm_output"] is not None
    assert isinstance(new["llm_output"], str)


# ---------------------------------------------------------------------
# TEST EXPLAIN NODE
# ---------------------------------------------------------------------
def test_explain_node(mock_llm, base_state):
    base_state["llm_output"] = "LangGraph is a workflow framework."
    new = explanation_node(base_state)
    assert "explanation" in new
    assert isinstance(new["explanation"], str)


# ---------------------------------------------------------------------
# TEST TOXICITY NODE
# ---------------------------------------------------------------------
def test_toxicity_node(base_state):
    base_state["llm_output"] = "You are stupid"
    new = toxicity_score_node(base_state)
    assert "toxicity_score" in new
    assert new["toxicity_score"] >= 0


# ---------------------------------------------------------------------
# TEST HALLUCINATION NODE
# (LLM judge is mocked)
# ---------------------------------------------------------------------
def test_hallucination_node(monkeypatch, base_state):
    def fake_judge(*args, **kwargs):
        return MockOpenAIResponse("0.75")

    monkeypatch.setattr("app.graph.nodes.client.responses.create", fake_judge)

    base_state["llm_output"] = "Wakanda's capital is Birnin Zana."
    new = hallucination_score_node(base_state)
    assert new["hallucination_score"] == 0.75


# ---------------------------------------------------------------------
# TEST COMBINED SCORE NODE
# ---------------------------------------------------------------------
def test_combine_node(base_state):
    base_state["toxicity_score"] = 0.2
    base_state["hallucination_score"] = 0.8
    new = combine_scores_node(base_state)
    assert new["overall_score"] == 0.5


# ---------------------------------------------------------------------
# TEST ARTIFACT NODE
# ---------------------------------------------------------------------
def test_artifact_node(tmp_path, base_state, monkeypatch):
    # patch log file path
    monkeypatch.setattr(
        "app.graph.nodes.LOG_PATH",
        tmp_path / "run.log",
        raising=False
    )

    base_state["user_input"] = "test input"
    base_state["score"] = 1.0

    new = artifact_node(base_state)
    assert "artifacts" in new
    assert len(new["artifacts"]) == 1