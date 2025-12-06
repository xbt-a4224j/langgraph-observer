# app/tests/test_llm_service.py

import time
from unittest.mock import MagicMock

from app.services.llm_service import LLMService


def test_llm_service_basic_generation():
    # Mock adapter response
    mock_adapter = MagicMock()
    mock_adapter.generate_text.return_value = {
        "text": "Hello world",
        "usage": MagicMock(
            input_tokens=10,
            output_tokens=20,
            total_tokens=30,
        ),
    }

    service = LLMService(adapter=mock_adapter)

    state = {"user_input": "hi"}

    result = service.generate(state)

    # Output should be set
    assert result["llm_output"] == "Hello world"

    # Token usage dict should be correct
    assert result["token_usage"] == {"input": 10, "output": 20, "total": 30}

    # Cost calculation (simple sanity check)
    expected_cost = round((10 / 1000 * 0.00015) + (20 / 1000 * 0.00060), 6)
    assert result["cost"] == expected_cost

    # Should add a start_time
    assert "start_time" in result
    assert isinstance(result["start_time"], float)