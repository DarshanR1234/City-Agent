# City Agent 🚀

A conversational AI agent built with **LangChain**, **Mistral AI**, **OpenWeather API**, and **Tavily Search API**.

The agent can:

* 🌤 Get current weather for Indian cities
* 📰 Fetch latest city-related news
* 🤖 Use LangChain tools and agents
* 🔒 Ask for human approval before executing any tool
* 💬 Maintain conversation history during the session

---

## Features

### Weather Tool

Uses the OpenWeather API to fetch:

* Current temperature
* Weather conditions
* Real-time weather updates

Example:

User: What's the weather in Mumbai?

Bot: Weather in Mumbai: scattered clouds, 29°C

---

### News Tool

Uses Tavily Search API to retrieve:

* Latest city news
* News article titles
* Source URLs
* Short summaries

Example:

User: Latest news in Delhi

Bot:

* New Metro Expansion Announced
  🔗 https://...
  📝 Delhi government announced...

---

### Human-in-the-Loop Approval

Before any tool is executed, the user is asked for permission:

```text
Agent wants to call 'get_weather'. Approve? (yes/no):
```

If denied:

```text
Tool call denied by user.
```

This adds safety and control over agent actions.

---

## Project Structure

```text
city-agent/
│
├── app.py
├── .env
├── requirements.txt
└── README.md
```

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/city-agent.git

cd city-agent
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Required Packages

```txt
langchain
langchain-mistralai
python-dotenv
requests
tavily-python
rich
```

Install manually:

```bash
pip install langchain langchain-mistralai python-dotenv requests tavily-python rich
```

---

## Environment Variables

Create a `.env` file:

```env
OPENWEATHER_API_KEY=your_openweather_api_key

TAVILY_API_KEY=your_tavily_api_key

MISTRAL_API_KEY=your_mistral_api_key
```

---

## Getting API Keys

### OpenWeather

1. Create account at https://openweathermap.org
2. Generate API key
3. Add it to `.env`

### Tavily

1. Create account at https://tavily.com
2. Generate API key
3. Add it to `.env`

### Mistral AI

1. Create account at https://console.mistral.ai
2. Generate API key
3. Add it to `.env`

---

## Running the Application

```bash
python app.py
```

Output:

```text
City Agent | type exit to quit
```

---

## Example Conversation

```text
You : What's the weather in Surat?

Agent wants to call 'get_weather'. Approve? (yes/no):
yes

Bot : Weather in Surat: clear sky, 31°C
```

```text
You : Latest news in Ahmedabad

Agent wants to call 'get_news'. Approve? (yes/no):
yes

Bot :
Latest news in Ahmedabad:

- News Title
  🔗 https://...
  📝 News summary...
```

---

## How It Works

### 1. User Message

User enters a query.

### 2. LangChain Agent

The Mistral model decides whether a tool is required.

### 3. Human Approval Middleware

Before tool execution:

```python
@wrap_tool_call
def human_approval(request, handler):
```

The user must approve.

### 4. Tool Execution

Agent calls:

* `get_weather()`
* `get_news()`

### 5. Response Generation

Tool output is returned to the LLM and transformed into a natural language response.

---

## Technologies Used

* LangChain
* Mistral AI
* OpenWeather API
* Tavily Search API
* Python
* Rich
* dotenv

---

## Future Improvements

* Multi-city weather comparison
* Weather forecasts
* Persistent memory using LangGraph
* Additional city services

  * Hotels
  * Restaurants
  * Traffic updates
  * Events
* Streamlit UI
* Voice assistant support

---

## License

MIT License

Feel free to use, modify, and distribute this project.
