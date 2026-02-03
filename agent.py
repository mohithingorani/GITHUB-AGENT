from langchain_ollama import ChatOllama
from tools.github_fetcher import fetch_github_profile
from langchain.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
    ToolMessage
)

llm = ChatOllama(
    model="gpt-oss:20b",
    temperature=0
).bind_tools([fetch_github_profile])


def github_agent_query(query: str):
    messages = [
        SystemMessage(
    content=(
        "You are a helpful assistant that fetches GitHub profile data using the provided tool. "
        "Respond in plain text only. "
        "Do not use Markdown, tables, bullet points, bold text, backticks, or any special formatting. "
        "Use only normal sentences and line breaks using '\\n'. "
        "Do not include HTML or any other formatting characters."
    )
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
