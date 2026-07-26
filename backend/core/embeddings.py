from sentence_transformers import SentenceTransformer
from core.config import settings


class EmbeddingGenerator:

    def __init__(self, model_name=None):

        if model_name is None:
            model_name = settings.EMBEDDING_MODEL

        print(f"Loading embedding model: {model_name}")

        self.model = SentenceTransformer(
            model_name,
            device="cpu"
        )


    # ----------------------------------------

    def embed_text(self, text: str):
        return self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True
        )


    # ----------------------------------------

    def embed_chunks(self, chunks: list):

        texts = [
            chunk.text 
            for chunk in chunks
        ]

        vectors = self.model.encode(
            texts,
            batch_size=4,          # important for 8GB RAM
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False
        )


        embedded_chunks = []

        for chunk, vector in zip(chunks, vectors):

            embedded_chunks.append(
                {
                    "chunk": chunk,
                    "embedding": vector
                }
            )


        return embedded_chunks