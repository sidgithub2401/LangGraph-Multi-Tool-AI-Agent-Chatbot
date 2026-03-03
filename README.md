
# 🚀 LangGraph Multi-Tool AI Agent Chatbot

An advanced AI-powered multi-tool chatbot built using **LangGraph**, **OpenAI GPT-4.1-mini**, and **Streamlit**, capable of handling real-world tasks such as:

* 📈 Stock Price Retrieval
* 🌦 Weather Information
* 🧮 Calculator Operations
* ✈️ Trip Cost Estimation
* 🔍 Live Web Search
* 📧 Sending Emails

This project demonstrates an **Agentic AI system with tool-calling, memory persistence, and streaming responses**, making it suitable for production-level AI applications.

---

## 🏗 Architecture Overview

The application is built using:

* **LangGraph StateGraph** for agent orchestration
* **OpenAI GPT-4.1-mini** for reasoning and tool selection
* **ToolNode** for dynamic tool execution
* **SQLite Checkpointer** for conversation memory
* **Streamlit** for real-time chat UI
* External APIs:

  * Weather API
  * AlphaVantage Stock API
  * Gmail SMTP

---

## 🧠 How It Works

1. User sends a message via Streamlit UI.
2. The message is passed to the LangGraph `StateGraph`.
3. The LLM decides:

   * Respond directly
   * OR call a tool
4. If tool is needed:

   * ToolNode executes the tool
   * Result is passed back to LLM
5. Final response is streamed back to UI.
6. Conversation is saved using SQLite checkpointer.

---

## 📂 Project Structure

```
├── Chatbot.py        # Backend LangGraph agent
├── frontend.py       # Streamlit UI
├── requirements.txt
├── .env              # API keys (not committed)
├── demo.db           # SQLite memory DB
└── README.md
```

---

## 🛠 Tools Implemented

| Tool               | Description                      |
| ------------------ | -------------------------------- |
| get_stock_price    | Fetches daily stock data         |
| get_weather_status | Retrieves weather information    |
| calculator         | Performs arithmetic operations   |
| estimate_trip_cost | AI-based travel budget estimator |
| send_mail          | Sends real email via Gmail       |
| DuckDuckGoSearch   | Performs web search              |

---

## 🔐 Environment Variables

Create a `.env` file:

```
Open_AI_API=your_openai_key
waether_api_key=your_weather_key
stock_price_api_key=your_stock_key
EMAIL_ADDRESS=your_email
EMAIL_PASSWORD=your_app_password
```

---

## ▶️ Run Locally

```bash
pip install -r requirements.txt
streamlit run frontend.py
```

---

## 🌍 Deployment

This project can be deployed for free using:

* Streamlit Community Cloud (Recommended)
* Render
* Railway

---

## 🧩 Features

* Multi-thread chat support
* Persistent memory using SQLite
* Real-time streaming responses
* Tool usage status indicator
* Modular tool architecture
* Agentic decision-making using LangGraph

---

## 📈 Why This Project Matters

This demonstrates:

* Agentic AI Architecture
* Tool Calling & Orchestration
* Memory Management
* Production-ready UI
* Real-world API Integration

It is designed as a **portfolio-ready GenAI system** for AI/ML & Generative AI roles.

---

## 👨‍💻 Author

Sid Sha
AI/ML Engineer | GenAI Enthusiast

---

## ⭐ If You Like This Project

Star the repository and connect with me on LinkedIn.
