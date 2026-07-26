from langchain_core.prompts import ChatPromptTemplate
from core.llm import GroqLLM


class RAGChain:

    def __init__(self):

        self.llm = GroqLLM().get_model()

        # =====================================================
        # Document Prompt
        # =====================================================

        self.document_prompt = ChatPromptTemplate.from_template(
"""
You are DocWise AI.

You answer questions ONLY from the uploaded document.

Rules:


1. The **Answer** must come ONLY from the uploaded document.
2. Never modify, exaggerate, or contradict the information found in the document.
3. After providing the answer, you MAY use your general programming or domain knowledge ONLY to explain the answer in simpler words.
4. The explanation must never contradict the document.
5. If appropriate, provide one simple, practical example to help the user understand the concept.
6. Use clear headings and separate every section with a blank line.
7. Keep explanations concise, beginner-friendly, and easy to read.
8. If the answer is not present in the document, reply EXACTLY:


I don't know from the document.

Document Context:

{context}

Question:

{question}

Answer:
"""
        )

        # =====================================================
        # Web Prompt
        # =====================================================

        self.web_prompt = ChatPromptTemplate.from_template(
"""
You are DocWise AI.

The uploaded document does not contain the requested information.

Answer ONLY using the external evidence below.

Wikipedia

{wiki}

--------------------------------------------------

Tavily

{tavily}

--------------------------------------------------
Rules:

1. First clearly state:

"The answer is not available in the uploaded document."

2. Carefully inspect BOTH the Wikipedia and Tavily evidence.

3. If EITHER Wikipedia OR Tavily contains sufficient information,
answer the question using the available source.

4. Do NOT require both sources to contain information.

5. If both sources contain useful information,
combine them naturally.

6. If one source failed or is unrelated,
ignore it and use the other source.

7. Answer in the following format using proper Markdown headings and blank lines:

## Answer

(Give a short direct answer.)

## Explanation

(Explain the concept in simple language using ONLY the provided external evidence.)

## Example

(Provide a simple example if the external evidence contains enough information.
If no suitable example exists, write "No example available.")

## Source

(State whether the information comes from Wikipedia, Tavily, or both.)

8. Keep the explanation concise, accurate, and focused on the user's question.

9. Never invent facts or use knowledge outside the provided external evidence.

10. Reply with:

"I could not find a reliable answer."

ONLY if BOTH Wikipedia AND Tavily fail to provide relevant information.

11. Ignore failed searches, empty results, or unrelated information from either source if the other source provides a valid answer.

12. Return the answer using proper Markdown formatting with headings and blank lines exactly as shown above.

Answer:
"""
        )

        # =====================================================
        # Chains
        # =====================================================

        self.document_chain = (
            self.document_prompt
            | self.llm
        )

        self.web_chain = (
            self.web_prompt
            | self.llm
        )

    # =====================================================
    # Document QA
    # =====================================================

    def document_invoke(
        self,
        context: str,
        question: str
    ) -> str:
        
        response = self.document_chain.invoke(
            {
                "context": context,
                "question": question
            }
        )

        return response.content

    # =====================================================
    # Web QA
    # =====================================================

    def web_invoke(
        self,
        question: str,
        wiki: str,
        tavily: str
    ) -> str:
        
        response = self.web_chain.invoke(
            {
                "question": question,
                "wiki": wiki,
                "tavily": tavily
            }
        )

        return response.content










