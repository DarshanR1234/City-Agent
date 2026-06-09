from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from rich import print


@tool
def count_words(text: str) -> int:
    """Use this tool whenever the user asks for the number of words in a text."""
    return len(text.split())


tools = {
    "count_words": count_words
}

llm = ChatMistralAI(model="mistral-small-2506")
llm_with_tools = llm.bind_tools([count_words])

messages = []

while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit"]:
        break

    messages.append(HumanMessage(content=user_input))

    response = llm_with_tools.invoke(messages)

    if response.tool_calls:
        messages.append(response)

        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]

            tool_result = tools[tool_name].invoke(tool_call["args"])

            messages.append(
                ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call["id"]
                )
            )
        print("Tool Calls:", response.tool_calls)
        response = llm_with_tools.invoke(messages)

    print(f"AI: {response.content}")

    messages.append(response)