# Agentic Multimodal PDF Chatbot

A professional-grade chatbot that leverages **Gemini 2.5 Flash** and **LangGraph** to provide agentic, multimodal reasoning over PDF documents. It doesn't just read text—it understands tables, diagrams, and the connections between them.

## 🚀 Features
- **Multimodal Understanding**: Analyzes images, charts, and tables natively using Gemini's latest 2.5 Flash model.
- **Agentic Reasoning**: Controlled by LangGraph to ensure accurate, context-aware responses.
- **Premium UI**: Modern glassmorphic React interface with smooth animations and drag-and-drop support.
- **FastAPI Backend**: High-performance backend with seamless integration with the Google GenAI SDK.

## 🛠️ Tech Stack
- **Frontend**: React, Vite, Framer Motion, Lucide React, Axios.
- **Backend**: Python, FastAPI, LangGraph, Google GenAI SDK.
- **AI Model**: Gemini 2.5 Flash.

## 📂 Project Structure
```text
.
├── server/             # FastAPI backend
│   ├── main.py         # App entrance & LangGraph flow
│   ├── processor.py    # Gemini Multimodal service
│   ├── venv/           # Virtual environment
│   └── .env            # Environment variables (API Key)
├── frontend/           # React frontend
│   ├── src/            # Components and styles
│   └── package.json    # Frontend dependencies
├── run.ps1             # Convenience script to start both servers
└── .gitignore          # Git exclusion rules
```

## 🚥 Getting Started

### Prerequisites
- Node.js & npm
- Python 3.10+
- A Google Gemini API Key

### Setup
1.  **Clone the repository**:
    ```bash
    git clone <your-repo-url>
    cd agentic-rag-qa-bot
    ```

2.  **Configure Backend**:
    - Navigate to `server/`.
    - Create a `.env` file (if not present) and add:
      ```text
      GOOGLE_API_KEY=your_api_key_here
      ```
    - The virtual environment and dependencies should already be set up if you followed the installation steps.

### Running the App
The easiest way is to use the provided PowerShell script in the root directory:
```powershell
.\run.ps1
```

Alternatively, run manually:
- **Backend**: `cd server; .\venv\Scripts\activate; python main.py`
- **Frontend**: `cd frontend; npm run dev`

## 💬 Example Queries
- "Explain the flowchart on page 3."
- "What is the correlation between Figure 1 and Table 2?"
- "Summarize the key findings from the charts on page 10."

## 📄 License
MIT
