# 📡 API Documentation

## Credit Risk Platform REST API

Base URL: `http://localhost:8000`

---

## Authentication

Currently no authentication required (add API keys in production).

---

## Endpoints

### 1. **Root**

**GET** `/`

Returns API status and documentation links.

**Response:**
```json
{
  "message": "Credit Risk API is running",
  "docs": "/docs",
  "health": "/health"
}
```

---

### 2. **Health Check**

**GET** `/health`

Check if the API and models are loaded correctly.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "version": "1.0.0"
}
```

---

### 3. **Single Prediction**

**POST** `/predict`

Assess credit risk for a single applicant with full explainability.

**Request Body:**
```json
{
  "age": 30,
  "credit_amount": 5000,
  "duration": 24,
  "installment_rate": 4
}
```

**Parameters:**
- `age` (int): Applicant age (18-100)
- `credit_amount` (float): Loan amount (100-100,000)
- `duration` (int): Loan duration in months (1-120)
- `installment_rate` (int): Installment rate as % of disposable income (1-10)

**Response:**
```json
{
  "decision": "APPROVED",
  "probability": 0.23,
  "top_factors": [
    {
      "feature": "credit_amount",
      "impact": 0.15,
      "direction": "NEGATIVE"
    },
    {
      "feature": "duration",
      "impact": 0.08,
      "direction": "POSITIVE"
    }
  ],
  "recommendations": null,
  "adverse_notice": null
}
```

**If Declined:**
```json
{
  "decision": "DECLINED",
  "probability": 0.78,
  "top_factors": [...],
  "recommendations": "RECOMMENDATIONS TO IMPROVE APPROVAL ODDS\n...",
  "adverse_notice": "ADVERSE ACTION NOTICE\n..."
}
```

---

### 4. **Batch Prediction**

**POST** `/batch-predict`

Process multiple credit applications at once.

**Request Body:**
```json
{
  "applications": [
    {
      "age": 30,
      "credit_amount": 5000,
      "duration": 24,
      "installment_rate": 4
    },
    {
      "age": 45,
      "credit_amount": 10000,
      "duration": 36,
      "installment_rate": 3
    }
  ]
}
```

**Response:**
```json
{
  "predictions": [
    {
      "application": {...},
      "decision": "APPROVED",
      "probability": 0.23
    },
    {
      "application": {...},
      "decision": "DECLINED",
      "probability": 0.82
    }
  ],
  "total": 2
}
```

---

### 5. **Model Information**

**GET** `/model-info`

Get details about the loaded model and its performance.

**Response:**
```json
{
  "model_name": "CatBoost",
  "performance": {
    "model_name": "catboost",
    "accuracy": 0.76,
    "roc_auc": 0.79,
    "precision": 0.625,
    "recall": 0.5,
    "f1_score": 0.556
  },
  "all_models": [...],
  "features": [...]
}
```

---

## Error Codes

- **200**: Success
- **422**: Validation Error (invalid input)
- **500**: Internal Server Error

---

## Interactive Documentation

FastAPI provides auto-generated interactive docs:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Code Examples

### Python

```python
import requests

# Single prediction
data = {
    "age": 30,
    "credit_amount": 5000,
    "duration": 24,
    "installment_rate": 4
}

response = requests.post("http://localhost:8000/predict", json=data)
result = response.json()

print(f"Decision: {result['decision']}")
print(f"Probability: {result['probability']:.2%}")
```

### JavaScript

```javascript
const data = {
  age: 30,
  credit_amount: 5000,
  duration: 24,
  installment_rate: 4
};

fetch('http://localhost:8000/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(data),
})
  .then(response => response.json())
  .then(result => {
    console.log('Decision:', result.decision);
    console.log('Probability:', result.probability);
  });
```

### cURL

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 30,
    "credit_amount": 5000,
    "duration": 24,
    "installment_rate": 4
  }'
```

---

## Rate Limiting

Not implemented yet. Recommend implementing in production:
- Free tier: 10 requests/day
- Starter: 500 requests/month
- Business: 5,000 requests/month
- Enterprise: Unlimited

---

## Deployment

### Local Development

```bash
cd api
uvicorn main:app --reload
```

### Production (Docker)

```bash
docker build -t credit-risk-api .
docker run -p 8000:8000 credit-risk-api
```

### Cloud Deployment

- **AWS**: Elastic Beanstalk or ECS
- **GCP**: Cloud Run or App Engine
- **Azure**: App Service or Container Instances
- **Heroku**: `heroku create` + `git push heroku main`

---

## Security Considerations

For production deployment:

1. **Add API Key Authentication**
2. **Implement Rate Limiting**
3. **Use HTTPS only**
4. **Validate all inputs**
5. **Add logging and monitoring**
6. **Implement CORS properly** (don't use `allow_origins=["*"]`)
7. **Use environment variables for secrets**

---

## Support

For API support: api-support@creditrisk.ai
