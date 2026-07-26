from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

from core.llm import GroqLLM

from tools.wiki_search import wikipedia_search
from tools.tavily_search import tavily_search


class ToolAgent:

    def __init__(self):

        self.llm = GroqLLM().get_model()

        self.tools = [

            wikipedia_search,

            tavily_search,

        ]

        prompt = ChatPromptTemplate.from_messages(
            [

                (
                    "system",
                    """
You are an intelligent tool-using assistant.

Your job is to answer the user's question by deciding which tool(s) to use.

Available tools:

- wikipedia_search
- tavily_search

Guidelines:

• Use Wikipedia for definitions, people, concepts and history.

• Use Tavily for recent information or detailed web information.

• If both are useful, call both.

• Never make up information.

• Base your final answer ONLY on tool outputs.
"""
                ),

                ("human", "{input}"),

                ("placeholder", "{agent_scratchpad}")

            ]
        )

        agent = create_tool_calling_agent(

            self.llm,

            self.tools,

            prompt

        )

        self.executor = AgentExecutor(

            agent=agent,

            tools=self.tools,

            verbose=True,

            return_intermediate_steps=True

        )

    def invoke(self, question):

        result = self.executor.invoke(

            {

                "input": question

            }

        )

        return result