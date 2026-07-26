from core.loader import DocumentLoader
from core.chunking import TextChunker
from core.embeddings import EmbeddingGenerator
from core.vectorstore import VectorStore
from core.retriever import Retriever
from core.chains import RAGChain
from core.config import settings

class RAGPipeline:

    def __init__(self):

        self.loader = DocumentLoader()

        self.chunker = TextChunker(
            chunk_size=settings.CHUNK_SIZE,
            overlap=settings.CHUNK_OVERLAP,
        )

        self.embedder = None
        self.vectorstore = None
        self.retriever = None
        self.chain = None
    # --------------------------

    def _load_embedder(self):

        if self.embedder is None:
            print("Loading Embedding Model...")
            self.embedder = EmbeddingGenerator()

    # --------------------------

    def _load_chain(self):

        if self.chain is None:
            print("Loading LangChain RAG Chain...")
            self.chain = RAGChain()

    # --------------------------

    def ingest(self, filepath):

        self._load_embedder()

        document = self.loader.load(filepath)

        chunks = self.chunker.chunk_document(document)

        embedded_chunks = self.embedder.embed_chunks(chunks)
        if not embedded_chunks:
            raise ValueError(
                "No text could be extracted from the uploaded document."
            )
        
        dimension = len(embedded_chunks[0]["embedding"])

        self.vectorstore = VectorStore(dimension)

        self.vectorstore.add_embeddings(embedded_chunks)

        self.retriever = Retriever(
            self.vectorstore,
            self.embedder,
        )

        print("\nDocument indexed successfully!")

    # --------------------------
    