from core.embeddings import EmbeddingGenerator
from core.vectorstore import VectorStore


class Retriever:
    """
    Retrieves the most relevant document chunks
    for a user query.
    """

    def __init__(
        self,
        vectorstore: VectorStore,
        embedder: EmbeddingGenerator,
    ):

        self.vectorstore = vectorstore
        self.embedder = embedder

    # ----------------------------------------

    def retrieve(
        self,
        question: str,
        top_k: int = 3,
    ):

        query_embedding = self.embedder.embed_text(question)

        results = self.vectorstore.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        return results



    # ----------------------------------------

    def get_all_chunks(self):

        return self.vectorstore.get_all_chunks()


    # ----------------------------------------

    def get_chunks_by_page(

        self,

        page

    ):

        return self.vectorstore.get_chunks_by_page(page)


    # ----------------------------------------

    def get_chunks_by_pages(

        self,

        start_page,

        end_page

    ):

        return self.vectorstore.get_chunks_by_pages(

            start_page,

            end_page

        )