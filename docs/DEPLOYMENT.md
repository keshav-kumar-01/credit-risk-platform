# 🚀 Deployment Guide

## Credit Risk Platform Deployment Options

---

## Table of Contents

1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [Database Setup](#database-setup)
5. [Environment Variables](#environment-variables)
6. [Production Checklist](#production-checklist)

---

## Local Development

### 1. Setup Python Environment

```bash
# Create virtual environment
conda create -n credit-risk python=3.9
conda activate credit-risk

# Install dependencies
pip install -r requirements.txt
```

### 2. Prepare Data & Models

```bash
# Download datasets (if needed)
python data/download_datasets.py

# Run feature engineering
python src/feature_engineering.py

# Train models
python src/model_training.py

# Generate explainability artifacts
python src/explainability.py

# Run fairness audit
python src/fairness_audit.py
```

### 3. Run Applications

**Streamlit Frontend:**
```bash
cd frontend
streamlit run app.py
```
Access: http://localhost:8501

**FastAPI Backend:**
```bash
cd api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
Access: http://localhost:8000/docs

---

## Docker Deployment

### 1. Create Dockerfile

Create `Dockerfile` in project root:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose ports
EXPOSE 8000 8501

# Default command (API)
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Create docker-compose.yml

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./models:/app/models
      - ./data:/app/data
    environment:
      - ENVIRONMENT=production
    command: uvicorn api.main:app --host 0.0.0.0 --port 8000

  frontend:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./models:/app/models
      - ./data:/app/data
    depends_on:
      - api
    command: streamlit run frontend/app.py --server.port 8501

  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: credit_risk
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: secure_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### 3. Build & Run

```bash
# Build images
docker-compose build

# Run containers
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

---

## Cloud Deployment

### AWS Deployment

#### Option 1: Elastic Beanstalk

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.9 credit-risk-platform

# Create environment
eb create credit-risk-prod

# Deploy
eb deploy

# Open in browser
eb open
```

#### Option 2: ECS (Fargate)

1. Push Docker image to ECR
2. Create ECS cluster
3. Define task definition
4. Create service
5. Configure ALB

**Estimated Cost**: $20-50/month

---

### Google Cloud Platform

#### Cloud Run (Recommended)

```bash
# Build & push to GCR
gcloud builds submit --tag gcr.io/PROJECT_ID/credit-risk-api

# Deploy
gcloud run deploy credit-risk-api \
  --image gcr.io/PROJECT_ID/credit-risk-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

**Estimated Cost**: $10-30/month (pay-per-use)

---

### Heroku

```bash
# Login
heroku login

# Create app
heroku create credit-risk-platform

# Add buildpack
heroku buildpacks:set heroku/python

# Deploy
git push heroku main

# Scale
heroku ps:scale web=1

# Open
heroku open
```

**Estimated Cost**: $7-25/month (Hobby/Professional dynos)

---

### Azure

#### App Service

```bash
# Login
az login

# Create resource group
az group create --name credit-risk-rg --location eastus

# Create app service plan
az appservice plan create --name credit-risk-plan \
  --resource-group credit-risk-rg --sku B1 --is-linux

# Create web app
az webapp create --resource-group credit-risk-rg \
  --plan credit-risk-plan --name credit-risk-app \
  --runtime "PYTHON|3.9"

# Deploy
az webapp up --name credit-risk-app
```

**Estimated Cost**: $13-55/month

---

## Database Setup

### PostgreSQL

```python
# .env file
DATABASE_URL=postgresql://user:password@localhost:5432/credit_risk

# Create tables
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT NOW(),
    age INT,
    credit_amount FLOAT,
    duration INT,
    installment_rate INT,
    decision VARCHAR(20),
    probability FLOAT,
    model_version VARCHAR(50)
);

CREATE INDEX idx_timestamp ON predictions(timestamp);
CREATE INDEX idx_decision ON predictions(decision);
```

### MongoDB

```python
# .env file
MONGO_URI=mongodb://localhost:27017/credit_risk

# Collections
db.predictions.createIndex({"timestamp": -1})
db.predictions.createIndex({"decision": 1})
```

---

## Environment Variables

Create `.env` file:

```bash
# Application
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/credit_risk
MONGO_URI=mongodb://localhost:27017/credit_risk

# API
API_KEY=your-api-key
RATE_LIMIT=1000

# Monitoring
SENTRY_DSN=your-sentry-dsn
LOG_LEVEL=INFO

# Model
MODEL_VERSION=1.0.0
MODEL_PATH=/app/models/trained/best_model_catboost.pkl
```

---

## Production Checklist

### Security
- [ ] Add API key authentication
- [ ] Enable HTTPS/SSL
- [ ] Set up CORS properly
- [ ] Implement rate limiting
- [ ] Validate all inputs
- [ ] Use environment variables for secrets
- [ ] Enable security headers

### Performance
- [ ] Enable response caching
- [ ] Use CDN for static assets
- [ ] Implement database connection pooling
- [ ] Add model prediction caching
- [ ] Enable gzip compression
- [ ] Optimize Docker image size

### Monitoring
- [ ] Set up logging (Sentry, LogRocket)
- [ ] Add performance monitoring (New Relic, Datadog)
- [ ] Configure alerting
- [ ] Set up uptime monitoring
- [ ] Track API usage metrics
- [ ] Monitor model performance drift

### Backup & Recovery
- [ ] Automated database backups
- [ ] Model version control
- [ ] Disaster recovery plan
- [ ] Health check endpoints
- [ ] Graceful shutdown handling

### Compliance
- [ ] GDPR compliance (EU)
- [ ] FCRA compliance (US)
- [ ] Data retention policies
- [ ] Audit logging
- [ ] Privacy policy
- [ ] Terms of service

---

## Scaling Strategies

### Horizontal Scaling
- Use load balancer (AWS ALB, GCP Load Balancer)
- Deploy multiple API instances
- Use Redis for session management
- Implement request queuing (Celery + RabbitMQ)

### Vertical Scaling
- Increase instance size
- Optimize model inference
- Use GPU for predictions (if using neural networks)

### Database Scaling
- Read replicas for queries
- Write sharding for predictions
- Use TimescaleDB for time-series data

---

## Cost Optimization

1. **Start Small**: Cloud Run or Heroku ($10-25/month)
2. **Scale Gradually**: Add resources based on usage
3. **Use Spot Instances**: AWS/GCP spot instances (70% cheaper)
4. **Cache Aggressively**: Reduce redundant predictions
5. **Monitor Usage**: Set budget alerts

---

## Support

For deployment support: devops@creditrisk.ai
