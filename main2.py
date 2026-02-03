from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain_ollama import ChatOllama
from langchain.messages import HumanMessage,SystemMessage
from tools.fetcher_for_agent import fetch_github_profile


llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0,
).bind_tools([fetch_github_profile])

llm2= ChatOllama(
    model="gpt-oss:20b",
    temperature=0,
).bind_tools([fetch_github_profile])

agent = create_agent(
    model=llm,
    tools=[fetch_github_profile],
    
)


def agent_response(prompt: str) -> str:
        messages = [
            SystemMessage(
                content="""
            You are a GitHub analysis assistant.

            Your job:
            - Answer the user's question accurately and concisely.
            - Use GitHub data when required.

            Tool usage rules:
            - If answering requires GitHub data, you MUST call the appropriate tool.
            - Do NOT describe tool calls in text.
            - Emit a real tool call when needed.
            - Never invent or assume GitHub data.

            Reasoning & output rules:
            - Explain your reasoning step by step.
            - Use statistics when available.
            - End with a short numbered summary.

            If a comparison is requested (e.g. "better than"):
            - Fetch data for ALL entities before answering.
            - If criteria is unclear, ask for clarification.
            """
                    ),
        HumanMessage(content=prompt),
        ]

        response = agent.invoke({"messages": messages})
        return response["messages"][-1].content
    

if __name__ == "__main__":
    while True:
        prompt = input("Enter your prompt: ")
        response = agent_response(prompt)
        print("Agent Response:")
        print(response)
