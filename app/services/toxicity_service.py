# app/services/toxicity_service.py

from typing import Dict, Any, Optional

from app.adapters.openai_adapter import OpenAIAdapter
#     "id": "modr-abc123",
#     "model": "omni-moderation-latest",
#     "results": [
#         {
#             "flagged": False,
#             "categories": {
#                 "harassment": False,
#                 "harassment/threatening": False,
#                 "hate": False,
#                 "hate/threatening": False,
#                 "self-harm": False,
#                 "sexual": False,
#                 "sexual/minors": False,
#                 "violence": False,
#                 "violence/graphic": False
#             },
#             "category_scores": {
#                 "harassment": 0.00002,
#                 "harassment/threatening": 0.00000,
#                 "hate": 0.00001,
#                 "hate/threatening": 0.00000,
#                 "self-harm": 0.00000,
#                 "sexual": 0.00003,
#                 "sexual/minors": 0.00000,
#                 "violence": 0.00005,
#                 "violence/graphic": 0.00000
#             }
#         }
#     ]
# }
#

class ToxicityService:
    """
    Wraps the OpenAI moderation API and returns a numeric toxicity score
    (0.0–1.0), consistent with the above moderation struct form
    """

    def __init__(self, adapter: Optional[OpenAIAdapter] = None):
        self.adapter = adapter or OpenAIAdapter()

    def score_toxicity(self, state: Dict[str, Any]) -> Dict[str, Any]:

        text = state.get("llm_output", "")
        if not text:
            state["toxicity_score"] = 0.0
            return state

        response = self.adapter.moderate_text(text)
        raw = response.category_scores

        # Flatten possible Pydantic structure
        try:
            flat = raw.model_dump()
        except Exception:
            flat = raw.__dict__

        numeric_vals = []

        for k, v in flat.items():
            try:
                numeric_vals.append(float(v))
            except Exception:
                pass  # skip None or non-numerics

        toxicity = max(numeric_vals) if numeric_vals else 0.0

        state["toxicity_score"] = float(toxicity)
        return state