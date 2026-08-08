# Doc_Wise_AI

**Doc_Wise_AI** is an AI-powered document question-answering and analysis system based on **Retrieval Augmented Generation (RAG)**. It allows users to upload documents and ask questions about their content through an interactive web interface.

The system retrieves relevant information from the uploaded document using **semantic search and FAISS**, and then generates responses using a **Llama Large Language Model through Groq**.

If the required information is not sufficiently available in the uploaded document, the system can use **Wikipedia and Tavily** to obtain external information and generate an appropriate response.

---

## Features

* Upload and process PDF, DOCX, and TXT documents.
* Extract text from uploaded documents.
* Split documents into smaller chunks.
* Generate semantic embeddings using BAAI BGE.
* Store embeddings using FAISS.
* Perform semantic similarity search.
* Answer questions using retrieved document context.
* Generate document summaries.
* Use Wikipedia for external information.
* Use Tavily for web search and fact verification.
* Manage AI workflow using LangGraph.
* Interactive web-based frontend.
* Flask-based backend.
* Cloud deployment support.

---

# Project Structure

```text
Doc_Wise_AI/
│
├── backend/
│   │
│   ├── agents/
│   │   ├── graph.py              # LangGraph workflow
│   │   ├── nodes.py              # Agent processing nodes
│   │   ├── state.py              # Shared workflow state
│   │   ├── fact_checker.py       # Fact verification agent
│   │   └── tool_agent.py         # Tool calling agent
│   │
│   ├── core/
│   │   ├── pipeline.py           # Main RAG pipeline
│   │   ├── models.py             # Data models
│   │   ├── chunking.py           # Text splitting
│   │   ├── embeddings.py         # Embedding generation
│   │   ├── vectorstore.py        # FAISS vector store
│   │   ├── llm.py                # Groq LLM configuration
│   │   └── config.py             # Application settings
│   │
│   ├── tools/
│   │   ├── summary_tool.py       # Document summarization
│   │   ├── tavily_search.py      # Tavily web search
│   │   └── wiki_search.py        # Wikipedia search
│   │
│   ├── uploads/                  # Temporary uploaded documents
│   │
│   └── app.py                    # Flask backend application
│
├── frontend/
│   │
│   ├── index.html                # Landing/upload page
│   ├── index1.html               # Chat interface
│   │
│   ├── css/
│   │   └── style.css             # Frontend styling
│   │
│   └── js/
│       └── script.js             # Frontend JavaScript
│
└── README.md
```

---

# System Workflow

The complete Doc_Wise_AI workflow is based on document retrieval, similarity checking, response generation, and external verification.

```text
                         User Question
                               │
                               ▼
                    Retrieve from Vector DB
                               │
                               ▼
                    Similarity Score Check
                               │
                  ┌────────────┴────────────┐
                  │                         │
          Score >= Threshold         Score < Threshold
                  │                         │
                  ▼                         ▼
       Answer from Document          Search Wikipedia
                  │                   Search Tavily
                  │                         │
                  ▼                         ▼
       Fact Check using Tavily      Generate Answer from
       (Verify Document Answer)     External Sources
                  │                         │
                  ▼                         ▼
             Final Response          Mention that answer
          from Uploaded Document     is not in document
```

---

# RAG Processing Workflow

The document processing workflow is:

```text
Document Upload
      │
      ▼
Document Loading
      │
      ▼
Text Extraction
      │
      ▼
Text Chunking
      │
      ▼
Embedding Generation
      │
      ▼
FAISS Vector Store
      │
      ▼
User Question
      │
      ▼
Query Embedding
      │
      ▼
Semantic Retrieval
      │
      ▼
Similarity Score
      │
      ▼
Relevant Context
      │
      ▼
Llama + Groq
      │
      ▼
Final Response
```

---

# Agent Workflow

LangGraph is used to manage the decision-making workflow of the application.

```text
User Query
    │
    ▼
Retrieve Node
    │
    ▼
Decision / Routing
    │
    ├──────────────► Document Answer
    │
    └──────────────► External Tools
                         │
                 ┌───────┴────────┐
                 ▼                ▼
             Wikipedia         Tavily
                 │                │
                 └───────┬────────┘
                         ▼
                    Fact Checker
                         │
                         ▼
                  Final Response
```

---

# Core Components

## Document Loader

Extracts text from uploaded documents and prepares it for further processing.

Supported formats:

* PDF
* DOCX
* TXT

---

## Chunking

Large documents are divided into smaller sections to make retrieval more efficient and preserve relevant context.

---

## Embeddings

The project uses:

```text
BAAI/bge-small-en-v1.5
```

to convert text into numerical vector representations.

---

## FAISS Vector Store

FAISS is used to store and search document embeddings.

The system uses vector similarity to retrieve the most relevant document chunks for a user's question.

---

## Retriever

The Retriever converts the user's question into an embedding and searches the FAISS vector store for relevant document chunks.

---

## LLM

The project uses a **Llama-based Large Language Model through Groq** to generate responses from the retrieved context.

---

## LangGraph

LangGraph manages the workflow by connecting different processing nodes and routing the query according to the similarity score and required operation.

---

## Summary Tool

The Summary Tool generates a concise summary of the uploaded document using the LLM.

---

## Wikipedia Tool

The Wikipedia Tool retrieves additional information from Wikipedia when the required information is not sufficiently available in the uploaded document.

---

## Tavily Tool

The Tavily Tool performs web searches and provides external evidence for answering and verifying queries.

---

## Fact Checker

The Fact Checker validates document-based answers using external evidence, particularly Tavily search results.

---

# Technology Stack

| Component            | Technology             |
| -------------------- | ---------------------- |
| Programming Language | Python                 |
| Backend              | Flask                  |
| Frontend             | HTML, CSS, JavaScript  |
| LLM                  | Llama                  |
| LLM Inference        | Groq                   |
| Embedding Model      | BAAI/bge-small-en-v1.5 |
| Embedding Framework  | Sentence Transformers  |
| Vector Database      | FAISS                  |
| Agent Framework      | LangGraph              |
| External Search      | Tavily                 |
| Knowledge Source     | Wikipedia              |
| PDF Processing       | PyMuPDF                |
| DOCX Processing      | python-docx            |


---
# Running the Application

Navigate to the backend directory:

```bash
cd backend
```

Run the Flask application:

```bash
python app.py
```

The application can then be accessed through the local Flask server shown in the terminal.

---

# Example

### Step 1: Upload Document

```text
Machine_Learning.pdf
```

### Step 2: Ask a Question

```text
What is supervised learning?
```

### Step 3: Retrieval

The system converts the question into an embedding and searches the FAISS vector store.

### Step 4: Context

Relevant document chunks are retrieved.

### Step 5: Generation

The retrieved context is passed to the Llama model through Groq.

### Step 6: Response

```text
Supervised learning is a machine learning approach
where models are trained using labelled datasets
to make predictions.
```

If the required information cannot be sufficiently retrieved from the document, the system can search external sources such as Wikipedia and Tavily.

---

# Deployment

The application can be deployed using cloud platforms such as **Render** for the Flask backend.

---

# Project Objective

The main objective of Doc_Wise_AI is to develop an intelligent document assistant that combines **RAG, semantic search, LLMs, LangGraph, and external knowledge sources** to provide reliable and context-aware answers from uploaded documents.

---

# Future Scope

Possible future improvements include:

* Multi-document conversations.
* OCR for scanned documents.
* Table and image understanding.
* Hybrid keyword + semantic retrieval.
* Improved reranking.
* User authentication.
* Document history and management.
* Voice-based interaction.
* Advanced AI agents.
* Citation generation.

---

# Conclusion

Doc_Wise_AI demonstrates the practical implementation of a modern **Retrieval Augmented Generation system**. By combining document processing, embeddings, FAISS, LangGraph, Llama, Groq, Wikipedia, and Tavily, the system provides an interactive platform for document analysis, question answering, summarization, and fact verification.
