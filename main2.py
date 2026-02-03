from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain_ollama import ChatOllama
from langchain.messages import HumanMessage,SystemMessage
from tools.fetcher_for_agent import fetch_github_profile
import pprint

llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0,
).bind_tools([fetch_github_profile])

agent = create_agent(
    model=llm,
    tools=[fetch_github_profile],
    
)

messages = [
    SystemMessage(
        content="You are a helpful assistant that fetches GitHub profile data using the provided tool."
    ),
    SystemMessage(
        content="""
        If the answer requires GitHub data:
        - Call the appropriate tool
        - Do NOT describe the tool call in text
        - Emit a real tool call
        """
    ),
    SystemMessage(
    content="""    You must always explain your reasoning step by step.
    Provide statistics and a short summary paragraph including key points at the end of your answer with numbers.
    """
),
    HumanMessage(
        content="What language does mohithingorani use the most in their public GitHub repositories?"
    )
]

response = agent.invoke({
    "messages": messages
})
print(response["messages"][-1].content)