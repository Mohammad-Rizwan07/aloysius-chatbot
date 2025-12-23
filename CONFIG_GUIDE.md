# Configuration Guide - Aloysius Chatbot

## Overview

This guide explains all configuration options for the Aloysius Chatbot. The system uses environment variables for flexible configuration across different environments (development, staging, production).

## Environment Setup

### 1. Create `.env` File

Copy the template:
```bash
cp .env.example .env
```

### 2. Configure Required Variables

#### Google Gemini API (REQUIRED)

```env
GEMINI_API_KEY=your_actual_api_key_here
GEMINI_MODEL=gemini-2.0-flash
```

**How to get API key:**
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new project or select existing
3. Generate API key
4. Paste in `.env`

### 3. Environment Selection

```env
ENVIRONMENT=development  # or production, staging
```

**Impact:**
- `development`: Reload enabled, detailed logging, CORS open
- `production`: Optimized, strict CORS, secure defaults

## Configuration Sections

### 1. Vector Database Configuration

```env
VECTOR_DB_PATH=data/vector_db
COLLECTION_NAME=aloysius_knowledge
```

**Options:**
- `VECTOR_DB_PATH`: Directory where vector embeddings are stored
- `COLLECTION_NAME`: Name of the ChromaDB collection

### 2. Chunking Strategy

```env
CHUNK_SIZE=500
CHUNK_OVERLAP=100
MIN_CHUNK_SIZE=200
MAX_CHUNK_SIZE=1000
```

**Tuning Guide:**
| Parameter | Value | Effect |
|-----------|-------|--------|
| `CHUNK_SIZE` | Smaller (300-400) | More granular retrieval, more chunks |
| | Larger (700-1000) | Broader context, fewer chunks |
| `CHUNK_OVERLAP` | Smaller (50) | Faster processing, less redundancy |
| | Larger (150) | Better continuity, more overlap |
| `MIN_CHUNK_SIZE` | Smaller (100) | Include short content |
| | Larger (300) | Only substantial content |

**Recommendation for FAQ-based content:**
```env
CHUNK_SIZE=600
CHUNK_OVERLAP=100
MIN_CHUNK_SIZE=150
```

### 3. Content Filtering

```env
FILTER_NAVIGATION=true
REMOVE_DUPLICATES=true
MIN_CONTENT_LENGTH=100
```

**Options:**
- `FILTER_NAVIGATION`: Remove menu items, navigation links
- `REMOVE_DUPLICATES`: Eliminate repeated content
- `MIN_CONTENT_LENGTH`: Minimum characters for a valid chunk

### 4. RAG Pipeline Configuration

```env
TOP_K_RESULTS=5
SIMILARITY_THRESHOLD=0.6
USE_RERANKING=false
```

**Tuning:**
| Parameter | Value | Effect |
|-----------|-------|--------|
| `TOP_K_RESULTS` | 3 | Faster, focused results |
| | 5 | Balanced (default) |
| | 10 | More context, slower |
| `SIMILARITY_THRESHOLD` | 0.5 | Broader matching |
| | 0.6 | Balanced (default) |
| | 0.8 | Stricter matching |

### 5. Logging Configuration

```env
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
LOG_FORMAT=json
```

**Log Levels:**
- `DEBUG`: Verbose, all operations
- `INFO`: General information (recommended)
- `WARNING`: Only warnings and errors
- `ERROR`: Only errors

**For Development:**
```env
LOG_LEVEL=DEBUG
```

**For Production:**
```env
LOG_LEVEL=INFO
```

### 6. Server Configuration

```env
HOST=0.0.0.0
PORT=8000
RELOAD=true
```

**Development:**
```env
HOST=0.0.0.0
PORT=8000
RELOAD=true
```

**Production:**
```env
HOST=127.0.0.1
PORT=8000
RELOAD=false
```

### 7. Application Information

```env
APP_NAME=St. Aloysius University AI Assistant
APP_VERSION=1.0.0
```

## Configuration Profiles

### Development Profile

```env
ENVIRONMENT=development
GEMINI_API_KEY=your_dev_key

CHUNK_SIZE=500
CHUNK_OVERLAP=100
TOP_K_RESULTS=5

LOG_LEVEL=DEBUG
RELOAD=true
HOST=0.0.0.0
```

### Production Profile

```env
ENVIRONMENT=production
GEMINI_API_KEY=your_prod_key

CHUNK_SIZE=600
CHUNK_OVERLAP=120
TOP_K_RESULTS=5

LOG_LEVEL=INFO
RELOAD=false
HOST=127.0.0.1
```

### Testing Profile

```env
ENVIRONMENT=staging
CHUNK_SIZE=400
CHUNK_OVERLAP=80
LOG_LEVEL=DEBUG
```

## Advanced Configuration

### Custom Chunk Processing

For specialized content types, adjust:

**Academic documents:**
```env
CHUNK_SIZE=700
MIN_CHUNK_SIZE=300
FILTER_NAVIGATION=true
REMOVE_DUPLICATES=true
```

**FAQ content:**
```env
CHUNK_SIZE=400
MIN_CHUNK_SIZE=100
FILTER_NAVIGATION=true
CHUNK_OVERLAP=50
```

**Large manuals:**
```env
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
MIN_CHUNK_SIZE=200
```

### Performance Tuning

**For faster responses:**
```env
TOP_K_RESULTS=3
SIMILARITY_THRESHOLD=0.7
USE_RERANKING=false
CHUNK_SIZE=500
```

**For better accuracy:**
```env
TOP_K_RESULTS=8
SIMILARITY_THRESHOLD=0.5
USE_RERANKING=true
CHUNK_SIZE=600
```

## Security Considerations

### 1. API Key Management
- ✅ Never commit `.env` to git
- ✅ Use different keys for dev/prod
- ✅ Rotate keys periodically
- ✅ Store securely in CI/CD systems

### 2. Environment Variables in CI/CD

**GitHub Actions Example:**
```yaml
env:
  GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
  ENVIRONMENT: production
```

**Docker Example:**
```dockerfile
ARG GEMINI_API_KEY
ENV GEMINI_API_KEY=${GEMINI_API_KEY}
```

### 3. Production Checklist

- [ ] `ENVIRONMENT=production`
- [ ] `RELOAD=false`
- [ ] `LOG_LEVEL=INFO`
- [ ] `HOST=127.0.0.1` or specific IP
- [ ] API key from production project
- [ ] CORS properly configured
- [ ] Logs directed to persistent storage

## Troubleshooting

### Issue: "GEMINI_API_KEY not configured"

**Solution:**
1. Check `.env` exists: `ls .env`
2. Check key is set: `grep GEMINI_API_KEY .env`
3. Ensure no placeholder text
4. Restart application

### Issue: Memory usage high

**Solution:**
```env
CHUNK_SIZE=300    # Reduce chunk size
TOP_K_RESULTS=3   # Reduce retrieval results
```

### Issue: Slow responses

**Solution:**
```env
TOP_K_RESULTS=3      # Reduce from 5
SIMILARITY_THRESHOLD=0.7  # Stricter matching
```

### Issue: Missing content in responses

**Solution:**
```env
MIN_CHUNK_SIZE=50    # Allow smaller chunks
TOP_K_RESULTS=8      # Retrieve more
SIMILARITY_THRESHOLD=0.5  # Broader matching
```

## Validation

Check configuration is valid:

```python
from config.config import config

# Should print without errors
print(f"Model: {config.gemini.model}")
print(f"Chunk size: {config.chunking.chunk_size}")
print(f"Environment: {config.app.environment}")
```

Or use the setup script:
```bash
python setup.py
```

## Complete `.env` Example

```env
# ============================================
# GOOGLE GEMINI API (REQUIRED)
# ============================================
GEMINI_API_KEY=your_actual_key_here
GEMINI_MODEL=gemini-2.0-flash

# ============================================
# VECTOR DATABASE
# ============================================
VECTOR_DB_PATH=data/vector_db
COLLECTION_NAME=aloysius_knowledge

# ============================================
# TEXT CHUNKING STRATEGY
# ============================================
CHUNK_SIZE=500
CHUNK_OVERLAP=100
MIN_CHUNK_SIZE=200
MAX_CHUNK_SIZE=1000
FILTER_NAVIGATION=true
REMOVE_DUPLICATES=true
MIN_CONTENT_LENGTH=100

# ============================================
# RAG PIPELINE
# ============================================
TOP_K_RESULTS=5
SIMILARITY_THRESHOLD=0.6
USE_RERANKING=false

# ============================================
# LOGGING
# ============================================
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
LOG_FORMAT=json

# ============================================
# SERVER
# ============================================
HOST=0.0.0.0
PORT=8000
RELOAD=true

# ============================================
# APPLICATION
# ============================================
APP_NAME=St. Aloysius University AI Assistant
APP_VERSION=1.0.0
ENVIRONMENT=development
```

---

**For questions or custom configurations, contact the development team.**
