
# from huggingface_hub import InferenceClient
# from core.config import settings
# import numpy as np



# class EmbeddingGenerator:


#     def __init__(self, model_name=None):

#         if model_name is None:
#             model_name = settings.HF_EMBEDDING_MODEL


#         print(
#             f"Using HuggingFace Embedding API: {model_name}"
#         )


#         self.client = InferenceClient(
#             token=settings.HF_TOKEN
#         )


#         self.model = model_name



#     # ----------------------------------------
#     # Single text embedding
#     # ----------------------------------------

#     def embed_text(self, text: str):

#         vector = self.client.feature_extraction(
#             text,
#             model=self.model
#         )


#         vector = np.array(
#             vector,
#             dtype="float32"
#         )


#         return vector



#     # ----------------------------------------
#     # Multiple chunks embedding
#     # ----------------------------------------

#     def embed_chunks(self, chunks: list):


#         texts = [
#             chunk.text
#             for chunk in chunks
#         ]


#         embedded_chunks = []


#         for chunk, text in zip(
#             chunks,
#             texts
#         ):


#             vector = self.client.feature_extraction(
#                 text,
#                 model=self.model
#             )


#             vector = np.array(
#                 vector,
#                 dtype="float32"
#             )


#             embedded_chunks.append(
#                 {
#                     "chunk": chunk,
#                     "embedding": vector
#                 }
#             )


#         return embedded_chunks










# cloudflare
import time
import requests
import numpy as np

from core.config import settings


class EmbeddingGenerator:

    def __init__(self, model_name=None):

        self.model = (
            model_name or settings.CF_EMBEDDING_MODEL
        )

        self.api_url = (
            f"https://api.cloudflare.com/client/v4/accounts/"
            f"{settings.CF_ACCOUNT_ID}/ai/run/{self.model}"
        )

        self.headers = {
            "Authorization": f"Bearer {settings.CF_API_TOKEN}",
            "Content-Type": "application/json"
        }

        self.batch_size = 32
        self.max_retries = 3

        print(f"Using Cloudflare Embedding API: {self.model}")

    def _get_embeddings(self, texts):

        for attempt in range(self.max_retries):

            try:
                response = requests.post(
                    self.api_url,
                    headers=self.headers,
                    json={
                        "text": texts,
                        "pooling": "mean"
                    },
                    timeout=60
                )

                response.raise_for_status()

                result = response.json()["result"]

                vectors = np.asarray(
                    result["data"],
                    dtype=np.float32
                )

                if vectors.ndim != 2 or vectors.shape[1] != 384:
                    raise ValueError(
                        f"Unexpected embedding shape: {vectors.shape}"
                    )

                return vectors

            except Exception as e:

                print(
                    f"Embedding request failed "
                    f"({attempt + 1}/{self.max_retries}): {e}"
                )

                if attempt == self.max_retries - 1:
                    raise

                time.sleep(2 ** attempt)

    def embed_text(self, text: str):

        vectors = self._get_embeddings([text])

        vector = vectors[0]

        print("\n===== QUERY EMBEDDING =====")
        print("Shape :", vector.shape)
        print("Norm  :", np.linalg.norm(vector))
        print("===========================\n")

        return vector

    def embed_chunks(self, chunks: list):

        texts = [
            chunk.text for chunk in chunks
        ]

        embedded_chunks = []

        for start in range(0, len(texts), self.batch_size):

            batch = texts[
                start:start + self.batch_size
            ]

            vectors = self._get_embeddings(batch)

            for chunk, vector in zip(
                chunks[start:start + self.batch_size],
                vectors
            ):

                print("\n========== CHUNK ==========")
                print("Page :", chunk.page_number)
                print("Shape:", vector.shape)
                print("Norm :", np.linalg.norm(vector))
                print("===========================\n")

                embedded_chunks.append({
                    "chunk": chunk,
                    "embedding": vector
                })

        return embedded_chunks
