import faiss
import numpy as np

from core.chunking import DocumentChunk


class VectorStore:
    """
    Stores embeddings using FAISS.
    """

    def __init__(self, embedding_dimension: int):

        self.index = faiss.IndexFlatIP(embedding_dimension)

        self.chunks: list[DocumentChunk] = []

    # -----------------------------------

    def add_embeddings(self, embedded_chunks):

        vectors: list[np.ndarray] = []
        for item in embedded_chunks:

            vectors.append(item["embedding"])
            self.chunks.append(item["chunk"])

        vectors = np.array(vectors).astype("float32")

        self.index.add(vectors)

    # -----------------------------------

    def search(self, query_embedding, top_k=3):
     
        if self.index.ntotal == 0:
            return []

        top_k = min(top_k, len(self.chunks))

        query_embedding = np.array(
            [query_embedding]
        ).astype("float32")

        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for score, idx in zip(scores[0], indices[0]):

            if idx == -1:
                continue

            results.append({
                "score": float(score),
                "chunk": self.chunks[idx]
            })

        return results


        # -----------------------------------
    # Return all chunks
    # -----------------------------------

    def get_all_chunks(self):

        return self.chunks


    # -----------------------------------
    # Return chunks from one page
    # -----------------------------------

    def get_chunks_by_page(self, page):

        return [

            chunk

            for chunk in self.chunks

            if chunk.page_number == page

        ]


    # -----------------------------------
    # Return chunks from page range
    # -----------------------------------

    def get_chunks_by_pages(

        self,

        start_page,

        end_page

    ):

        return [

            chunk

            for chunk in self.chunks

            if start_page <= chunk.page_number <= end_page

        ]