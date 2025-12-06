# app/tests/test_hallucination_service.py

from unittest.mock import MagicMock

from app.services.hallucination_service import HallucinationService


def test_hallucination_service_parses_numeric_score():
    mock_adapter = MagicMock()
    mock_adapter.generate_text.return_value = {"text": "0.42"}

    service = HallucinationService(adapter=mock_adapter)

    state = {
        "user_input": "Who was president in 1400?",
        "llm_output": "It was John Doe."
    }

    result = service.score_hallucination(state)

    assert result["hallucination_score"] == 0.42


def test_hallucination_service_handles_missing_output():
    service = HallucinationService(adapter=MagicMock())

    state = {"user_input": "anything", "llm_output": ""}

    result = service.score_hallucination(state)
    assert result["hallucination_score"] == 0.0