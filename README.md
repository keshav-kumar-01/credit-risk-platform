# 💳 Explainable AI Credit Risk Platform (v2.0)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Production-brightgreen)
![API](https://img.shields.io/badge/API-FastAPI-009688)

**A production-ready SaaS platform for explainable AI credit risk assessment**, combining bank-grade lending decisions with full transparency through SHAP, LIME, and counterfactual analysis.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Start the platform (API + Website)
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000

# Visit: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

---

## 🎯 Key Features

### 🤖 6 Machine Learning Models
- **CatBoost** (Best Performer), XGBoost, LightGBM, Random Forest, Gradient Boosting, Logistic Regression
- Automatic best-model selection with cross-validation

### 🔍 Triple Explainability
| Method | Type | Description |
|--------|------|-------------|
| **SHAP** | TreeExplainer | Game-theory based guaranteed fair attribution |
| **LIME** | Model-Agnostic | Local interpretable model-agnostic validation |
| **Counterfactual** | Perturbation | "What-if" scenarios showing path to approval |

### 📋 Comprehensive Application (50+ Fields)
Covers the **5 Cs of Credit** used by all major banks:
- **Character**: Credit history, payment behavior, inquiries
- **Capacity**: Income, debt-to-income ratio, employment
- **Capital**: Savings, investments, total assets
- **Collateral**: Property value, vehicle value
- **Conditions**: Loan purpose, amount, duration

### ⚖️ Fairness & Compliance
- **FCRA**: Auto-generated adverse action notices with specific reasons
- **ECOA**: Bias detection via Fairlearn across protected attributes
- **GDPR**: Right to explanation for automated decisions
- **SR 11-7**: Model documentation and validation framework

---

## 🏗️ Architecture

```
credit-risk-platform/
├── api/
│   └── main.py              # FastAPI SaaS API (v2.0)
├── website/                  # SaaS Website Frontend
│   ├── index.html           # Main page
│   ├── styles.css           # Premium dark theme CSS
│   └── app.js               # Interactive frontend JS
├── src/
│   ├── feature_engineering.py
│   ├── model_training.py
│   ├── explainability.py    # SHAP + LIME + Counterfactual
│   └── fairness_audit.py
├── models/
│   ├── trained/             # 6 ML model pickles
│   └── explainers/          # SHAP/LIME explainer objects
├── frontend/
│   └── app.py               # Streamlit dashboard (legacy)
├── data/
│   ├── raw/                 # German Credit + multi-source
│   └── processed/           # Train/test splits
└── docs/
    ├── API_DOCUMENTATION.md
    ├── MODEL_CARD.md
    └── DEPLOYMENT.md
```

---

## 📡 REST API

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/assess` | Full 50+ field credit assessment |
| `POST` | `/api/v1/quick-check` | Rapid 4-field screening |
| `POST` | `/api/v1/batch-assess` | Up to 100 applications |
| `POST` | `/api/v1/explain/lime` | LIME model-agnostic explanation |
| `GET` | `/api/v1/health` | Health check & uptime |
| `GET` | `/api/v1/model-info` | Model performance data |
| `GET` | `/api/v1/pricing` | Pricing tiers |
| `GET` | `/api/v1/application-fields` | All available fields |

### Quick Start Examples

**Python:**
```python
import requests

# Full Assessment
response = requests.post(
    "http://localhost:8000/api/v1/assess",
    json={
        "age": 35,
        "credit_amount": 25000,
        "duration": 36,
        "annual_income": 85000,
        "employment_status": "full_time",
        "credit_score": 720,
        "housing_status": "mortgage",
        "loan_purpose": "auto_purchase"
    },
    headers={"X-API-Key": "demo-key-free-tier"}
)

result = response.json()
print(f"Decision: {result['decision']}")
print(f"Risk Grade: {result['risk_grade']}")
print(f"Default Probability: {result['probability']:.1%}")
```

**cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/quick-check" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: demo-key-free-tier" \
  -d '{"age": 30, "credit_amount": 15000, "duration": 24, "installment_rate": 4}'
```

### API Response Format
```json
{
  "request_id": "uuid",
  "decision": "APPROVED",
  "probability": 0.1823,
  "risk_level": "LOW",
  "risk_grade": "A",
  "credit_score_equivalent": 740,
  "top_factors": [...],
  "explainability": {
    "method": "SHAP (TreeExplainer)",
    "top_factors": [...],
    "explanation_text": "Human-readable explanation..."
  },
  "debt_to_income_ratio": 0.15,
  "loan_to_value_ratio": 0.07,
  "processing_time_ms": 245.3
}
```

### Authentication
Pass your API key in the `X-API-Key` header.

| Tier | Limit | API Key |
|------|-------|---------|
| Free | 10/day | `demo-key-free-tier` |
| Starter | 500/day | Contact us |
| Business | 5,000/day | Contact us |
| Enterprise | Unlimited | Contact us |

---

## 🌐 SaaS Website

The platform includes a stunning dark-mode SaaS website at `http://localhost:8000/` with:

- **Hero** with animated gradient orbs and glassmorphism
- **Credit Assessment** form with Quick Check (4 fields) and Full Assessment (50+ fields)
- **Real-time Results** with risk gauge, SHAP factor bars, and decision explanations
- **API Documentation** with copy-able code samples in Python, cURL, and JavaScript
- **Pricing Page** with 4 tiers
- **Compliance Section** covering FCRA, ECOA, GDPR, SR 11-7
- **Fully Responsive** design for mobile, tablet, and desktop

---

## 🛠️ Development

```bash
# Run Streamlit dashboard (legacy)
streamlit run frontend/app.py

# Run API server with hot-reload
uvicorn api.main:app --reload --port 8000

# Run tests
pytest tests/ -v

# Docker
docker-compose up -d
```

---

## 📊 Model Performance

| Model | AUC-ROC | Accuracy | F1 Score |
|-------|---------|----------|----------|
| CatBoost | 0.79 | 76% | 0.74 |
| XGBoost | 0.78 | 75% | 0.73 |
| LightGBM | 0.77 | 75% | 0.72 |
| Random Forest | 0.76 | 74% | 0.71 |

---

## 📄 License

MIT License — See [LICENSE](LICENSE) for details.

## 👤 Author

**Keshav Kumar**
- Email: keshavkumarhf@gmail.com
- Phone: +91 92668 26263
