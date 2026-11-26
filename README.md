# IntelliQuest – AI-Powered Knowledge and Research Automation Platform

**IntelliQuest** is an advanced AI-powered knowledge and research automation platform that combines Retrieval-Augmented Generation (RAG), multi-agent systems, and multimodal AI to provide intelligent document-based question answering and automated research assistance.

The platform allows users to upload PDF documents, ask questions based on document content, analyze images, evaluate AI-generated responses, and perform research using intelligent AI agents.

## 🚀 Key Features

- **Document Management:** Upload, index, view, and delete PDF documents.
- **Retrieval-Augmented Generation (RAG):** Retrieve relevant information from uploaded documents and generate context-aware answers.
- **LangGraph Integration:** Manage the RAG workflow using a structured graph-based architecture.
- **Multi-Agent Research:** Use CrewAI agents for research, analysis, and knowledge assistance.
- **MCP Integration:** Expose document search and question-answering capabilities through Model Context Protocol tools.
- **Multimodal Image Understanding:** Upload images and ask questions about their visual content.
- **AI Response Evaluation:** Evaluate answer relevance, context relevance, answer-context alignment, retrieval quality, and faithfulness.
- **Interactive Dashboard:** Access all major features through a Streamlit-based interface.
- **Persistent Storage:** Store document embeddings using ChromaDB and document metadata using SQLite.

## 🏗️ System Architecture

```text
                 IntelliQuest
                      |
             Streamlit Frontend
                      |
          Application and Workflow Layer
                      |
       +--------------+--------------+
       |              |              |
      RAG           LangGraph       CrewAI
       |              |              |
   Retrieval       Workflow      AI Agents
       |              |              |
       +--------------+--------------+
                      |
               Gemini LLM
                      |
       +--------------+--------------+
       |              |              |
    ChromaDB       SQLite        Image QA
   Vector Store   Metadata       Gemini Vision
       |
   Embeddings
       |
 Sentence Transformers
```

## 🛠️ Technologies Used

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| Large Language Model | Google Gemini |
| AI Framework | LangChain |
| Workflow Orchestration | LangGraph |
| Multi-Agent Framework | CrewAI |
| Retrieval System | RAG |
| Vector Database | ChromaDB |
| Embeddings | Sentence Transformers |
| Database | SQLite, SQLAlchemy |
| Image Understanding | Gemini Vision |
| Document Processing | PyPDF |
| Evaluation | Semantic Similarity, Faithfulness Evaluation |
| Model Libraries | Transformers, PyTorch |
| Tool Integration | FastMCP |

## 📁 Project Structure

```text
IntelliQuest_AI/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .env
│
├── frontend/
│   └── app.py
│
├── backend/
│   ├── agents/
│   │   └── crew_workflow.py
│   │
│   ├── database/
│   │   ├── db.py
│   │   └── models.py
│   │
│   ├── document_processing/
│   │   └── pdf_loader.py
│   │
│   ├── evaluation/
│   │   ├── evaluation_metrics.py
│   │   └── response_evaluator.py
│   │
│   ├── mcp_server/
│   │   └── server.py
│   │
│   ├── models/
│   │   └── model_router.py
│   │
│   ├── multimodal/
│   │   └── image_qa.py
│   │
│   ├── orchestration/
│   │   └── rag_graph.py
│   │
│   └── rag/
│       ├── answer_generator.py
│       ├── embeddings.py
│       ├── ingestion.py
│       ├── text_splitter.py
│       └── vector_store.py
│
├── storage/
│   ├── uploads/
│   ├── reports/
│   ├── chroma_db/
│   └── intelliquest.db
│
└── tests/
    ├── test_model_router.py
    ├── test_rag.py
    ├── test_langgraph.py
    ├── test_crewai.py
    ├── test_mcp_server.py
    ├── test_image_qa.py
    ├── test_database.py
    ├── test_document_metadata.py
    ├── test_evaluation.py
    ├── test_retrieval_quality.py
    └── test_answer_quality.py
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone <your-github-repository-url>
cd IntelliQuest_AI
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory.

```env
GOOGLE_API_KEY=your_google_api_key
MODEL_PROVIDER=gemini
GEMINI_MODEL=gemini-3.5-flash-lite
```

Replace the placeholder with your own Google API key. Never upload your actual API key to GitHub.

### 5. Run the Application

```bash
python -m streamlit run frontend/app.py
```

Open the local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

## 🧪 Testing

The project includes test modules covering the major components.

Run individual tests using:

```bash
python -m tests.test_model_router
python -m tests.test_rag
python -m tests.test_langgraph
python -m tests.test_crewai
python -m tests.test_mcp_server
python -m tests.test_image_qa
python -m tests.test_database
python -m tests.test_document_metadata
python -m tests.test_evaluation
python -m tests.test_retrieval_quality
python -m tests.test_answer_quality
```

The implemented test modules have been executed successfully in the development environment.

## 🔌 MCP Server

IntelliQuest provides MCP tools for external AI applications and compatible MCP clients.

Available tools:

- `search_documents(question, top_k)` – Searches indexed documents for relevant information.
- `ask_intelliquest(question)` – Generates an answer using the document question-answering workflow.

Run the MCP Inspector during development:

```bash
fastmcp dev inspector backend/mcp_server/server.py
```

## 💡 Applications

- Academic document analysis
- Intelligent knowledge management
- Research automation
- Document-based question answering
- AI-assisted learning
- Multimodal information extraction

## 🔮 Future Enhancements

- Support for additional document formats.
- Advanced conversational memory.
- More specialized AI agents.
- Cloud deployment and scalable storage.
- Enhanced evaluation and benchmarking.
- Additional multimodal capabilities.

## 👨‍💻 Project Information

**Project Name:** IntelliQuest

**Project Type:** AI / Machine Learning / Generative AI

**Core Concepts:** Retrieval-Augmented Generation, Multi-Agent Systems, LangGraph, MCP, and Multimodal AI.

---

*IntelliQuest – Transforming documents and information into intelligent knowledge.*
