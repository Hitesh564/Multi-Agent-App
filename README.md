# 🧠 NovaMind - Adaptive Multi-Agent AI System

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Next.js](https://img.shields.io/badge/Next.js-14-black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688)

NovaMind is a professional-grade, multi-agent artificial intelligence workspace. It intelligently routes user queries to specialized agents, supporting persistent memory, real-time tool execution (news, weather), and Retrieval-Augmented Generation (RAG) for interacting with uploaded documents.

---

## ✨ Key Features

- **🧠 Multi-Agent Architecture**: A smart Router Agent analyzes your prompt and dynamically hands it off to the best-suited specialist (General LLM, Tool Agent, or RAG Agent).
- **📄 Document Intelligence (RAG)**: Upload PDFs or text files. The system chunks, embeds, and stores them in a local FAISS vector database for highly accurate context retrieval.
- **🛠️ Live Tools**: Connects to external APIs to fetch real-time data, including current weather and latest global news headlines.
- **💾 Persistent Memory**: Integrated with Supabase to store your chat history across sessions permanently.
- **🎨 Cinematic UI**: A sleek, fully responsive Next.js frontend featuring smooth animations, dark mode aesthetics, and specialized panels for documents and memory.

---

## 🛠️ Technology Stack

### Frontend
- **Framework**: [Next.js](https://nextjs.org/) (App Router, React 18)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/) & Vanilla CSS for glassmorphism and animations
- **Icons**: [Lucide React](https://lucide.dev/)
- **Language**: TypeScript

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (High-performance Python API)
- **LLM Provider**: [Groq](https://groq.com/) (Using `llama-3.1-8b-instant` for ultra-fast inference)
- **Vector Store**: [FAISS](https://github.com/facebookresearch/faiss) (Local vector database for lightning-fast semantic search)
- **Embeddings**: `all-MiniLM-L6-v2` via HuggingFace
- **Database**: [Supabase](https://supabase.com/) (PostgreSQL for message history)

---

## 🏗️ How It Works (System Architecture)

1. **User Input**: The user sends a message via the Next.js chat interface.
2. **Context & Memory Retrieval**: The backend fetches the last 4 messages from Supabase and checks local memory items.
3. **Router Agent**: A classification algorithm determines the intent of the query:
   - *Is it a question about an uploaded document?* ➡️ **RAG Agent**
   - *Is it asking for current news or weather?* ➡️ **Tool Agent**
   - *Is it a general conversation?* ➡️ **General LLM Agent**
4. **Execution**:
   - **RAG Agent**: Converts the query to a vector, searches the FAISS index, retrieves the top document chunks, and synthesizes an answer strictly based on the text.
   - **Tool Agent**: Identifies the necessary external API (NewsAPI, OpenWeather), fetches the JSON data, and formats a clean response.
   - **General Agent**: Generates a natural, conversational response using Groq.
5. **Output Formatting**: The Formatter Agent ensures the final output is clean, professional, and free of markdown clutter before sending it back to the UI.

---

## 🚀 Getting Started

### Prerequisites
- Node.js (v18+)
- Python (3.10+)
- A [Groq](https://console.groq.com/) API Key
- A [Supabase](https://supabase.com/) account
- API keys for [NewsAPI](https://newsapi.org/) and [OpenWeather](https://openweathermap.org/) (optional, for tools)

### 1. Backend Setup

Open a terminal in the root directory:

```bash
# Create a virtual environment
python -m venv .venv

# Activate the environment (Windows)
.venv\Scripts\activate
# Activate the environment (Mac/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Create a `.env` file in the root directory based on the `.env.example`:
```env
# Example .env configuration
GROQ_API_KEY=your_groq_api_key
LLM_PROVIDER=groq
LLM_MODEL=llama-3.1-8b-instant

NEWS_API_KEY=your_news_api_key
OPENWEATHER_API_KEY=your_weather_api_key

SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

Run the backend server:
```bash
uvicorn server:app --port 8000 --reload
```

### 2. Frontend Setup

Open a **new** terminal and navigate to the frontend folder:

```bash
cd frontend

# Install dependencies
npm install

# Start the Next.js development server
npm run dev
```

### 3. Start Chatting!
Open your browser and navigate to `http://localhost:3000`. 

---

## 📂 Project Structure

```
Multi-Agent-App/
├── agents/                 # Logic for RAG, Tool, Router, and LLM agents
├── config/                 # Application settings and environment parsing
├── data/                   # Local storage for FAISS indices and JSON metadata
├── frontend/               # Next.js React application
├── services/               # Core services (FAISS, Supabase, Embeddings)
│   └── tools/              # External API integrations (News, Weather)
├── utils/                  # Helpers (PDF parsers, chunkers, loggers)
├── server.py               # FastAPI backend entry point
└── requirements.txt        # Python dependencies
```

---

## 🤝 Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request if you'd like to add a new Tool Agent or improve the UI.

## 📝 License
This project is licensed under the MIT License.
