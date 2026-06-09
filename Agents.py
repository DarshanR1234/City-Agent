from dotenv import load_dotenv
import os
import requests

load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from langchain_core.messages import ToolMessage
from tavily import TavilyClient
from rich import print
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call


@tool
def get_weather(city: str) -> str:
    """Get current weather of a city"""

    api_key = os.getenv("OPENWEATHER_API_KEY")

    url = (
        f"http://api.openweathermap.org/data/2.5/weather"
        f"?q={city},IN&appid={api_key}&units=metric"
    )

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if str(data.get("cod")) != "200":
            return f"Error: {data.get('message', 'Could not fetch weather')}"

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]

        return f"Weather in {city}: {desc}, {temp}°C"

    except Exception as e:
        return f"Weather API Error: {str(e)}"



tavily_client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

@tool
def get_news(city: str) -> str:
    """Get latest news about a city"""

    try:
        response = tavily_client.search(
            query=f"latest news in {city}",
            search_depth="basic",
            max_results=3
        )

        results = response.get("results", [])

        if not results:
            return f"No news found for {city}"

        news_list = []

        for r in results:
            title = r.get("title", "No title")
            url = r.get("url", "")
            snippet = r.get("content", "")

            news_list.append(
                f"- {title}\n"
                f"  🔗 {url}\n"
                f"  📝 {snippet[:120]}..."
            )

        return (
            f"Latest news in {city}:\n\n"
            + "\n\n".join(news_list)
        )

    except Exception as e:
        return f"News API Error: {str(e)}"


llm = ChatMistralAI(
    model="mistral-small-2506"
)




@wrap_tool_call
def human_approval(request, handler):
    """Ask for approval before tool execution"""

    tool_name = request.tool_call["name"]

    confirm = input(
        f"Agent wants to call '{tool_name}'. Approve? (yes/no): "
    )

    if confirm.lower() != "yes":
        return ToolMessage(
            content="Tool call denied by user.",
            tool_call_id=request.tool_call["id"]
        )

    return handler(request)


agent = create_agent(
    llm,
    tools=[get_weather, get_news],
    system_prompt="""
You are a helpful city assistant.

You can:
- Answer city-related questions
- Provide weather updates
- Provide latest news

Remember information shared during the conversation whenever possible.
""",
    middleware=[human_approval]
)



chat_history = []

print("[bold green]City Agent | type exit to quit[/bold green]")

while True:

    user_input = input("You : ")

    if user_input.lower() == "exit":
        print("[bold red]Goodbye![/bold red]")
        break

    # Save user message
    chat_history.append({
        "role": "user",
        "content": user_input
    })

    try:

        result = agent.invoke({
            "messages": chat_history
        })

        bot_reply = result["messages"][-1].content

        # Save assistant reply
        chat_history.append({
            "role": "assistant",
            "content": bot_reply
        })

        print("bot :", bot_reply)

    except Exception as e:
        print(f"[red]Error:[/red] {e}")