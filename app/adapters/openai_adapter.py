# app/adapters/openai_adapter.py

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class OpenAIAdapter:
    """
    Thin wrapper around the OpenAI client.
    For now, only text generation is exposed.
    """

    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = OpenAI()
        self.model = model

    def generate_text(self, prompt: str):
        """
        Equivalent to the client.responses.create(...) call in llm_generate_node.
        Returns text and the raw usage object so cost calculation stays identical.
        """
        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )

        return {
            "text": response.output_text,
            "usage": response.usage,  # same shape as in your current nodes.py
        }

    def moderate_text(self, text: str):
        """
        Calls the OpenAI moderation endpoint.
        Returns an object with .category_scores, matching the original API.
        """
        resp = self.client.moderations.create(
            model="omni-moderation-latest",
            input=text
        )
        return resp.results[0]