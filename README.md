# St. Aloysius University AI Chatbot

A professional-grade RAG (Retrieval Augmented Generation) powered AI assistant for St. Aloysius University's knowledge base. Built with FastAPI, Google Gemini API, and semantic chunking.

## 🎯 Features

- **Advanced RAG Pipeline**: Multi-phase semantic retrieval system
- **Google Gemini Integration**: State-of-the-art LLM for accurate responses
- **Semantic Chunking**: Intelligent document processing that preserves context
- **Vector Database**: Efficient similarity-based retrieval with ChromaDB
- **Professional Configuration**: Environment-based setup with security best practices
- **Comprehensive Logging**: Structured logging for debugging and monitoring
- **Production-Ready API**: FastAPI with proper error handling and validation

## 🏗️ Architecture

```
Phase 1: Sitemap Extraction
    ↓
Phase 2: Web Crawling → Raw Markdown
    ↓
Phase 3: Advanced Processing & Semantic Chunking
    ↓
Phase 4: Embedding & Vector Storage
    ↓
Phase 5: Change Detection & Updates
    ↓
Phase 6: RAG Retrieval
    ↓
Phase 7: FastAPI Server & Responses
```

## 📋 Prerequisites

- Python 3.9+
- Google Gemini API Key (paid version)
- Git

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd aloysius-chatbot
```

### 2. Create Virtual Environment

```bash
# On Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# On Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory (copy from `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
# Required: Your Google Gemini API Key
GEMINI_API_KEY=your_actual_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash

# Optional: Customize other settings as needed
ENVIRONMENT=development
```

**⚠️ NEVER commit `.env` to version control. It's in `.gitignore`.**

## 🔧 Configuration

All configuration is managed through `config/config.py` and environment variables.

### Key Configuration Options

```env
# LLM Configuration
GEMINI_API_KEY=your_api_key
GEMINI_MODEL=gemini-2.0-flash

# Chunking Strategy
CHUNK_SIZE=500
CHUNK_OVERLAP=100
MIN_CHUNK_SIZE=200
MAX_CHUNK_SIZE=1000
FILTER_NAVIGATION=true
REMOVE_DUPLICATES=true

# RAG Settings
TOP_K_RESULTS=5
SIMILARITY_THRESHOLD=0.6

# Server
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=development
```

## 📝 Usage

### Start the API Server

```bash
python -m phase7_api.main
```

The API will be available at `http://localhost:8000`

### API Endpoints

#### 1. Health Check
```bash
GET /api/v1/health
```

#### 2. Chat Endpoint
```bash
POST /api/v1/chat
Content-Type: application/json

{
  "question": "What are the admission requirements for BTech?"
}
```

**Response:**
```json
{
  "answer": "St. Aloysius offers multiple BTech programs...",
  "sources": ["https://staloysius.edu.in/admissions"],
  "confidence": 0.85
}
```

#### 3. API Info
```bash
GET /api/v1/info
```

#### 4. Interactive Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🔄 Data Pipeline

### Phase 1: Sitemap Extraction
```bash
python -m phase1_sitemap.run_phase1
```

### Phase 2: Web Crawling
```bash
python -m phase2_extraction.run_phase2
```

### Phase 3: Advanced Processing & Chunking
```bash
python -m phase3_processing.run_phase3
```

### Phase 4: Vector Embedding & Storage
```bash
python -m phase4_vectorstore.run_phase4
```

### Phase 5: Change Detection
```bash
python -m phase5_updates.run_phase5
```

## 🎓 Chunking Strategy

The advanced chunking system improves retrieval quality:

1. **Semantic Splitting**: Chunks based on document structure (headings, paragraphs)
2. **Navigation Filtering**: Removes UI elements and menu items
3. **Duplicate Removal**: Eliminates redundant content
4. **Quality Scoring**: Filters low-quality chunks
5. **Metadata Enrichment**: Adds URL, section, and timestamp info

## 🔐 Security Best Practices

- ✅ API keys stored in `.env` (never in code)
- ✅ `.env` is in `.gitignore`
- ✅ `.env.example` shows structure without sensitive data
- ✅ Environment-based configuration for production/development
- ✅ Input validation on all API endpoints
- ✅ Structured logging for audit trails

## 📊 Logging

Logs are stored in `logs/app.log` with:
- Timestamp
- Log level
- Module name
- Function name
- Line number
- Full message

### Configure Logging Level

```env
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE=logs/app.log
```

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=.
```

## 📦 Project Structure

```
aloysius-chatbot/
├── config/
│   ├── config.py           # Configuration management
│   ├── logging_setup.py    # Logging configuration
│   └── __init__.py
│
├── phase1_sitemap/         # Sitemap extraction
├── phase2_extraction/      # Web crawling
├── phase3_processing/      # Text processing & advanced chunking
│   ├── advanced_chunk.py   # NEW: Semantic chunking
│   └── ...
├── phase4_vectorstore/     # Vector embedding
├── phase5_updates/         # Change detection
├── phase6_rag/
│   ├── gemini_llm.py       # NEW: Gemini API integration
│   ├── retrieve_context.py
│   └── embed_query.py
├── phase7_api/
│   ├── main.py             # FastAPI application
│   ├── api.py              # API routes
│   ├── schemas.py          # Pydantic models
│   └── rag_service.py
│
├── data/
│   ├── url_registry.json
│   ├── state_snapshot.json
│   ├── raw_markdown/
│   ├── processed_chunks/
│   └── vector_db/
│
├── frontend/               # Web UI (optional)
├── logs/                   # Application logs
├── .env.example            # Configuration template
├── .gitignore             # Git ignore rules
├── requirements.txt       # Python dependencies
└── README.md
```

## 🐛 Troubleshooting

### "GEMINI_API_KEY not configured"
- Check `.env` file exists and is in the root directory
- Ensure `GEMINI_API_KEY=your_key` is set (not "your_google_gemini_api_key_here")
- Restart the application

### Vector DB Not Found
- Run `python -m phase4_vectorstore.run_phase4` to initialize

### Low Confidence Scores
- Ensure chunks were generated properly: `python -m phase3_processing.run_phase3`
- Check chunk quality: Review `logs/app.log`
- Verify content is semantically similar to queries

## 📄 License

All rights reserved. St. Aloysius University.

## 🤝 Contributing

Contact the development team for contribution guidelines.

## 📞 Support

For issues or questions:
- Check logs in `logs/app.log`
- Review API documentation at `/docs`
- Contact development team

---

**Version**: 1.0.0  
**Last Updated**: December 2025
