# Product Requirements Document (PRD)

## Adaptive Multi-Agent AI Assistant
### with RAG and Intelligent Tool Routing

---

| Field | Details |
|---|---|
| **Document Version** | v1.0 |
| **Status** | Draft – Ready for Development |
| **Author** | AI Product Team |
| **Last Updated** | 2025 |
| **Audience** | Engineers, Architects, Stakeholders, Portfolio Reviewers |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement](#2-problem-statement)
3. [Goals and Objectives](#3-goals-and-objectives)
4. [User Personas](#4-user-personas)
5. [Use Cases / User Stories](#5-use-cases--user-stories)
6. [System Architecture Overview](#6-system-architecture-overview)
7. [Functional Requirements](#7-functional-requirements)
8. [Non-Functional Requirements](#8-non-functional-requirements)
9. [Technical Design (High-Level)](#9-technical-design-high-level)
10. [Data Flow / Workflow](#10-data-flow--workflow)
11. [Risks and Mitigations](#11-risks-and-mitigations)
12. [Future Enhancements](#12-future-enhancements)
13. [Success Metrics](#13-success-metrics)

---

## 1. Executive Summary

The **Adaptive Multi-Agent AI Assistant** is a production-grade intelligent assistant that moves beyond the limitations of a single-model chatbot. Instead of processing every query through one generic model, it uses a **Router Agent** as its decision-making core — dynamically dispatching queries to one of three specialized agents:

- An **LLM Agent** for general conversational queries
- A **RAG Agent** for document-grounded question answering (PDF-based)
- A **Tool Agent** for real-time data retrieval via external APIs

The system is designed to be **modular**, **extensible**, and **production-ready** — built with Python, Streamlit, FAISS, and Groq/Together AI APIs. This architecture reflects how modern enterprise AI systems are built: not as monolithic chatbots, but as orchestrated agent pipelines that route intelligence where it's needed most.

This document defines the full product scope, architecture, and requirements to guide engineering implementation and serve as a portfolio artifact demonstrating senior-level AI system design.

---

## 2. Problem Statement

### 2.1 Current Landscape

Most AI assistants deployed today suffer from a fundamental architectural flaw: **one-size-fits-all inference**. Whether the user asks a general knowledge question, queries an internal document, or needs live stock prices — the same model is hit with the same prompt, leading to:

- **Hallucinated answers** when real-time data is needed
- **Missed context** when domain-specific documents exist but aren't retrieved
- **Wasted compute** when a simple LLM call could have sufficed
- **Poor user experience** — no structure, no sourcing, no adaptability

### 2.2 The Gap

There is no lightweight, open-architecture solution that:
- Intelligently **classifies** the type of query before processing
- **Selects** the right agent or tool based on that classification
- **Integrates** document Q&A, live API data, and general LLM responses in a single unified interface
- Is **modular enough** to extend without rewriting the core system

### 2.3 The Opportunity

By building a multi-agent system with a central router, we can deliver:
- Higher accuracy through grounded, source-aware responses
- Real-time data integration without model fine-tuning
- A scalable foundation that can grow with additional tools and agents
- A professional, portfolio-grade system that mirrors production AI architectures at companies like Anthropic, OpenAI, and enterprise AI teams

---

## 3. Goals and Objectives

### 3.1 Primary Goals

| # | Goal | Description |
|---|---|---|
| G1 | Intelligent Query Routing | Classify and route every user query to the right agent automatically |
| G2 | Document Q&A via RAG | Allow users to upload PDFs and ask questions grounded in document content |
| G3 | Real-Time Data Access | Integrate external APIs (weather, stocks, etc.) for live data retrieval |
| G4 | Unified Conversational Interface | Provide a clean Streamlit UI with chat history and multi-modal input |
| G5 | Production-Ready Architecture | Modular codebase, clean separation of concerns, easy to extend |

### 3.2 Secondary Objectives

- Provide source citations when using RAG to increase response trustworthiness
- Handle failures gracefully — no raw error dumps to the user
- Enable zero-downtime addition of new agents or tools
- Demonstrate enterprise-grade AI system design in a portfolio context

### 3.3 Out of Scope (v1.0)

- User authentication / multi-user session management
- Persistent memory across sessions
- Fine-tuning of the underlying LLM
- Voice input / output
- Mobile-native application

---

## 4. User Personas

### Persona 1 — Priya, the Research Analyst

> **Background:** Works at a consulting firm. Spends hours reading PDFs and reports daily.  
> **Goal:** Ask questions about uploaded research documents without reading them end-to-end.  
> **Pain Point:** Current tools require manual ctrl+F or reading entire documents.  
> **How she uses the system:** Uploads a 50-page market report. Asks: *"What is the projected CAGR for the EV market in 2030?"* — gets a pinpointed answer with document context.

---

### Persona 2 — Arjun, the Independent Developer

> **Background:** Freelance developer learning about AI agent systems.  
> **Goal:** Understand how multi-agent routing works; wants to extend the system with new agents.  
> **Pain Point:** Most tutorials are toy examples — not representative of real architecture.  
> **How he uses the system:** Explores the codebase. Adds a new "SQL Query Agent" by following the modular agent interface.

---

### Persona 3 — Meera, the Business User

> **Background:** Non-technical user at a mid-size company.  
> **Goal:** Get quick answers — weather, stock prices, general questions — in one place.  
> **Pain Point:** Switching between different apps (Google, Yahoo Finance, ChatGPT) is inefficient.  
> **How she uses the system:** Types: *"What's the weather in Mumbai right now?"* or *"What's Apple's stock price?"* — gets instant, structured answers.

---

### Persona 4 — Rahul, the AI/ML Interview Candidate

> **Background:** CS graduate preparing for AI engineering interviews.  
> **Goal:** Build a portfolio project that demonstrates production-level AI system design.  
> **Pain Point:** Most GitHub projects are not interview-worthy — they lack architecture depth.  
> **How he uses the system:** Forks the repo. Studies the architecture. Presents it in interviews as a full-stack AI system demonstrating RAG, tool use, and agent orchestration.

---

## 5. Use Cases / User Stories

### Epic 1 — Query Routing

| ID | User Story | Priority |
|---|---|---|
| US-01 | As a user, I want the system to automatically detect my query type so I don't have to choose manually | P0 |
| US-02 | As a user, I want general questions answered directly without needing a document or API | P0 |
| US-03 | As a developer, I want the router's decision to be transparent and logged | P1 |

### Epic 2 — Document Q&A (RAG)

| ID | User Story | Priority |
|---|---|---|
| US-04 | As a user, I want to upload a PDF and ask questions about its content | P0 |
| US-05 | As a user, I want my answers to include the source passage or page reference | P1 |
| US-06 | As a user, I want to upload multiple documents and query across all of them | P2 |
| US-07 | As a user, I want a clear message if no relevant content is found in my document | P0 |

### Epic 3 — Real-Time Tool Integration

| ID | User Story | Priority |
|---|---|---|
| US-08 | As a user, I want to ask for current weather and get a real-time structured response | P0 |
| US-09 | As a user, I want to ask for a stock price and receive live market data | P1 |
| US-10 | As a user, I want API errors to be handled gracefully without breaking the chat | P0 |

### Epic 4 — UI & Experience

| ID | User Story | Priority |
|---|---|---|
| US-11 | As a user, I want a clean chat interface with message history | P0 |
| US-12 | As a user, I want to see which agent handled my query | P1 |
| US-13 | As a user, I want responses to be formatted clearly (not raw JSON) | P0 |
| US-14 | As a user, I want a loading indicator when the system is processing | P1 |

---

## 6. System Architecture Overview

### 6.1 High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        STREAMLIT UI                             │
│          [ Chat Interface + PDF Uploader + History ]            │
└───────────────────────────────┬─────────────────────────────────┘
                                │ User Query / Document
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                       ROUTER AGENT                              │
│         Classifies intent → General | RAG | Tool                │
│         (Prompt-based classification via LLM)                   │
└────────────┬──────────────────┬──────────────────┬─────────────┘
             │                  │                  │
             ▼                  ▼                  ▼
    ┌─────────────┐   ┌─────────────────┐  ┌─────────────────┐
    │  LLM AGENT  │   │    RAG AGENT    │  │   TOOL AGENT    │
    │             │   │                 │  │                 │
    │ - Groq API  │   │ - PDF Parsing   │  │ - Weather API   │
    │ - Together  │   │ - Chunking      │  │ - Stock API     │
    │   AI API    │   │ - Embeddings    │  │ - Extensible    │
    │             │   │ - FAISS Search  │  │   Tool Registry │
    └──────┬──────┘   └──────┬──────────┘  └───────┬─────────┘
           │                 │                      │
           └─────────────────┼──────────────────────┘
                             ▼
              ┌──────────────────────────┐
              │   RESPONSE FORMATTER     │
              │  Structures & renders    │
              │  output to Streamlit UI  │
              └──────────────────────────┘
```

### 6.2 Component Summary

| Component | Role | Technology |
|---|---|---|
| **Router Agent** | Classifies query intent and dispatches to the right agent | LLM prompt classification (Groq/Together AI) |
| **LLM Agent** | Handles general knowledge queries | Groq API / Together AI |
| **RAG Agent** | Document-based question answering | LangChain + FAISS + Sentence Transformers |
| **Tool Agent** | Real-time external API calls | Python `requests` + OpenWeatherMap, Alpha Vantage |
| **Response Formatter** | Unified output rendering | Python + Streamlit |
| **Vector Store** | Embedding storage and similarity search | FAISS (local) |
| **UI Layer** | User-facing chat interface | Streamlit |

---

## 7. Functional Requirements

### 7.1 Router Agent

| ID | Requirement |
|---|---|
| FR-R01 | The router SHALL classify every incoming query into one of three categories: `GENERAL`, `RAG`, or `TOOL` |
| FR-R02 | Classification SHALL be performed using a structured LLM prompt with explicit category definitions |
| FR-R03 | The router SHALL return both the classification label and a confidence rationale |
| FR-R04 | If classification is ambiguous, the router SHALL default to `GENERAL` |
| FR-R05 | The router SHALL log every routing decision with query text, classified category, and timestamp |

### 7.2 LLM Agent

| ID | Requirement |
|---|---|
| FR-L01 | The LLM Agent SHALL accept a plain-text query and return a natural language response |
| FR-L02 | The agent SHALL support at least one primary LLM provider (Groq or Together AI) |
| FR-L03 | The agent SHALL maintain the last N messages as conversation context (configurable N) |
| FR-L04 | The agent SHALL return a response within the configured timeout; otherwise surface a fallback message |

### 7.3 RAG Agent

| ID | Requirement |
|---|---|
| FR-RAG01 | The RAG Agent SHALL accept one or more PDF files and parse their text content |
| FR-RAG02 | Parsed text SHALL be split into overlapping chunks (configurable chunk size and overlap) |
| FR-RAG03 | Each chunk SHALL be embedded using a sentence transformer model and stored in a FAISS index |
| FR-RAG04 | On query, the agent SHALL retrieve the top-K most semantically similar chunks |
| FR-RAG05 | Retrieved chunks SHALL be passed as context to the LLM to generate a grounded answer |
| FR-RAG06 | If no relevant chunks are found (similarity below threshold), the agent SHALL return a "no relevant content found" message |
| FR-RAG07 | Source references (chunk index or page number) SHALL be included in the response where available |
| FR-RAG08 | The FAISS index SHALL persist in session memory; re-upload re-indexes |

### 7.4 Tool Agent

| ID | Requirement |
|---|---|
| FR-T01 | The Tool Agent SHALL maintain a registry of available tools with name, description, and handler function |
| FR-T02 | The agent SHALL identify the correct tool to invoke based on query content |
| FR-T03 | The Weather Tool SHALL call OpenWeatherMap (or equivalent) and return temperature, condition, and humidity |
| FR-T04 | The Stock Tool SHALL call Alpha Vantage (or equivalent) and return current price, change, and volume |
| FR-T05 | All API calls SHALL have a configurable timeout (default: 5 seconds) |
| FR-T06 | On API failure, the agent SHALL return a structured error message without crashing the application |
| FR-T07 | New tools SHALL be addable by registering a handler in the tool registry — no changes to router logic required |

### 7.5 Response Formatter Agent

| ID | Requirement |
|---|---|
| FR-F01 | All agent outputs SHALL be passed through the formatter before rendering |
| FR-F02 | The formatter SHALL label each response with its source agent (e.g., `[LLM Agent]`, `[RAG Agent]`) |
| FR-F03 | Tool responses SHALL be rendered as structured cards (not raw JSON) |
| FR-F04 | RAG responses SHALL display the answer followed by source references |
| FR-F05 | Error messages SHALL be user-friendly (no stack traces, no raw API errors) |

### 7.6 UI Requirements

| ID | Requirement |
|---|---|
| FR-UI01 | The UI SHALL provide a persistent chat interface with scrollable message history |
| FR-UI02 | The UI SHALL include a PDF upload widget in the sidebar |
| FR-UI03 | The UI SHALL display a spinner or status indicator during query processing |
| FR-UI04 | The UI SHALL display which agent handled each response |
| FR-UI05 | The UI SHALL allow clearing the chat history |
| FR-UI06 | The UI SHALL support markdown rendering in responses |

---

## 8. Non-Functional Requirements

### 8.1 Performance

| ID | Requirement |
|---|---|
| NFR-P01 | General LLM queries SHALL complete in under **3 seconds** (P95) under standard load |
| NFR-P02 | RAG retrieval + LLM generation SHALL complete in under **5 seconds** (P95) for documents under 20 pages |
| NFR-P03 | Tool API calls SHALL complete within the 5-second timeout or return a graceful fallback |
| NFR-P04 | PDF ingestion and indexing SHALL complete in under **10 seconds** for documents up to 50 pages |

### 8.2 Scalability

| ID | Requirement |
|---|---|
| NFR-S01 | The agent architecture SHALL be modular — new agents can be added without modifying existing agent code |
| NFR-S02 | The tool registry SHALL support dynamic tool registration at runtime |
| NFR-S03 | The FAISS index SHALL be replaceable with a cloud vector store (Pinecone, Weaviate) with minimal code changes |

### 8.3 Reliability

| ID | Requirement |
|---|---|
| NFR-R01 | The system SHALL handle all exceptions at the agent level and return a user-friendly fallback response |
| NFR-R02 | API timeouts and failures SHALL NOT crash the Streamlit application |
| NFR-R03 | If the LLM API is unavailable, the system SHALL surface a clear "Service Unavailable" message |

### 8.4 Maintainability

| ID | Requirement |
|---|---|
| NFR-M01 | Code SHALL follow a clean folder structure separating agents, services, utils, and config |
| NFR-M02 | All configuration values (API keys, timeouts, chunk sizes) SHALL be stored in a `.env` file or `config.py` — never hardcoded |
| NFR-M03 | Each agent SHALL have a corresponding unit test file |
| NFR-M04 | All public functions SHALL have docstrings |

### 8.5 Security

| ID | Requirement |
|---|---|
| NFR-SEC01 | API keys SHALL be loaded from environment variables; `.env` SHALL be in `.gitignore` |
| NFR-SEC02 | Uploaded documents SHALL be processed in-memory; no persistent storage to disk by default |
| NFR-SEC03 | No user data SHALL be logged in plaintext |

---

## 9. Technical Design (High-Level)

### 9.1 Project Folder Structure

```
adaptive-multi-agent-assistant/
│
├── app.py                          # Streamlit entry point
├── requirements.txt
├── .env.example
├── README.md
│
├── agents/
│   ├── __init__.py
│   ├── router_agent.py             # Query classification logic
│   ├── llm_agent.py                # General LLM response handler
│   ├── rag_agent.py                # RAG pipeline handler
│   ├── tool_agent.py               # Tool dispatch handler
│   └── formatter_agent.py          # Response formatting logic
│
├── services/
│   ├── __init__.py
│   ├── llm_service.py              # Groq / Together AI API wrapper
│   ├── embedding_service.py        # Sentence transformer wrapper
│   ├── vector_store.py             # FAISS index manager
│   └── tools/
│       ├── __init__.py
│       ├── tool_registry.py        # Tool registration + dispatch
│       ├── weather_tool.py         # OpenWeatherMap integration
│       └── news_tool.py            # News API integration
│
├── utils/
│   ├── __init__.py
│   ├── pdf_parser.py               # PDF text extraction
│   ├── text_chunker.py             # Text splitting logic
│   └── logger.py                   # Structured logging
│
├── config/
│   ├── __init__.py
│   └── settings.py                 # Centralized config (loads from .env)
│
└── tests/
    ├── test_router_agent.py
    ├── test_rag_agent.py
    ├── test_tool_agent.py
    └── test_llm_agent.py
```

### 9.2 Router Agent — Classification Logic

The router uses a structured LLM prompt to classify queries. Example prompt structure:

```
You are a query classifier for an AI assistant system.

Classify the following query into EXACTLY ONE category:
- GENERAL: General knowledge, definitions, explanations, or conversational questions
- RAG: Questions that require information from uploaded documents
- TOOL: Questions requiring real-time data (weather, stock prices, live information)

Query: "{user_query}"

Respond with only the category name: GENERAL, RAG, or TOOL
```

### 9.3 RAG Pipeline — Key Parameters

| Parameter | Default Value | Description |
|---|---|---|
| `CHUNK_SIZE` | 500 tokens | Size of each text chunk |
| `CHUNK_OVERLAP` | 50 tokens | Overlap between adjacent chunks |
| `TOP_K` | 4 | Number of chunks retrieved per query |
| `SIMILARITY_THRESHOLD` | 0.4 | Minimum cosine similarity to consider a chunk relevant |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | Sentence transformer model |

### 9.4 Tool Registry Design

Tools are registered as a dictionary of handlers:

```python
TOOL_REGISTRY = {
    "weather": {
        "description": "Get current weather for a city",
        "keywords": ["weather", "temperature", "forecast", "rain", "sunny"],
        "handler": get_weather
    },
    "stock": {
        "description": "Get current stock price for a ticker",
        "keywords": ["stock", "price", "shares", "market", "ticker"],
        "handler": get_stock_price
    }
}
```

### 9.5 Tech Stack Summary

| Layer | Technology | Rationale |
|---|---|---|
| UI | Streamlit | Rapid prototyping, native Python, easy deployment |
| LLM API | Groq (primary) / Together AI (fallback) | Fast inference, free tier available, OpenAI-compatible API |
| Embeddings | `sentence-transformers` (HuggingFace) | Free, local, high quality for semantic search |
| Vector Store | FAISS | Local, no infrastructure required, production-replaceable |
| PDF Parsing | `PyPDF2` / `pdfplumber` | Reliable text extraction from diverse PDF formats |
| Agent Orchestration | Native Python (LangGraph optional) | LangGraph can be layered in for complex workflows |
| External APIs | OpenWeatherMap, Alpha Vantage | Free tiers sufficient for v1.0 |
| Config Management | `python-dotenv` + `settings.py` | Clean separation of config from code |

---

## 10. Data Flow / Workflow

### 10.1 Standard Query Flow (General / Tool)

```
1. User enters query in Streamlit chat input
         │
2. app.py sends query to RouterAgent.classify(query)
         │
3. RouterAgent returns category: GENERAL | RAG | TOOL
         │
   ┌─────┴──────────────────────────┐
   │                                │
GENERAL                           TOOL
   │                                │
4. LLMAgent.generate(query)      ToolAgent.dispatch(query)
   │                                │
5. LLM API called (Groq)         Tool identified via keyword match
   │                                │
6. Raw LLM text returned         External API called (weather/stock)
   │                                │
   └─────────────────┬──────────────┘
                     │
7. FormatterAgent.format(response, agent_type)
                     │
8. Formatted response rendered in Streamlit chat window
```

### 10.2 RAG Query Flow (Document Upload)

```
[Document Upload Phase]
1. User uploads PDF via sidebar
2. PDFParser.extract_text(pdf_file)
3. TextChunker.split(text) → list of chunks
4. EmbeddingService.embed(chunks) → vector array
5. VectorStore.index(vectors) → FAISS index stored in session

[Query Phase]
6. User enters a document-based question
7. RouterAgent classifies as RAG
8. RAGAgent.retrieve(query)
   a. EmbeddingService.embed(query)
   b. VectorStore.search(query_vector, top_k=4)
   c. Returns top-K relevant chunks
9. RAGAgent.generate(query, retrieved_chunks)
   a. Chunks injected into LLM prompt as context
   b. LLM generates grounded answer
10. FormatterAgent formats with source references
11. Response rendered in UI
```

### 10.3 Edge Case Handling

| Scenario | Handling |
|---|---|
| Empty user input | Input validation in UI — show prompt to enter a query |
| No document uploaded for RAG query | RAG Agent returns: *"No document found. Please upload a PDF first."* |
| RAG retrieval below similarity threshold | Returns: *"No relevant content found in the uploaded document."* |
| External API timeout | Tool Agent catches `requests.Timeout`; returns: *"Unable to retrieve data. Please try again."* |
| External API returns error code | Returns structured error with API name and suggestion |
| LLM API rate limit / failure | LLM Service catches exception; returns: *"AI service is currently unavailable."* |
| Ambiguous query (hard to classify) | Router defaults to GENERAL; LLM responds with best effort |

---

## 11. Risks and Mitigations

| # | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R01 | LLM misclassifies query category | Medium | High | Robust prompt engineering + fallback to GENERAL; log classification decisions for monitoring |
| R02 | RAG retrieves irrelevant chunks (hallucination risk) | Medium | High | Similarity threshold filter; include source citations so users can verify |
| R03 | External API rate limits or downtime | Medium | Medium | Implement retry logic with exponential backoff; cache recent API responses where permitted |
| R04 | Large PDF causes slow indexing or OOM | Low | Medium | Limit PDF size (default 20MB); process in streaming chunks; warn user on large uploads |
| R05 | FAISS index becomes stale after re-upload | Low | Low | Clear and rebuild FAISS index on every new upload; keep it session-scoped |
| R06 | API keys exposed in code | Low | Critical | `.env` file + `.gitignore`; `settings.py` loads via `os.environ`; documented in README |
| R07 | LLM generates harmful or inaccurate responses | Low | High | System prompt instructs model to refuse harmful requests; caveat uncertain answers |
| R08 | Streamlit session state inconsistency | Medium | Medium | Centralize all session state management; reset state on document re-upload |

---

## 12. Future Enhancements

### Phase 2 — Short-Term (Next 3 Months)

| Enhancement | Description |
|---|---|
| **Memory Agent** | Maintain persistent conversation history across sessions using Redis or SQLite |
| **Multi-document RAG** | Support uploading and querying across multiple PDFs simultaneously |
| **Agent Trace View** | UI panel showing the reasoning chain: query → router decision → agent execution |
| **LangGraph Integration** | Replace manual agent dispatch with LangGraph for stateful, conditional multi-step workflows |

### Phase 3 — Medium-Term (3–6 Months)

| Enhancement | Description |
|---|---|
| **SQL Agent** | Accept database schema + NL query → generate and execute SQL → return results |
| **Web Search Tool** | Integrate Serper or Tavily API to search the live web as a tool option |
| **Streaming Responses** | Stream LLM tokens to UI for faster perceived response time |
| **Authentication** | User login, per-user document stores, and conversation history |

### Phase 4 — Long-Term Vision

| Enhancement | Description |
|---|---|
| **Auto-Tool Discovery** | LLM selects from tool registry automatically using OpenAI function-calling style |
| **Feedback Loop** | Users rate responses; poor ratings trigger re-routing or fallback chain |
| **Cloud Vector Store** | Replace FAISS with Pinecone or Weaviate for multi-user, persistent RAG |
| **Evaluation Framework** | Automated RAG quality scoring using RAGAS or custom metrics |
| **Voice Interface** | Whisper API for speech input; TTS for spoken responses |

---

## 13. Success Metrics

### 13.1 Technical Performance Metrics

| Metric | Target (v1.0) |
|---|---|
| General query response time (P95) | < 3 seconds |
| RAG query response time (P95) | < 5 seconds |
| Tool query response time (P95) | < 4 seconds |
| PDF ingestion time (50 pages) | < 10 seconds |
| Router classification accuracy | ≥ 90% on test query set |
| RAG answer relevance (human eval) | ≥ 80% relevant responses |

### 13.2 Reliability Metrics

| Metric | Target |
|---|---|
| API failure graceful handling | 100% of failures return user-friendly messages |
| Application crash rate | 0 crashes during normal operation |
| Empty input handling | 100% caught and prompted |

### 13.3 User Experience Metrics

| Metric | Target |
|---|---|
| Time to first response | < 1 second (UI responsiveness) |
| Source citations present in RAG responses | ≥ 90% of RAG responses |
| Agent label visible in every response | 100% |

### 13.4 Portfolio / Project Quality Metrics

| Metric | Target |
|---|---|
| Code coverage (unit tests) | ≥ 70% |
| Modules with docstrings | 100% |
| README completeness | Full setup, architecture overview, and demo instructions |
| `.env.example` provided | ✅ |
| No hardcoded secrets | 0 violations |

---

## Appendix A — Environment Variables Reference

```env
# LLM Configuration
GROQ_API_KEY=your_groq_api_key
TOGETHER_API_KEY=your_together_api_key
LLM_PROVIDER=groq                  # groq | together

# External APIs
OPENWEATHER_API_KEY=your_openweather_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key

# RAG Configuration
CHUNK_SIZE=500
CHUNK_OVERLAP=50
TOP_K_RESULTS=4
SIMILARITY_THRESHOLD=0.4
EMBEDDING_MODEL=all-MiniLM-L6-v2

# General
MAX_PDF_SIZE_MB=20
LLM_TIMEOUT_SECONDS=10
TOOL_TIMEOUT_SECONDS=5
```

---

## Appendix B — API Integration Summary

| API | Provider | Use Case | Free Tier |
|---|---|---|---|
| LLM Inference | Groq | General + RAG generation | Yes — generous free tier |
| Embeddings | HuggingFace (local) | Document vectorization | Free (local model) |
| Weather | OpenWeatherMap | Real-time weather data | Yes — 1,000 calls/day |
| Stock Prices | Alpha Vantage | Real-time stock data | Yes — 25 calls/day |
| FAISS | Meta (local library) | Vector similarity search | Free (local) |

---

*This PRD is intended as a living document. As the project evolves through development and testing, requirements, metrics, and architecture details should be updated to reflect the current state of the system.*

---

**Document End — Adaptive Multi-Agent AI Assistant PRD v1.0**