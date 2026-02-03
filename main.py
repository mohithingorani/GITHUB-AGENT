from langchain_ollama import ChatOllama
from tools.github_fetcher import fetch_github_profile
from langchain.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
    ToolMessage
)

llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0
).bind_tools([fetch_github_profile])

messages = [
    SystemMessage(
        content="You are a helpful assistant that fetches GitHub profile data using the provided tool."
    ),
    SystemMessage(
  content="""
  You must always explain your reasoning step by step.
  Provide statistics and a short summary paragraph.
  """
),
    HumanMessage(
        content=("What language does mohithingorani use the most in their public GitHub repositories?", ),
)]

response = llm.invoke(messages)
messages.append(response)

if isinstance(response, AIMessage):
    for call in response.tool_calls:
        tool_output = fetch_github_profile.invoke(call["args"])

        messages.append(
            ToolMessage(
                content=str(tool_output),
                tool_call_id=call["id"]
            )
        )

final_response = llm.invoke(messages)
print(final_response.content)


