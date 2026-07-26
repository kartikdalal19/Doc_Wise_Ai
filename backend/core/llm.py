from langchain_groq import ChatGroq
from core.config import settings



class GroqLLM:

    def __init__(self):

        if not settings.GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY not found. Set it in the environment variables."
            )

        self.llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model=settings.GROQ_MODEL,
            temperature=settings.TEMPERATURE,
        )

    def get_model(self):

        return self.llm