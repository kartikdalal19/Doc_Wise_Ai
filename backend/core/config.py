import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    # Embeddings
    # HF_EMBEDDING_MODEL = (
    #     "sentence-transformers/all-MiniLM-L6-v2"
    # )

    HF_EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

    
    # LLM
    # GROQ_MODEL = "llama-3.3-70b-versatile"
    GROQ_MODEL = "openai/gpt-oss-120b"
    TEMPERATURE = 0

    # Chunking
    CHUNK_SIZE = 300
    CHUNK_OVERLAP = 100

    # Retrieval
    TOP_K = 3
    RETRIEVAL_THRESHOLD = 0.65

    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

    # Feature flags
    ENABLE_FACT_CHECK = True
    ENABLE_WEB_SEARCH = True

    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    
    HF_TOKEN = os.getenv(
        "HF_TOKEN"
    )


settings = Settings()

# Validate environment variables
if not settings.GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

if settings.ENABLE_WEB_SEARCH and not settings.TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY environment variable is not set.")

if not settings.HF_TOKEN:
    raise ValueError(
        "HF_TOKEN environment variable is not set."
    )
