# Quick Start Guide

## ⚡ 5-Minute Setup

### Step 1: Install Dependencies
```bash
python setup.py
```

This will:
- ✅ Check Python version (3.9+)
- ✅ Create `.env` from `.env.example`
- ✅ Create necessary directories
- ✅ Install all packages
- ✅ Verify imports

### Step 2: Add Google Gemini API Key

Edit `.env`:
```bash
# Linux/Mac
nano .env

# Windows PowerShell
notepad .env
```

Find and update:
```env
GEMINI_API_KEY=your_actual_key_from_google_ai_studio
```

**Get API key:** https://aistudio.google.com/app/apikey

### Step 3: Run the Application
```bash
python -m phase7_api.main
```

You'll see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 4: Test the API

**Option A: Using Swagger UI (Browser)**
```
http://localhost:8000/docs
```

**Option B: Using curl**
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"question":"What are the admission requirements?"}'
```

**Option C: Using Python**
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/chat",
    json={"question": "What programs does St. Aloysius offer?"}
)

print(response.json())
```

---

## 📁 Project Structure at a Glance

```
aloysius-chatbot/
├── config/
│   ├── config.py              ← Configuration management
│   └── logging_setup.py       ← Logging setup
├── phase3_processing/
│   └── advanced_chunk.py      ← NEW: Smart chunking
├── phase6_rag/
│   └── gemini_llm.py          ← NEW: Gemini integration
├── phase7_api/
│   ├── main.py                ← FastAPI app
│   ├── api.py                 ← API routes
│   └── schemas.py             ← Data models
├── .env.example               ← Configuration template
├── .gitignore                 ← Git security
├── setup.py                   ← Quick setup script
├── README.md                  ← Full documentation
└── CONFIG_GUIDE.md            ← Configuration details
```

---

## 🔑 What's New

### Professional Setup
- ✅ **Environment variables** (`.env`) for secure configuration
- ✅ **Config module** (`config/config.py`) for centralized management
- ✅ **Logging system** with structured formatting
- ✅ **Google Gemini API** integration (replaces Ollama)

### Advanced Chunking
- ✅ **Semantic chunking** based on document structure
- ✅ **Navigation filtering** removes menu/UI content
- ✅ **Duplicate removal** for cleaner knowledge base
- ✅ **Quality scoring** for chunk validation
- ✅ **Metadata enrichment** with section/URL info

### Better API
- ✅ **Improved error handling** with proper HTTP status codes
- ✅ **Input validation** with Pydantic schemas
- ✅ **Confidence scores** for response reliability
- ✅ **Source attribution** for transparency
- ✅ **Swagger docs** at `/docs`

---

## 🚀 Common Commands

### Initialize Data Pipeline
```bash
# Extract URLs
python -m phase1_sitemap.run_phase1

# Crawl pages
python -m phase2_extraction.run_phase2

# Process & chunk with new semantic strategy
python -m phase3_processing.run_phase3

# Create embeddings & vector DB
python -m phase4_vectorstore.run_phase4

# Run API server
python -m phase7_api.main
```

### Check Health
```bash
curl http://localhost:8000/api/v1/health
```

### View API Documentation
```
http://localhost:8000/docs
```

### View Logs
```bash
tail -f logs/app.log
```

---

## ⚙️ Configuration Quick Reference

### Best for Accuracy
```env
TOP_K_RESULTS=8
SIMILARITY_THRESHOLD=0.5
CHUNK_SIZE=600
```

### Best for Speed
```env
TOP_K_RESULTS=3
SIMILARITY_THRESHOLD=0.7
CHUNK_SIZE=400
```

### Best for Balanced
```env
TOP_K_RESULTS=5
SIMILARITY_THRESHOLD=0.6
CHUNK_SIZE=500
```

For full config options, see [CONFIG_GUIDE.md](CONFIG_GUIDE.md)

---

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named 'google'"
```bash
pip install google-generativeai
```

### "GEMINI_API_KEY not configured"
- Check `.env` file exists in root directory
- Verify `GEMINI_API_KEY=` is set (not the placeholder text)
- Restart the application

### Port 8000 already in use
```bash
# Change in .env
PORT=8001

# Then restart
python -m phase7_api.main
```

### Vector DB not found
```bash
# Regenerate embeddings
python -m phase4_vectorstore.run_phase4
```

---

## 📚 Next Steps

1. **Add your data**: Run phases 1-4 to process the website
2. **Customize chunking**: Edit `CHUNK_SIZE` and `TOP_K_RESULTS` in `.env`
3. **Integrate with frontend**: Connect to your UI using the REST API
4. **Monitor performance**: Check `logs/app.log` for insights
5. **Deploy**: Use production environment settings

---

## 🎯 API Response Format

Every successful response includes:
```json
{
  "answer": "Detailed answer to the question",
  "sources": ["https://example.com/page1"],
  "confidence": 0.85
}
```

- **answer**: AI-generated response based on context
- **sources**: URLs where information came from
- **confidence**: How confident the system is (0.0 to 1.0)

---

**Questions?** Check [README.md](README.md) or [CONFIG_GUIDE.md](CONFIG_GUIDE.md)
