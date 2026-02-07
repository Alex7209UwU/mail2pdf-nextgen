# Mail2PDF NextGen - Docker Deployment Guide

**Production-Ready Docker Setup**

---

## 📦 Docker Overview

Mail2PDF NextGen is fully containerized with:
- Pre-built Docker image
- docker-compose orchestration
- Health checks
- Resource limits
- Non-root user
- Volume mapping

---

## 🚀 Quick Start

```bash
# 1. Clone repository
git clone https://github.com/Alex7209UwU/mail2pdf-nextgen.git
cd mail2pdf-nextgen

# 2. Start with docker-compose
docker-compose up -d

# 3. Open in browser
# http://localhost:5000

# 4. Check status
docker-compose ps
docker-compose logs -f mail2pdf

# 5. Stop
docker-compose down
```

---

## 📋 Prerequisites

- Docker 20.10+
- docker-compose 1.29+
- 2GB RAM minimum
- 500MB disk space

Installations:
- Docker: https://docs.docker.com/install/
- docker-compose: https://docs.docker.com/compose/install/

---

## 🐳 Docker Compose Setup

### File: docker-compose.yml

```yaml
version: '3.8'

services:
  mail2pdf:
    build: .
    container_name: mail2pdf-nextgen
    ports:
      - "5000:5000"
    volumes:
      - ./data/input:/app/data/input
      - ./data/output:/app/data/output
    environment:
      - PYTHONUNBUFFERED=1
      - FLASK_ENV=production
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      resources:
        limits:
          memory: 2G
```

### Command Reference

```bash
# Start container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop container
docker-compose stop

# Stop and remove
docker-compose down

# Rebuild image
docker-compose build

# Restart
docker-compose restart

# Status
docker-compose ps
```

---

## 📁 Volume Mapping

### Default Volumes

```
Host                  Container           Purpose
./data/input    ←→    /app/data/input     Email files
./data/output   ←→    /app/data/output    Generated PDFs
```

### Create Directories

```bash
mkdir -p data/input
mkdir -p data/output
```

### Usage

```bash
# Add email files to ./data/input
cp email1.eml data/input/
cp email2.msg data/input/

# Start container
docker-compose up -d

# PDFs appear in ./data/output
ls data/output/  # email1.pdf, email2.pdf
```

---

## 🔧 Configuration

### Environment Variables

Create `.env` file:

```env
PYTHONUNBUFFERED=1
FLASK_ENV=production
FLASK_DEBUG=0
```

### Custom Port

Edit docker-compose.yml:

```yaml
ports:
  - "8080:5000"  # Change first number
```

Then access: http://localhost:8080

### Custom Memory Limit

Edit docker-compose.yml:

```yaml
deploy:
  resources:
    limits:
      memory: 4G  # Increase from 2G
```

---

## 🏗️ Dockerfile Details

### Multi-Stage Build

```dockerfile
FROM python:3.11-slim

# System dependencies
RUN apt-get update && apt-get install -y \
    libcairo2 libffi-dev libxml2 curl

# Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Application
COPY main.py app.py config.py utils.py .
COPY templates/ templates/

# Non-root user
RUN useradd -m -u 1000 appuser
USER appuser

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s \
    CMD curl -f http://localhost:5000/ || exit 1

CMD ["python", "app.py"]
```

---

## 🛡️ Security

### Non-Root User

Container runs as `appuser:1000` (non-root)

```bash
# Verify
docker-compose exec mail2pdf id
# uid=1000(appuser) gid=1000(appuser) groups=1000(appuser)
```

### File Permissions

```bash
# Set correct permissions
chown -R 1000:1000 data/
chmod -R 755 data/
```

### Network Isolation

```yaml
networks:
  - mail2pdf-network

networks:
  mail2pdf-network:
    driver: bridge
```

---

## 📊 Monitoring

### Health Check

```bash
# Manual check
docker-compose exec mail2pdf \
  curl -f http://localhost:5000/ || echo "Unhealthy"

# View health status
docker ps --format "table {{.Names}}\t{{.Status}}"
```

### Logs

```bash
# Real-time logs
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail=100

# Filter by service
docker-compose logs mail2pdf

# Export logs
docker-compose logs > app.log
```

### Resource Usage

```bash
# Monitor resources
docker stats

# Specific container
docker stats mail2pdf-nextgen
```

---

## 🚀 Production Deployment

### AWS EC2

```bash
# 1. Launch EC2 instance (Ubuntu 22.04)
# 2. Install Docker
sudo apt update
sudo apt install -y docker.io docker-compose

# 3. Clone and run
git clone https://github.com/Alex7209UwU/mail2pdf-nextgen.git
cd mail2pdf-nextgen
docker-compose up -d

# 4. Configure firewall
# Allow port 5000 in security group
```

### Azure Container Instances

```bash
# Build image
docker build -t mail2pdf:latest .

# Push to ACR
az acr build --registry myregistry --image mail2pdf:latest .

# Deploy
az container create \
  --resource-group mygroup \
  --name mail2pdf \
  --image myregistry.azurecr.io/mail2pdf:latest \
  --ports 5000 \
  --memory 2
```

### Google Cloud Run

```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT_ID/mail2pdf

# Deploy
gcloud run deploy mail2pdf \
  --image gcr.io/PROJECT_ID/mail2pdf \
  --platform managed \
  --memory 2GB \
  --port 5000
```

---

## 🔄 Scaling

### Horizontal Scaling

Using docker-compose with nginx:

```yaml
version: '3.8'
services:
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
  
  mail2pdf:
    build: .
    deploy:
      replicas: 3  # 3 containers
```

### Load Balancing

nginx.conf:

```nginx
upstream mail2pdf {
    least_conn;
    server mail2pdf:5000;
    server mail2pdf:5000;
    server mail2pdf:5000;
}

server {
    listen 80;
    location / {
        proxy_pass http://mail2pdf;
    }
}
```

---

## 🧹 Cleanup

```bash
# Stop container
docker-compose down

# Remove volumes
docker-compose down -v

# Remove image
docker rmi mail2pdf-nextgen

# Full cleanup
docker system prune -a

# Check space saved
docker system df
```

---

## 🆘 Troubleshooting

### Port Already in Use

```bash
# Find process using port 5000
lsof -i :5000

# Kill it
kill -9 <PID>

# Or change port in docker-compose.yml
ports:
  - "5001:5000"
```

### Out of Memory

```bash
# Check usage
docker stats

# Increase limit
deploy:
  resources:
    limits:
      memory: 4G  # From 2G
```

### Container Crashes

```bash
# View logs
docker-compose logs -f

# Restart
docker-compose restart

# Full rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Permission Denied

```bash
# Fix volume permissions
chown -R 1000:1000 data/
chmod -R 755 data/

# Restart
docker-compose restart
```

---

## 📚 References

- Docker Docs: https://docs.docker.com/
- docker-compose: https://docs.docker.com/compose/
- Docker Security: https://docs.docker.com/engine/security/

---

**Mail2PDF NextGen - Docker Deployment Guide**
