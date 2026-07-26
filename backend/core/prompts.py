class PromptBuilder:

    @staticmethod
    def build_prompt(question, retrieved_chunks):

        context = "\n\n".join(
            chunk["chunk"].text
            for chunk in retrieved_chunks
        )

        return f"""
You are DocWise AI.

You must answer ONLY from the supplied context.

If the answer is not available,
reply exactly:

"I could not find this information in the uploaded document."

Always answer clearly.

=========================
Context
=========================

{context}

=========================
Question
=========================

{question}

=========================
Answer
=========================
"""