# app/services/llm_service.py

import time
from typing import Optional, Dict, Any

from app.domain.state import GraphState
from app.adapters.openai_adapter import OpenAIAdapter


class LLMService:
    """
    Service responsible for LLM interactions plus associated cost/usage logic.
    Runs inside LangGraph, so it must accept and return dicts.
    """

    def __init__(self, adapter: Optional[OpenAIAdapter] = None):
        self.adapter = adapter or OpenAIAdapter()

    def generate(self, state: dict) -> dict:
        """
        LangGraph node: modifies and returns a dict-based state.
        """
        start_time = time.time()
        user_msg = state.get("user_input")

        result = self.adapter.generate_text(user_msg)

        llm_text = result["text"]
        usage = result["usage"]

        # Token usage
        input_tokens = usage.input_tokens
        output_tokens = usage.output_tokens
        total_tokens = usage.total_tokens

        input_cost = input_tokens / 1000 * 0.00015
        output_cost = output_tokens / 1000 * 0.00060
        total_cost = round(input_cost + output_cost, 6)

        # Update the existing dict and return it
        state.update({
            "start_time": start_time,
            "llm_output": llm_text,
            "token_usage": {
                "input": input_tokens,
                "output": output_tokens,
                "total": total_tokens,
            },
            "cost": total_cost,
        })

        return state