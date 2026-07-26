import re

from langchain_core.prompts import ChatPromptTemplate

from core.llm import GroqLLM


class SummaryTool:

    def __init__(self, retriever):

        self.retriever = retriever

        self.llm = GroqLLM().get_model()

        self.prompt = ChatPromptTemplate.from_template(
"""
You are DocWise AI.

You are given text extracted from a document.

Your task is to produce a high-quality study summary.

Guidelines:

1. Explain the main topic in simple language.
2. Highlight the most important ideas.
3. Preserve technical terms from the document.
4. Do NOT invent information.
5. Organize the summary using the headings below.
6. If the document contains code, briefly explain what the code does instead of copying it line by line.
7. If the document contains formulas, explain what they mean.
8. Keep the summary concise but complete.


Return the summary in this format:

# Overview

(sentences based on context data)

# Key Points

- Point 1
- Point 2
- Point 3

# Important Concepts

- ...

# Conclusion

(1-2 sentences)

Document Text:

{text}

Summary:
"""
        )

        self.chain = self.prompt | self.llm

    # ======================================================
    # Entire document summary
    # ======================================================

    def summarize_document(self):

        chunks = self.retriever.get_all_chunks()

        text = "\n\n".join(

            chunk.text

            for chunk in chunks

        )

        return self.chain.invoke(

            {

                "text": text

            }

        ).content

    # ======================================================
    # Single page summary
    # ======================================================

    def summarize_page(self, page):

        chunks = self.retriever.get_chunks_by_page(page)

        if not chunks:

            return f"No content found on page {page}."

        text = "\n\n".join(

            chunk.text

            for chunk in chunks

        )

        return self.chain.invoke(

            {

                "text": text

            }

        ).content

    # ======================================================
    # Page range summary
    # ======================================================

    def summarize_pages(

        self,

        start,

        end

    ):

        chunks = self.retriever.get_chunks_by_pages(

            start,

            end

        )

        if not chunks:

            return "No content found."

        text = "\n\n".join(

            chunk.text

            for chunk in chunks

        )

        return self.chain.invoke(

            {

                "text": text

            }

        ).content

    # ======================================================
    # Main Entry
    # ======================================================

    def invoke(

        self,

        question

    ):

        q = question.lower()

        # ----------------------------------
        # Entire document
        # ----------------------------------

        if "entire" in q or "whole" in q or "full document" in q:

            return self.summarize_document()

        # ----------------------------------
        # Page range
        # ----------------------------------

        match = re.search(

            r"pages?\s+(\d+)\s*[-to]+\s*(\d+)",

            q

        )

        if match:

            start = int(match.group(1))

            end = int(match.group(2))

            return self.summarize_pages(

                start,

                end

            )

        # ----------------------------------
        # Single page
        # ----------------------------------

        match = re.search(

            r"page\s+(\d+)",

            q

        )

        if match:

            page = int(match.group(1))

            return self.summarize_page(page)

        # ----------------------------------
        # Default
        # ----------------------------------

        return self.summarize_topic(question)



        # ======================================================
    # Semantic Topic Summary (FAISS)
    # ======================================================

    def summarize_topic(
        self,
        question
    ):

        results = self.retriever.retrieve(
            question,
            top_k=10
        )

        if not results:

            return "No relevant information found."

        text = "\n\n".join(

            item["chunk"].text

            for item in results

        )

        return self.chain.invoke(

            {
                "text": text
            }

        ).content
        














    #     What this supports immediately

    # These queries will now work:

    # Summarize the document
    # Give me the summary of the whole document
    # Summarize page 4
    # Give summary of page 12
    # Summarize pages 3-7
    # Summarize pages 3 to 7