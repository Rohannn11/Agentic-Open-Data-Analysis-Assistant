# Agentic Open Data Analysis Assistant

A production-ready, Dockerized AI application that autonomously plans, fetches, analyzes, and visualizes global economic data. Built with a microservices architecture, it leverages **Google Gemini 2.5 Flash** as the cognitive engine to orchestrate data retrieval from the **World Bank** and **OECD** APIs, delivering professional-grade insights and interactive dashboards.

---

## 🚀 Key Features

* **Autonomous Agent Architecture:** A multi-agent system (Planner, Fetcher, Analyst, Narrator) that breaks down natural language queries into executable data pipelines.
* **Multi-Source Intelligence:** Seamless integration with **World Bank** (Global Development Data) and **OECD** (Advanced Economy Data), dynamically selected based on query context.
* **Context-Aware Analysis:**
    * **Single Country Deep-Dive:** Detailed reports on trends, volatility, and policy implications.
    * **Multi-Country Comparison:** Side-by-side performance benchmarking.
    * **Smart Context:** Automatically fetches related indicators (e.g., adds "Inflation" context when querying "GDP").
* **Advanced Visualization:**
    * **Dual-Chart Dashboard:** Interactive Trend Lines (Time-Series) and Comparative Bar Charts (Averages).
    * **Smart Metrics:** Automatically distinguishes between "Percentage Growth" and "Point Change" for accurate economic reporting.
* **Production-Ready:** Fully containerized with **Docker** & **Docker Compose**, featuring structured JSON logging and Nginx static serving.

---

## 🛠️ Technology Stack

### **Backend (The Brain)**
* **Language:** Python 3.11
* **Framework:** FastAPI (High-performance Async API)
* **AI Model:** Google Gemini 2.5 Flash (via `google-genai` SDK)
* **Data Processing:** Pandas, NumPy
* **Observability:** Custom JSON Structured Logging

### **Frontend (The Face)**
* **Server:** Nginx (Alpine Linux)
* **Core:** Vanilla JavaScript (ES6+), HTML5, CSS3
* **Visualization:** Chart.js (Responsive, Interactive)
* **Formatting:** Marked.js (Markdown rendering for AI narratives)

### **Infrastructure (The Engine)**
* **Containerization:** Docker & Docker Compose
* **Gateway:** Uvicorn (ASGI Server)

---

## 🏗️ Architecture

The system follows a linear **Orchestrator Pattern**:

1.  **Gateway (FastAPI):** Receives the user query (e.g., *"Compare GDP of India and USA"*).
2.  **Planner Agent (Gemini):** Analyzes the intent.
    * Extracts Entities: `["IND", "USA"]`
    * Selects Indicators: `GDP Growth` + `Inflation` (Context)
    * Selects Source: `WORLDBANK`
3.  **Fetcher Agent:** Iterates through the plan, routing requests to the specific **API Adapter** (WorldBank or OECD) to retrieve raw time-series data.
4.  **Analyst Agent:**
    * Cleans and aggregates data.
    * Computes Statistics (Min, Max, Growth, Trend).
    * Formats data structures for `Chart.js`.
5.  **Narrator Agent (Gemini):** Consumes the statistics and source metadata to generate a professional economic report (Comparative vs. Deep-Dive).
6.  **Frontend:** Renders the JSON response into a dashboard with charts and markdown text.

---

## 📂 Project Structure

```bash
.
├── docker-compose.yml       # Orchestration config
├── Dockerfile               # Backend container definition
├── requirements.txt         # Python dependencies
├── .env                     # API Keys (GitIgnored)
│
├── gateway/                 # API Entry Point
│   └── main.py              # FastAPI App & Routes
│
├── orchestrator/            # The Agentic Core
│   ├── main.py              # Pipeline Logic
│   ├── logger.py            # Structured Logging
│   ├── schemas.py           # Pydantic Data Models
│   └── agents/
│       ├── planner.py       # Intent Recognition
│       ├── fetcher.py       # Data Retrieval Loop
│       ├── analyst.py       # Statistics & Chart Prep
│       └── narrator.py      # Insight Generation
│
├── data/                    # Data Layer
│   ├── canonical.py         # Standard Data format
│   └── adapters/            # API Connectors
│       ├── worldbank_adapter.py
│       └── oecd_adapter.py
│
└── frontend/                # Web Dashboard
    ├── Dockerfile           # Nginx container definition
    ├── index.html           # UI Layout
    ├── styles.css           # Dark Mode Styling
    └── app.js               # Client-side Logic

## Prerequisites

- Docker Desktop installed and running  
- A Google Gemini API Key  

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/agentic-data-analyst.git
cd agentic-data-analyst
```

### 2. Configure Environment

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. Build & Run

Launch the entire stack with one command:

```bash
docker-compose up --build
```

---

## Access the Application

- **Dashboard:** http://localhost:3000  
- **API Docs:** http://localhost:8000/docs  

---

## 🧪 Example Queries

Try these in the dashboard:

- **Single Country:**  
  `"Unemployment in France"`

- **Comparison:**  
  `"Compare GDP growth of India and China"`

- **Complex Query:**  
  `"How is the inflation situation in USA vs UK?"`

---

## 🔮 Future Roadmap

- **Caching (Redis):** Reduce API latency and quota usage  
- **Forecasting (Prophet):** Predictive analytics for future trends (2025+)  
- **Chat Memory:** Multi-turn conversations (e.g., "Now add Germany to the chart")  
- **PDF Reports:** Downloadable executive summaries  

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
