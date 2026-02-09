# 💳 Explainable AI Credit Risk Platform

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Production-brightgreen)

A production-ready, explainable AI platform for credit risk assessment with built-in fairness auditing and regulatory compliance features.

## 🎯 Key Features

### 🤖 **Advanced ML Models**
- **6 State-of-the-art Models**: Logistic Regression, Random Forest, XGBoost, LightGBM, CatBoost, Gradient Boosting
- **Ensemble Methods**: Automated model comparison and best model selection
- **Imbalanced Data Handling**: SMOTE, SMOTEENN, and undersampling techniques
- **Feature Engineering**: Automated feature creation, encoding, and scaling

### 🔍 **Explainability (XAI)**
- **SHAP (SHapley Additive exPlanations)**: Global and local feature importance
- **LIME**: Model-agnostic explanations
- **Adverse Action Notices**: Legally compliant rejection notices (US regulations)
- **Actionable Recommendations**: What-if analysis for applicants

### ⚖️ **Fairness & Compliance**
- **Bias Detection**: Fairlearn integration for demographic parity and equalized odds
- **Protected Attributes**: Age, gender, and custom sensitive features
- **Regulatory Reports**: GDPR-compliant explanations, model documentation
- **Audit Trails**: Complete decision transparency

### 🚀 **Deployment Ready**
- **Streamlit Web App**: Interactive UI for single and batch predictions
- **FastAPI Backend**: RESTful API for production integration
- **Database Support**: PostgreSQL and MongoDB connectors
- **Scalable Architecture**: Modular design for easy extension

## 📊 **Model Performance**

| Model | Accuracy | ROC-AUC | F1-Score |
|-------|----------|---------|----------|
| CatBoost | 76% | 0.791 | 0.556 |
| Gradient Boosting | 73% | 0.776 | 0.542 |
| Random Forest | 73% | 0.752 | 0.557 |
| LightGBM | 71% | 0.750 | 0.517 |
| XGBoost | 72% | 0.734 | 0.491 |
| Logistic Regression | 73% | 0.717 | 0.542 |

## 🛠️ Installation

### Prerequisites
- Python 3.9 or higher
- Anaconda (recommended) or virtualenv

### Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/credit-risk-platform.git
cd credit-risk-platform

# Create virtual environment
conda create -n credit-risk python=3.9
conda activate credit-risk

# Install dependencies
pip install -r requirements.txt

# Run feature engineering
python src/feature_engineering.py

# Train models
python src/model_training.py

# Generate explainability artifacts
python src/explainability.py

# Run fairness audit
python src/fairness_audit.py

# Launch Streamlit app
cd frontend
streamlit run app.py
```

## 📁 Project Structure

```
credit-risk-platform/
├── data/
│   ├── raw/                    # Original datasets
│   ├── processed/              # Processed data after feature engineering
│   └── download_datasets.py    # Data download scripts
├── src/
│   ├── feature_engineering.py  # Feature creation & preprocessing
│   ├── model_training.py       # Train all ML models
│   ├── explainability.py       # SHAP, LIME, adverse notices
│   └── fairness_audit.py       # Bias detection & fairness
├── models/
│   ├── trained/                # Saved model files (.pkl)
│   ├── explainers/             # SHAP explainers
│   └── feature_engineer.pkl    # Preprocessing pipeline
├── frontend/
│   └── app.py                  # Streamlit web application
├── api/
│   └── main.py                 # FastAPI backend
├── notebooks/
│   └── 01_data_exploration.ipynb
├── reports/
│   ├── figures/                # Visualizations (ROC, SHAP plots)
│   ├── outputs/                # PDFs, notices, recommendations
│   └── model_comparison.csv    # Performance comparison
├── tests/
│   └── test_*.py               # Unit tests
├── docs/
│   └── API_DOCUMENTATION.md    # API reference
├── requirements.txt
└── README.md
```

## 🎨 Streamlit Web App

Launch the interactive web application:

```bash
cd frontend
streamlit run app.py
```

**Features:**
- 🏠 **Home**: Model performance dashboard
- 📊 **Single Prediction**: Real-time credit decision with explanations
- 📈 **Batch Analysis**: Upload CSV for bulk processing
- ⚖️ **Fairness Audit**: Bias detection reports

## 🔌 API Usage

Start the FastAPI server:

```bash
cd api
uvicorn main:app --reload
```

**Example Request:**

```python
import requests

data = {
    "age": 30,
    "credit_amount": 5000,
    "duration": 24,
    "installment_rate": 4
}

response = requests.post("http://localhost:8000/predict", json=data)
print(response.json())
```

**Response:**

```json
{
    "decision": "APPROVED",
    "probability": 0.23,
    "top_factors": [
        {"feature": "credit_amount", "impact": 0.15},
        {"feature": "duration", "impact": -0.08}
    ],
    "recommendations": ["Maintain current payment history"]
}
```

## 📚 Data Sources

This platform uses publicly available datasets:

1. **German Credit Data** (UCI Repository) - 1,000 records
2. **Lending Club Loan Data** - 2M+ records
3. **Give Me Some Credit** (Kaggle) - 150k+ records
4. **Home Credit Default Risk** (Kaggle) - 300k+ records

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src --cov-report=html
```

## 💰 Monetization Strategy

### SaaS Pricing Tiers

| Tier | Price | Predictions/Month | Features |
|------|-------|-------------------|----------|
| **Free** | $0 | 10 | Basic predictions |
| **Starter** | $99 | 500 | API access + explanations |
| **Business** | $299 | 5,000 | White-label + batch |
| **Enterprise** | $999 | Unlimited | Custom models + SLA |

### Target Customers
- Credit unions
- Microfinance institutions
- FinTech lenders (Affirm, Klarna competitors)
- Small banks
- Buy-now-pay-later startups

### Revenue Projections
- **Year 1**: $23k (10 small + 3 mid-size clients)
- **Year 2**: $80k-120k (50 customers + enterprise)
- **Year 3**: $200k-500k (100+ customers + white-label)

## 🔒 Regulatory Compliance

- ✅ **FCRA** (Fair Credit Reporting Act) - Adverse action notices
- ✅ **ECOA** (Equal Credit Opportunity Act) - Bias detection
- ✅ **GDPR** (EU) - Right to explanation
- ✅ **SR 11-7** (Federal Reserve) - Model risk management

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 📧 Contact

For enterprise inquiries: contact@creditrisk.ai

## 🙏 Acknowledgments

- **SHAP** by Scott Lundberg
- **Fairlearn** by Microsoft Research
- **UCI Machine Learning Repository**
- **Kaggle** for public datasets

---

**Built with ❤️ for transparent and fair AI in finance**
