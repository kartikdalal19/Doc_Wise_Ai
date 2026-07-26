
from huggingface_hub import InferenceClient
from core.config import settings
import numpy as np



class EmbeddingGenerator:


    def __init__(self, model_name=None):

        if model_name is None:
            model_name = settings.HF_EMBEDDING_MODEL


        print(
            f"Using HuggingFace Embedding API: {model_name}"
        )


        self.client = InferenceClient(
            token=settings.HF_TOKEN
        )


        self.model = model_name



    # ----------------------------------------
    # Single text embedding
    # ----------------------------------------

    def embed_text(self, text: str):

        vector = self.client.feature_extraction(
            text,
            model=self.model
        )


        vector = np.array(
            vector,
            dtype="float32"
        )


        return vector



    # ----------------------------------------
    # Multiple chunks embedding
    # ----------------------------------------

    def embed_chunks(self, chunks: list):


        texts = [
            chunk.text
            for chunk in chunks
        ]


        embedded_chunks = []


        for chunk, text in zip(
            chunks,
            texts
        ):


            vector = self.client.feature_extraction(
                text,
                model=self.model
            )


            vector = np.array(
                vector,
                dtype="float32"
            )


            embedded_chunks.append(
                {
                    "chunk": chunk,
                    "embedding": vector
                }
            )


        return embedded_chunks
