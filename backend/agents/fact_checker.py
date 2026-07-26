import json
import re

from langchain_core.prompts import ChatPromptTemplate
from core.llm import GroqLLM


class FactChecker:

    def __init__(self):

        self.llm = GroqLLM().get_model()

        self.prompt = ChatPromptTemplate.from_template(
"""
You are an expert fact-checking AI.

Question:
{question}

Answer:
{answer}

Uploaded Document:

{document}

External Evidence (Wikipedia + Tavily):

{web}

Rules:

1. If the answer came from the uploaded document:

- Compare it with external evidence.
- If both agree:
    verified = true

- If the document contradicts trusted external sources:
    verified = false

2. If the answer came from external sources:

- Verify it using the provided external evidence.

3. Confidence must be between 0 and 1.

Return ONLY JSON.

{{
    "verified": true,
    "confidence": 0.95,
    "reason": "..."
}}
"""
        )

        self.chain = self.prompt | self.llm

    def __call__(self, state):

        response = self.chain.invoke(
            {
                "question": state["question"],
                "answer": state["answer"],
                "document": state["context"],
                "web": state.get("web_results", "")
            }
        )

        try:

            match = re.search(
                r"\{.*\}",
                response.content,
                re.DOTALL
            )

            if not match:
                raise ValueError("No JSON returned")

            json_text = match.group()

            data = json.loads(json_text)

        except Exception as e:

            print("Fact Checker Error:", e)
            print(response.content)

            data = {
            "verified": False,
            "confidence": 0.0,
            "reason": "Unable to verify answer"
        }

        return {

            "verified": data["verified"],

            "confidence": data["confidence"],

            "verification": data["reason"]

        }