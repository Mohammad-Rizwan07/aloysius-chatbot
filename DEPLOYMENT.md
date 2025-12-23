# Deployment Guide

## Overview

This guide covers deploying the Aloysius Chatbot from development to production environments.

---

## Pre-Deployment Checklist

### Code Quality
- [ ] All tests passing
- [ ] No hardcoded values in code
- [ ] No API keys in repository
- [ ] All dependencies in `requirements.txt`
- [ ] Code follows PEP 8 style guide

### Configuration
- [ ] `.env.example` updated with latest options
- [ ] `.env` created with production values
- [ ] `ENVIRONMENT=production` set
- [ ] `RELOAD=false` for production
- [ ] API key validated

### Data
- [ ] Vector database populated (phases 1-4 run)
- [ ] Embeddings generated
- [ ] Quality of chunks verified
- [ ] No stale data

### Security
- [ ] SSL/TLS certificates ready
- [ ] API key rotated for production
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] Logging enabled

---

## Local Testing (Development)

### 1. Setup Environment
```bash
python setup.py
```

### 2. Configure for Testing
```env
ENVIRONMENT=development
LOG_LEVEL=DEBUG
RELOAD=true
PORT=8000
```

### 3. Start Server
```bash
python -m phase7_api.main
```

### 4. Test API
```bash
# Health check
curl http://localhost:8000/api/v1/health

# Chat
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"question":"Test question"}'

# Swagger UI
open http://localhost:8000/docs
```

### 5. Monitor Logs
```bash
tail -f logs/app.log
```

---

## Docker Deployment

### 1. Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create necessary directories
RUN mkdir -p logs data/vector_db

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Run application
CMD ["python", "-m", "phase7_api.main"]
```

### 2. Create .dockerignore

```
__pycache__/
*.py[cod]
.env
.git
.gitignore
venv/
logs/
data/raw_markdown/
data/processed_chunks/
.DS_Store
```

### 3. Build & Run Docker Image

```bash
# Build
docker build -t aloysius-chatbot:1.0.0 .

# Run
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=your_key \
  -e ENVIRONMENT=production \
  -e LOG_LEVEL=INFO \
  -v $(pwd)/logs:/app/logs \
  aloysius-chatbot:1.0.0
```

---

## Cloud Deployment (Google Cloud Run)

### 1. Prepare Application

```bash
# Create requirements.txt
pip freeze > requirements.txt
```

### 2. Create main.py (if not exists)

```python
# Already created in phase7_api/main.py
# Ensure it can be run as: python -m phase7_api.main
```

### 3. Deploy to Cloud Run

```bash
# Set project
gcloud config set project YOUR_PROJECT_ID

# Deploy
gcloud run deploy aloysius-chatbot \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_key,ENVIRONMENT=production
```

### 4. Configure Environment Variables

```bash
gcloud run services update aloysius-chatbot \
  --set-env-vars GEMINI_API_KEY=your_key,\
ENVIRONMENT=production,\
LOG_LEVEL=INFO,\
TOP_K_RESULTS=5
```

---

## Production Configuration

### .env for Production

```env
# LLM Configuration
GEMINI_API_KEY=your_production_key
GEMINI_MODEL=gemini-2.0-flash

# Environment
ENVIRONMENT=production
RELOAD=false

# Server
HOST=0.0.0.0
PORT=8000

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/aloysius/app.log

# Chunking (tuned for accuracy)
CHUNK_SIZE=600
CHUNK_OVERLAP=120
TOP_K_RESULTS=5

# Security
SIMILARITY_THRESHOLD=0.6
```

---

## Reverse Proxy Setup (Nginx)

### Configuration

```nginx
upstream aloysius_api {
    server localhost:8000;
}

server {
    listen 443 ssl http2;
    server_name api.staloysius.edu.in;

    ssl_certificate /etc/ssl/certs/staloysius.crt;
    ssl_certificate_key /etc/ssl/private/staloysius.key;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req zone=api_limit burst=20 nodelay;

    # Proxy settings
    location /api/ {
        proxy_pass http://aloysius_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Documentation
    location /docs {
        proxy_pass http://aloysius_api/docs;
    }

    location /redoc {
        proxy_pass http://aloysius_api/redoc;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name api.staloysius.edu.in;
    return 301 https://$server_name$request_uri;
}
```

---

## Monitoring & Logging

### Log Rotation (Linux)

Create `/etc/logrotate.d/aloysius-chatbot`:

```
/var/log/aloysius/app.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    postrotate
        systemctl reload aloysius-chatbot > /dev/null 2>&1 || true
    endscript
}
```

### Systemd Service (Linux)

Create `/etc/systemd/system/aloysius-chatbot.service`:

```ini
[Unit]
Description=Aloysius Chatbot API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/aloysius-chatbot
Environment="PATH=/opt/aloysius-chatbot/venv/bin"
ExecStart=/opt/aloysius-chatbot/venv/bin/python -m phase7_api.main
Restart=on-failure
RestartSec=10

# Logging
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable aloysius-chatbot
sudo systemctl start aloysius-chatbot

# Check status
sudo systemctl status aloysius-chatbot

# View logs
sudo journalctl -u aloysius-chatbot -f
```

---

## Performance Tuning

### Gunicorn Workers

For production, use Gunicorn instead of Uvicorn:

```bash
pip install gunicorn
```

Create `gunicorn_config.py`:

```python
# Server configuration
bind = "0.0.0.0:8000"
workers = 4  # 2 * CPU cores + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
timeout = 30

# Logging
accesslog = "/var/log/aloysius/access.log"
errorlog = "/var/log/aloysius/error.log"
loglevel = "info"
```

Run:
```bash
gunicorn -c gunicorn_config.py phase7_api.main:app
```

---

## Health Monitoring

### Automated Health Checks

```bash
# Cron job (every 5 minutes)
*/5 * * * * curl -f http://localhost:8000/api/v1/health || \
  systemctl restart aloysius-chatbot
```

### Performance Metrics

Monitor these metrics:
- Response time (target: <500ms)
- Confidence scores (target: >0.7)
- Error rate (target: <1%)
- API uptime (target: 99.9%)

---

## Backup & Recovery

### Database Backup

```bash
# Backup vector DB
tar -czf backup-$(date +%Y%m%d).tar.gz data/vector_db/

# Backup configuration
cp .env .env.backup
```

### Data Recovery

```bash
# Restore from backup
tar -xzf backup-20250101.tar.gz

# Regenerate embeddings if needed
python -m phase4_vectorstore.run_phase4
```

---

## Disaster Recovery

### If Vector DB Corrupted

1. Stop the application
2. Backup current vector DB
3. Delete `data/vector_db/`
4. Run phase 4: `python -m phase4_vectorstore.run_phase4`
5. Restart application

### If Gemini API Down

- Fallback: Use local LLM (requires separate setup)
- Or queue requests and retry later
- Or use cached responses for identical queries

---

## Security Hardening

### API Key Rotation

```bash
# 1. Generate new key in Google AI Studio
# 2. Update production .env
# 3. Restart application
# 4. Delete old key from Google Cloud Console
```

### CORS Configuration

For production, restrict CORS:

```env
# In future implementation:
# CORS_ORIGINS=https://staloysius.edu.in,https://www.staloysius.edu.in
```

### Rate Limiting

Enable in Nginx or use dedicated service:

```env
# Future: API key rate limiting
# MAX_REQUESTS_PER_MINUTE=100
```

---

## Rollback Procedure

If new version has issues:

```bash
# 1. Identify last stable version
git log --oneline

# 2. Checkout previous version
git checkout <previous-commit>

# 3. Restart application
systemctl restart aloysius-chatbot

# 4. Verify health
curl http://localhost:8000/api/v1/health
```

---

## CI/CD Pipeline (GitHub Actions)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run tests
        run: pytest
      
      - name: Deploy to Cloud Run
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: |
          gcloud run deploy aloysius-chatbot \
            --source . \
            --set-env-vars GEMINI_API_KEY=${{ secrets.GEMINI_API_KEY }}
```

---

## Monitoring Dashboard

Recommended tools:
- **Logging**: Google Cloud Logging
- **Monitoring**: Google Cloud Monitoring
- **APM**: DataDog or New Relic
- **Uptime**: UptimeRobot

---

## Support & Troubleshooting

### Common Issues

1. **High latency**
   - Increase `TOP_K_RESULTS`
   - Check vector DB size
   - Monitor network connectivity

2. **Low confidence scores**
   - Verify chunk quality
   - Check `SIMILARITY_THRESHOLD`
   - Re-run data pipeline

3. **API timeouts**
   - Increase timeout in Nginx
   - Reduce `TOP_K_RESULTS`
   - Scale horizontally with load balancer

---

## Next Steps

1. [ ] Setup production server
2. [ ] Configure SSL/TLS
3. [ ] Setup monitoring
4. [ ] Configure backups
5. [ ] Setup CI/CD pipeline
6. [ ] Document runbooks
7. [ ] Train support team

---

**Deployment Status**: Ready for Production  
**Last Updated**: December 2025
