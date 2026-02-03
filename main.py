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


def github_agent_query(query: str):
    messages = [
        SystemMessage(
            content="You are a helpful assistant that fetches GitHub profile data using the provided tool."
        ),
        HumanMessage(
            content=query,
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

    return final_response.content

while(True):
    user_query = input("Enter your GitHub query (or 'exit' to quit): ")
    if user_query.lower() == 'exit':
        break

    answer = github_agent_query(user_query)
    print("Agent Response:")
    print(answer)