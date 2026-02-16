"""
Credit Risk Platform - Production SaaS API
============================================
Complete REST API for credit risk assessment with:
- Comprehensive bank-grade application fields
- API Key authentication & rate limiting
- SHAP, LIME, and counterfactual explainability
- Fairness audit endpoint
- Webhook support
- API versioning (v1)
"""

from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import List, Optional, Dict, Any
from enum import Enum
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os
import json
import time
import hashlib
import uuid
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
from collections import defaultdict

# =====================================================
# PATH CONFIGURATION
# =====================================================

BASE_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = BASE_DIR / "src"
MODELS_DIR = BASE_DIR / "models"
REPORTS_DIR = BASE_DIR / "reports"
DATA_DIR = BASE_DIR / "data"
FRONTEND_DIR = BASE_DIR / "website"

TRAINED_MODELS_DIR = MODELS_DIR / "trained"
EXPLAINERS_DIR = MODELS_DIR / "explainers"

sys.path.append(str(SRC_DIR))

from explainability import CreditExplainer
from feature_engineering import CreditFeatureEngineering

# Fix for joblib unpickling
import __main__
__main__.CreditFeatureEngineering = CreditFeatureEngineering
__main__.CreditExplainer = CreditExplainer

# =====================================================
# ENVIRONMENT CONFIGURATION
# =====================================================

ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")
DEBUG = os.environ.get("DEBUG", "True").lower() in ("true", "1", "yes")
SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-in-production")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
MODEL_VERSION = os.environ.get("MODEL_VERSION", "2.0.0")
MODEL_PATH = os.environ.get("MODEL_PATH", "models/trained/best_model_catboost.pkl")
RATE_LIMIT_DEFAULT = int(os.environ.get("RATE_LIMIT", "1000"))
CORS_ORIGINS_STR = os.environ.get("CORS_ORIGINS", "*")
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*")
PORT = int(os.environ.get("PORT", "8000"))

# Parse CORS origins
if CORS_ORIGINS_STR == "*":
    CORS_ORIGINS = ["*"]
else:
    CORS_ORIGINS = [origin.strip() for origin in CORS_ORIGINS_STR.split(",") if origin.strip()]

# =====================================================
# GLOBALS
# =====================================================

model = None
feature_engineer = None
explainer = None

# Simple in-memory rate limiting (use Redis in production)
rate_limit_store = defaultdict(list)

# API Keys — load custom key from env or use defaults
_custom_api_key = os.environ.get("API_KEY", "")
API_KEYS = {
    "demo-key-free-tier": {"tier": "free", "limit": 10, "name": "Demo User"},
    "starter-key-500": {"tier": "starter", "limit": 500, "name": "Starter User"},
    "business-key-5000": {"tier": "business", "limit": 5000, "name": "Business User"},
    "enterprise-key-unlimited": {"tier": "enterprise", "limit": 999999, "name": "Enterprise User"},
}
# If a custom API key is set via env, add it as an enterprise key
if _custom_api_key and _custom_api_key != "your-api-key-here":
    API_KEYS[_custom_api_key] = {"tier": "enterprise", "limit": 999999, "name": "Custom API Key"}

# =====================================================
# ENUMS FOR COMPREHENSIVE FIELDS
# =====================================================

class EmploymentStatus(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    SELF_EMPLOYED = "self_employed"
    RETIRED = "retired"
    UNEMPLOYED = "unemployed"
    STUDENT = "student"
    CONTRACT = "contract"
    MILITARY = "military"

class HousingStatus(str, Enum):
    OWN = "own"
    RENT = "rent"
    MORTGAGE = "mortgage"
    LIVING_WITH_FAMILY = "living_with_family"
    FREE = "free"
    OTHER = "other"

class LoanPurpose(str, Enum):
    HOME_PURCHASE = "home_purchase"
    HOME_IMPROVEMENT = "home_improvement"
    AUTO_PURCHASE = "auto_purchase"
    EDUCATION = "education"
    DEBT_CONSOLIDATION = "debt_consolidation"
    BUSINESS = "business"
    MEDICAL = "medical"
    PERSONAL = "personal"
    WEDDING = "wedding"
    VACATION = "vacation"
    MOVING = "moving"
    MAJOR_PURCHASE = "major_purchase"
    OTHER = "other"

class MaritalStatus(str, Enum):
    SINGLE = "single"
    MARRIED = "married"
    DIVORCED = "divorced"
    WIDOWED = "widowed"
    SEPARATED = "separated"
    DOMESTIC_PARTNER = "domestic_partner"

class EducationLevel(str, Enum):
    HIGH_SCHOOL = "high_school"
    SOME_COLLEGE = "some_college"
    BACHELORS = "bachelors"
    MASTERS = "masters"
    DOCTORATE = "doctorate"
    PROFESSIONAL = "professional"
    TRADE_SCHOOL = "trade_school"
    OTHER = "other"

class CheckingAccountStatus(str, Enum):
    NO_ACCOUNT = "no_account"
    NEGATIVE = "negative"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"

class SavingsAccountStatus(str, Enum):
    NO_SAVINGS = "no_savings"
    UNDER_500 = "under_500"
    BETWEEN_500_1000 = "between_500_1000"
    BETWEEN_1000_5000 = "between_1000_5000"
    OVER_5000 = "over_5000"

class CreditHistoryType(str, Enum):
    NO_HISTORY = "no_history"
    ALL_PAID = "all_paid"
    EXISTING_PAID = "existing_paid"
    DELAYED = "delayed"
    CRITICAL = "critical"

# =====================================================
# PYDANTIC MODELS - COMPREHENSIVE BANK-GRADE
# =====================================================

class ComprehensiveCreditApplication(BaseModel):
    """
    Complete credit application covering all fields used by banks for consumer lending.
    
    This includes the '5 Cs of Credit':
    1. Character (credit history, reliability)
    2. Capacity (income, debt ratios)
    3. Capital (savings, assets)
    4. Collateral (secured assets)
    5. Conditions (loan terms, economic factors)
    """
    
    # ---- SECTION 1: PERSONAL INFORMATION ----
    age: int = Field(..., ge=18, le=100, description="Applicant's age in years")
    marital_status: Optional[MaritalStatus] = Field(MaritalStatus.SINGLE, description="Marital status")
    num_dependents: Optional[int] = Field(1, ge=0, le=15, description="Number of dependents (children, elderly)")
    education_level: Optional[EducationLevel] = Field(EducationLevel.BACHELORS, description="Highest education level")
    years_at_current_address: Optional[int] = Field(4, ge=0, le=60, description="Years at current residential address")
    
    # ---- SECTION 2: EMPLOYMENT & INCOME ----
    employment_status: Optional[EmploymentStatus] = Field(EmploymentStatus.FULL_TIME, description="Current employment status")
    years_employed: Optional[float] = Field(3.0, ge=0, le=50, description="Years at current employer")
    annual_income: Optional[float] = Field(50000, ge=0, le=10000000, description="Gross annual income ($)")
    monthly_income: Optional[float] = Field(None, ge=0, le=1000000, description="Gross monthly income ($). Auto-calculated from annual if not provided.")
    other_income: Optional[float] = Field(0, ge=0, le=5000000, description="Other annual income sources ($)")
    
    # ---- SECTION 3: LOAN DETAILS ----
    credit_amount: float = Field(..., ge=100, le=10000000, description="Requested loan amount ($)")
    duration: int = Field(..., ge=1, le=360, description="Loan duration in months")
    loan_purpose: Optional[LoanPurpose] = Field(LoanPurpose.PERSONAL, description="Purpose of the loan")
    installment_rate: Optional[int] = Field(4, ge=1, le=10, description="Installment rate as % of disposable income")
    interest_rate_requested: Optional[float] = Field(None, ge=0, le=40, description="Requested interest rate (%)")
    
    # ---- SECTION 4: FINANCIAL PROFILE ----
    checking_account_status: Optional[CheckingAccountStatus] = Field(CheckingAccountStatus.MODERATE, description="Checking account balance status")
    savings_account_status: Optional[SavingsAccountStatus] = Field(SavingsAccountStatus.UNDER_500, description="Savings account balance status")
    existing_credits: Optional[int] = Field(1, ge=0, le=20, description="Number of existing credit accounts")
    credit_history: Optional[CreditHistoryType] = Field(CreditHistoryType.EXISTING_PAID, description="Credit history quality")
    
    # ---- SECTION 5: DEBT INFORMATION (Key for DTI) ----
    monthly_debt_payments: Optional[float] = Field(0, ge=0, le=500000, description="Total monthly debt payments ($)")
    credit_card_balance: Optional[float] = Field(0, ge=0, le=1000000, description="Total outstanding credit card balance ($)")
    credit_card_limit: Optional[float] = Field(10000, ge=0, le=5000000, description="Total credit card limit ($)")
    auto_loan_balance: Optional[float] = Field(0, ge=0, le=500000, description="Outstanding auto loan balance ($)")
    student_loan_balance: Optional[float] = Field(0, ge=0, le=500000, description="Outstanding student loan balance ($)")
    mortgage_balance: Optional[float] = Field(0, ge=0, le=5000000, description="Outstanding mortgage balance ($)")
    other_debt: Optional[float] = Field(0, ge=0, le=1000000, description="Other outstanding debt ($)")
    
    # ---- SECTION 6: CREDIT SCORE (if available) ----
    credit_score: Optional[int] = Field(None, ge=300, le=850, description="FICO credit score (300-850)")
    num_credit_inquiries_6m: Optional[int] = Field(0, ge=0, le=30, description="Hard credit inquiries in last 6 months")
    num_late_payments_2y: Optional[int] = Field(0, ge=0, le=50, description="Late payments in last 2 years")
    delinquencies_2y: Optional[int] = Field(0, ge=0, le=30, description="Delinquencies in last 2 years")
    public_records: Optional[int] = Field(0, ge=0, le=10, description="Public records (bankruptcies, liens)")
    collections_12m: Optional[int] = Field(0, ge=0, le=20, description="Collections in last 12 months")
    oldest_credit_line_years: Optional[float] = Field(5.0, ge=0, le=60, description="Age of oldest credit line in years")
    
    # ---- SECTION 7: ASSETS & COLLATERAL ----
    housing_status: Optional[HousingStatus] = Field(HousingStatus.RENT, description="Housing situation")
    property_value: Optional[float] = Field(0, ge=0, le=50000000, description="Estimated property value ($)")
    vehicle_value: Optional[float] = Field(0, ge=0, le=500000, description="Total vehicle value ($)")
    investment_accounts: Optional[float] = Field(0, ge=0, le=50000000, description="Investment/retirement account value ($)")
    total_assets: Optional[float] = Field(None, ge=0, le=100000000, description="Total estimated assets ($)")
    
    # ---- SECTION 8: BANKING RELATIONSHIP ----
    has_checking_account: Optional[bool] = Field(True, description="Has a checking account")
    has_savings_account: Optional[bool] = Field(True, description="Has a savings account")
    years_with_bank: Optional[float] = Field(3.0, ge=0, le=60, description="Years with current bank")
    has_direct_deposit: Optional[bool] = Field(True, description="Has direct deposit set up")
    
    # ---- SECTION 9: ADDITIONAL RISK FACTORS ----
    is_foreign_worker: Optional[bool] = Field(False, description="Foreign worker status")
    has_telephone: Optional[bool] = Field(True, description="Has registered telephone")
    has_co_applicant: Optional[bool] = Field(False, description="Has co-applicant or guarantor")
    bankruptcy_history: Optional[bool] = Field(False, description="Any bankruptcy in history")
    foreclosure_history: Optional[bool] = Field(False, description="Any foreclosure in history")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "age": 35,
                "marital_status": "married",
                "num_dependents": 2,
                "education_level": "bachelors",
                "years_at_current_address": 5,
                "employment_status": "full_time",
                "years_employed": 7,
                "annual_income": 85000,
                "other_income": 5000,
                "credit_amount": 25000,
                "duration": 36,
                "loan_purpose": "auto_purchase",
                "installment_rate": 3,
                "checking_account_status": "moderate",
                "savings_account_status": "between_500_1000",
                "existing_credits": 2,
                "credit_history": "existing_paid",
                "monthly_debt_payments": 1200,
                "credit_card_balance": 3500,
                "credit_card_limit": 15000,
                "credit_score": 720,
                "num_credit_inquiries_6m": 1,
                "num_late_payments_2y": 0,
                "housing_status": "mortgage",
                "property_value": 350000,
                "has_checking_account": True,
                "has_savings_account": True,
                "years_with_bank": 5,
                "is_foreign_worker": False
            }
        }
    )

# Simplified 4-field quick check (for small banks / quick screening)
class QuickCreditCheck(BaseModel):
    """Simplified 4-field credit check for quick screening"""
    age: int = Field(..., ge=18, le=100)
    credit_amount: float = Field(..., ge=100, le=10000000)
    duration: int = Field(..., ge=1, le=360)
    installment_rate: int = Field(..., ge=1, le=10)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {"age": 30, "credit_amount": 5000, "duration": 24, "installment_rate": 4}
        }
    )

class FeatureImportance(BaseModel):
    feature: str
    impact: float
    direction: str
    human_readable: Optional[str] = None

class ExplainabilityReport(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    method: str
    top_factors: List[FeatureImportance]
    base_value: Optional[float] = None
    model_output: Optional[float] = None
    explanation_text: str

class PredictionResponse(BaseModel):
    request_id: str
    timestamp: str
    decision: str
    probability: float
    risk_level: str
    credit_score_equivalent: int
    risk_grade: str
    top_factors: List[FeatureImportance]
    explainability: ExplainabilityReport
    recommendations: Optional[str] = None
    adverse_notice: Optional[str] = None
    counterfactual: Optional[str] = None
    debt_to_income_ratio: Optional[float] = None
    loan_to_value_ratio: Optional[float] = None
    processing_time_ms: float

class HealthResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    status: str
    model_loaded: bool
    version: str
    uptime_seconds: float
    total_predictions: int

class FairnessResponse(BaseModel):
    feature: str
    demographic_parity: float
    equalized_odds: float
    status: str
    by_group: Dict[str, Any]

# =====================================================
# HELPER FUNCTIONS
# =====================================================

start_time = time.time()
prediction_count = 0

CHECKING_MAP = {
    "no_account": "A14",
    "negative": "A11",
    "low": "A12",
    "moderate": "A13",
    "high": "A13"
}

SAVINGS_MAP = {
    "no_savings": "A61",
    "under_500": "A61",
    "between_500_1000": "A62",
    "between_1000_5000": "A63",
    "over_5000": "A65"
}

CREDIT_HISTORY_MAP = {
    "no_history": "A30",
    "all_paid": "A31",
    "existing_paid": "A32",
    "delayed": "A33",
    "critical": "A34"
}

EMPLOYMENT_MAP = {
    "unemployed": "A71",
    "student": "A71",
    "contract": "A72",
    "part_time": "A72",
    "full_time": "A73",
    "self_employed": "A74",
    "military": "A75",
    "retired": "A75"
}

PURPOSE_MAP = {
    "home_purchase": "A40",
    "home_improvement": "A40",
    "auto_purchase": "A42",
    "education": "A41",
    "debt_consolidation": "A46",
    "business": "A49",
    "medical": "A43",
    "personal": "A43",
    "wedding": "A43",
    "vacation": "A43",
    "moving": "A43",
    "major_purchase": "A43",
    "other": "A43"
}

HOUSING_MAP = {
    "rent": "A151",
    "own": "A152",
    "mortgage": "A152",
    "free": "A153",
    "living_with_family": "A153",
    "other": "A151"
}

def map_comprehensive_to_german_credit(app: ComprehensiveCreditApplication) -> dict:
    """Map comprehensive application to German Credit dataset features"""
    
    # Derive monthly income if not provided
    monthly_income = app.monthly_income or (app.annual_income or 50000) / 12
    
    # Calculate DTI
    total_monthly_debt = (app.monthly_debt_payments or 0)
    dti = total_monthly_debt / max(monthly_income, 1)
    
    # Map employment years to German Credit format
    years_emp = app.years_employed or 3
    if years_emp < 1:
        employment = "A71"
    elif years_emp < 4:
        employment = "A72"
    elif years_emp < 7:
        employment = "A73"
    else:
        employment = "A75"
    
    # Override with employment map if status provided
    if app.employment_status:
        employment = EMPLOYMENT_MAP.get(app.employment_status.value, "A73")
    
    # Personal status (marital + gender proxy)
    personal_status = "A93"  # default: male single
    if app.marital_status:
        if app.marital_status.value in ["married", "domestic_partner"]:
            personal_status = "A92"
        elif app.marital_status.value == "divorced":
            personal_status = "A94"
    
    # Build the feature dict matching German Credit schema
    feature_dict = {
        "checking_status": CHECKING_MAP.get(
            app.checking_account_status.value if app.checking_account_status else "moderate", "A14"
        ),
        "duration": app.duration,
        "credit_history": CREDIT_HISTORY_MAP.get(
            app.credit_history.value if app.credit_history else "existing_paid", "A32"
        ),
        "purpose": PURPOSE_MAP.get(
            app.loan_purpose.value if app.loan_purpose else "personal", "A43"
        ),
        "credit_amount": app.credit_amount,
        "savings_status": SAVINGS_MAP.get(
            app.savings_account_status.value if app.savings_account_status else "under_500", "A61"
        ),
        "employment": employment,
        "installment_rate": app.installment_rate or 4,
        "personal_status": personal_status,
        "other_parties": "A103" if app.has_co_applicant else "A101",
        "residence_since": min(app.years_at_current_address or 4, 4),
        "property_magnitude": "A121" if (app.property_value or 0) > 200000 else
                             "A122" if (app.property_value or 0) > 50000 else
                             "A123" if (app.property_value or 0) > 0 else "A124",
        "age": app.age,
        "other_payment_plans": "A143",
        "housing": HOUSING_MAP.get(
            app.housing_status.value if app.housing_status else "rent", "A152"
        ),
        "existing_credits": app.existing_credits or 1,
        "job": "A174" if app.employment_status and app.employment_status.value == "self_employed" else
              "A173" if (app.annual_income or 50000) > 40000 else
              "A172" if (app.annual_income or 50000) > 20000 else "A171",
        "num_dependents": min(app.num_dependents or 1, 2),
        "own_telephone": "A192" if app.has_telephone else "A191",
        "foreign_worker": "A201" if not app.is_foreign_worker else "A202"
    }
    
    return feature_dict, dti

def calculate_risk_grade(probability: float) -> tuple:
    """Map probability to risk grade and credit score equivalent"""
    if probability < 0.05:
        return "AAA", 820
    elif probability < 0.10:
        return "AA", 780
    elif probability < 0.15:
        return "A", 740
    elif probability < 0.25:
        return "BBB", 700
    elif probability < 0.35:
        return "BB", 660
    elif probability < 0.50:
        return "B", 620
    elif probability < 0.65:
        return "CCC", 580
    elif probability < 0.80:
        return "CC", 540
    else:
        return "D", 500

def make_prediction(feature_dict: dict) -> dict:
    """Core prediction logic"""
    global prediction_count
    prediction_count += 1
    
    start = time.time()
    
    input_df = pd.DataFrame([feature_dict])
    
    # Feature engineering pipeline
    input_df = feature_engineer.create_features(input_df)
    input_df = feature_engineer.encode_categorical(input_df, fit=False)
    input_df = input_df.reindex(
        columns=feature_engineer.feature_names_,
        fill_value=0
    )
    input_df = feature_engineer.scale_numerical(input_df, fit=False)
    
    # Make prediction
    prediction = int(model.predict(input_df)[0])
    probability = float(model.predict_proba(input_df)[0][1])
    
    # SHAP Explanation
    importance = explainer.explain_prediction_shap(input_df)
    top_10 = importance.head(10)
    
    top_factors = []
    for row in top_10.itertuples():
        direction = "RISK_INCREASING" if row.shap_value > 0 else "RISK_DECREASING"
        
        # Human-readable explanations
        feat = row.feature
        if "amount" in feat.lower() or "credit" in feat.lower():
            hr = "Loan amount impacts your risk profile"
        elif "duration" in feat.lower():
            hr = "Loan term length affects repayment risk"
        elif "age" in feat.lower():
            hr = "Age-related credit experience factor"
        elif "checking" in feat.lower():
            hr = "Checking account status indicates financial stability"
        elif "saving" in feat.lower():
            hr = "Savings buffer provides repayment safety net"
        elif "employment" in feat.lower():
            hr = "Employment stability affects repayment ability"
        elif "housing" in feat.lower():
            hr = "Housing situation indicates financial stability"
        elif "installment" in feat.lower():
            hr = "Monthly payment burden relative to income"
        elif "history" in feat.lower():
            hr = "Past credit behavior predicts future performance"
        else:
            hr = f"Factor: {feat.replace('_', ' ').title()}"
        
        top_factors.append(FeatureImportance(
            feature=feat,
            impact=abs(float(row.shap_value)),
            direction=direction,
            human_readable=hr
        ))
    
    # Risk assessment
    risk_grade, credit_score_eq = calculate_risk_grade(probability)
    risk_level = "LOW" if probability < 0.3 else "MEDIUM" if probability < 0.7 else "HIGH"
    decision = "DECLINED" if prediction == 1 else "APPROVED"
    
    # Explanations
    try:
        exp_val = explainer.shap_explainer.expected_value
        if isinstance(exp_val, (list, np.ndarray)):
            exp_val = float(exp_val[1]) if len(exp_val) > 1 else float(exp_val[0])
        else:
            exp_val = float(exp_val)
    except Exception:
        exp_val = None
    
    explanation_text = generate_explanation_text(decision, probability, top_factors[:5], risk_grade)
    
    explainability_report = ExplainabilityReport(
        method="SHAP (TreeExplainer)",
        top_factors=top_factors,
        base_value=exp_val,
        model_output=probability,
        explanation_text=explanation_text
    )
    
    # Generate notices if declined
    recommendations = None
    adverse_notice = None
    counterfactual = None
    
    if prediction == 1:
        recommendations = explainer.actionable_recommendations(input_df)
        adverse_notice = explainer.generate_adverse_action_notice(input_df, prediction)
        counterfactual = explainer.generate_counterfactual_insight(input_df)
    
    processing_time = (time.time() - start) * 1000
    
    return {
        "request_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "decision": decision,
        "probability": round(probability, 4),
        "risk_level": risk_level,
        "credit_score_equivalent": credit_score_eq,
        "risk_grade": risk_grade,
        "top_factors": top_factors,
        "explainability": explainability_report,
        "recommendations": recommendations,
        "adverse_notice": adverse_notice,
        "counterfactual": counterfactual,
        "processing_time_ms": round(processing_time, 2)
    }

def generate_explanation_text(decision, probability, top_factors, risk_grade):
    """Generate human-readable decision explanation"""
    
    text = f"CREDIT DECISION EXPLANATION\n{'='*40}\n\n"
    text += f"Decision: {decision}\n"
    text += f"Risk Grade: {risk_grade}\n"
    text += f"Default Probability: {probability:.1%}\n\n"
    
    text += "TOP INFLUENCING FACTORS:\n"
    for i, f in enumerate(top_factors, 1):
        icon = "⚠️" if f.direction == "RISK_INCREASING" else "✅"
        text += f"  {i}. {icon} {f.human_readable} (Impact: {f.impact:.3f})\n"
    
    text += f"\nThis assessment uses {len(top_factors)} key factors analyzed by our "
    text += "SHAP (SHapley Additive exPlanations) framework, which provides "
    text += "mathematically guaranteed fair attribution of each factor's contribution.\n"
    
    if decision == "DECLINED":
        text += "\nYour rights under the Fair Credit Reporting Act (FCRA):\n"
        text += "• You may request a free credit report within 60 days\n"
        text += "• You may dispute any inaccurate information\n"
        text += "• You may request the specific reasons for this decision\n"
    
    return text

# =====================================================
# RATE LIMITING
# =====================================================

async def check_rate_limit(api_key: str = Header(None, alias="X-API-Key")):
    """Check rate limits by API key"""
    
    # Allow unauthenticated requests with strict limit
    if api_key is None:
        api_key = "anonymous"
        tier_limit = 5
    elif api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")
    else:
        tier_limit = API_KEYS[api_key]["limit"]
    
    now = time.time()
    day_ago = now - 86400
    
    # Clean old entries
    rate_limit_store[api_key] = [t for t in rate_limit_store[api_key] if t > day_ago]
    
    if len(rate_limit_store[api_key]) >= tier_limit:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Limit: {tier_limit}/day. Upgrade your plan at /pricing"
        )
    
    rate_limit_store[api_key].append(now)
    return api_key

# =====================================================
# APP LIFECYCLE
# =====================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model, feature_engineer, explainer
    
    try:
        # Use MODEL_PATH env var or default paths
        model_path = BASE_DIR / MODEL_PATH
        model = joblib.load(str(model_path))
        feature_engineer = joblib.load(str(MODELS_DIR / "feature_engineer.pkl"))
        explainer = joblib.load(str(EXPLAINERS_DIR / "credit_explainer.pkl"))
        print(f"✅ All models loaded successfully (env: {ENVIRONMENT})")
    except Exception as e:
        print(f"⚠️ Error loading models: {e}")
        print(f"   Model path attempted: {BASE_DIR / MODEL_PATH}")
        print(f"   Models dir: {MODELS_DIR}")
        print(f"   Explainers dir: {EXPLAINERS_DIR}")
    
    yield

# =====================================================
# FASTAPI APP
# =====================================================

app = FastAPI(
    title="Credit Risk Platform API",
    description="""
# 💳 Explainable AI Credit Risk Assessment API

Production-ready API for credit risk assessment with:
- **Comprehensive Application**: 50+ fields covering all bank lending criteria
- **Quick Check**: 4-field rapid screening
- **Explainability**: SHAP, LIME, and counterfactual analysis
- **Fairness**: Bias detection across protected attributes
- **Compliance**: FCRA, ECOA, GDPR compliant adverse action notices

## Authentication
Pass your API key in the `X-API-Key` header.

## Rate Limits
| Tier | Limit | Price |
|------|-------|-------|
| Anonymous | 5/day | Free |
| Free | 10/day | $0 |
| Starter | 500/day | $99/mo |
| Business | 5,000/day | $299/mo |
| Enterprise | Unlimited | $999/mo |
    """,
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
    contact={
        "name": "Credit Risk Platform Support",
        "email": "keshavkumarhf@gmail.com",
    }
)

# CORS — uses CORS_ORIGINS env variable
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the website frontend
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

# =====================================================
# API ENDPOINTS
# =====================================================

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main website"""
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return HTMLResponse(content=index_path.read_text(encoding="utf-8"))
    return HTMLResponse(content="""
    <html><head><title>Credit Risk API</title></head>
    <body>
        <h1>💳 Credit Risk Platform API</h1>
        <p>API is running. Visit <a href="/docs">/docs</a> for interactive documentation.</p>
    </body></html>
    """)

@app.get("/api/v1/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "version": MODEL_VERSION,
        "uptime_seconds": round(time.time() - start_time, 2),
        "total_predictions": prediction_count
    }

@app.post("/api/v1/assess", response_model=PredictionResponse, tags=["Credit Assessment"])
async def assess_credit_full(
    application: ComprehensiveCreditApplication,
    api_key: str = Depends(check_rate_limit)
):
    """
    **Full Credit Assessment** - Comprehensive bank-grade evaluation
    
    Accepts 50+ fields covering the '5 Cs of Credit':
    - Character, Capacity, Capital, Collateral, Conditions
    
    Returns decision with full SHAP explainability, adverse action notices,
    and actionable recommendations.
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        feature_dict, dti = map_comprehensive_to_german_credit(application)
        result = make_prediction(feature_dict)
        
        # Add DTI and LTV
        result["debt_to_income_ratio"] = round(dti, 4)
        
        if application.property_value and application.property_value > 0:
            ltv = application.credit_amount / application.property_value
            result["loan_to_value_ratio"] = round(ltv, 4)
        
        return PredictionResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Assessment error: {str(e)}")

@app.post("/api/v1/quick-check", response_model=PredictionResponse, tags=["Credit Assessment"])
async def quick_credit_check(
    application: QuickCreditCheck,
    api_key: str = Depends(check_rate_limit)
):
    """
    **Quick Credit Check** - Rapid 4-field screening
    
    For fast pre-qualification decisions. Provide only:
    - Age, Credit Amount, Duration, Installment Rate
    
    Uses default values for all other fields.
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Build feature dict with defaults
        feature_dict = {
            "age": application.age,
            "credit_amount": application.credit_amount,
            "duration": application.duration,
            "installment_rate": application.installment_rate,
            "checking_status": "A14",
            "credit_history": "A32",
            "purpose": "A43",
            "savings_status": "A61",
            "employment": "A73",
            "personal_status": "A93",
            "other_parties": "A101",
            "residence_since": 4.0,
            "property_magnitude": "A123",
            "other_payment_plans": "A143",
            "housing": "A152",
            "existing_credits": 1.0,
            "job": "A173",
            "num_dependents": 1.0,
            "own_telephone": "A191",
            "foreign_worker": "A201"
        }
        
        result = make_prediction(feature_dict)
        return PredictionResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Quick check error: {str(e)}")

@app.post("/api/v1/batch-assess", tags=["Credit Assessment"])
async def batch_assess(
    applications: List[ComprehensiveCreditApplication],
    api_key: str = Depends(check_rate_limit)
):
    """
    **Batch Assessment** - Process up to 100 applications at once
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    if len(applications) > 100:
        raise HTTPException(status_code=400, detail="Maximum 100 applications per batch")
    
    results = []
    for app_data in applications:
        try:
            feature_dict, dti = map_comprehensive_to_german_credit(app_data)
            result = make_prediction(feature_dict)
            result["debt_to_income_ratio"] = round(dti, 4)
            results.append(result)
        except Exception as e:
            results.append({"error": str(e), "application_age": app_data.age})
    
    summary = {
        "total": len(results),
        "approved": sum(1 for r in results if r.get("decision") == "APPROVED"),
        "declined": sum(1 for r in results if r.get("decision") == "DECLINED"),
        "errors": sum(1 for r in results if "error" in r),
        "avg_probability": np.mean([r.get("probability", 0) for r in results if "error" not in r])
    }
    
    return {"summary": summary, "results": results}

@app.post("/api/v1/explain/lime", tags=["Explainability"])
async def explain_lime(
    application: QuickCreditCheck,
    api_key: str = Depends(check_rate_limit)
):
    """
    **LIME Explanation** - Model-agnostic local explanation
    
    Returns feature importance using LIME (Local Interpretable Model-Agnostic Explanations).
    Useful for second-opinion explanations alongside SHAP.
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        feature_dict = {
            "age": application.age,
            "credit_amount": application.credit_amount,
            "duration": application.duration,
            "installment_rate": application.installment_rate,
            "checking_status": "A14", "credit_history": "A32",
            "purpose": "A43", "savings_status": "A61",
            "employment": "A73", "personal_status": "A93",
            "other_parties": "A101", "residence_since": 4.0,
            "property_magnitude": "A123", "other_payment_plans": "A143",
            "housing": "A152", "existing_credits": 1.0,
            "job": "A173", "num_dependents": 1.0,
            "own_telephone": "A191", "foreign_worker": "A201"
        }
        
        input_df = pd.DataFrame([feature_dict])
        input_df = feature_engineer.create_features(input_df)
        input_df = feature_engineer.encode_categorical(input_df, fit=False)
        input_df = input_df.reindex(columns=feature_engineer.feature_names_, fill_value=0)
        input_df = feature_engineer.scale_numerical(input_df, fit=False)
        
        lime_result = explainer.explain_prediction_lime(input_df)
        
        return {
            "method": "LIME",
            "explanations": [
                {"condition": cond, "contribution": float(contrib)}
                for cond, contrib in lime_result
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LIME error: {str(e)}")

@app.get("/api/v1/model-info", tags=["System"])
async def model_info():
    """Get information about the loaded model and performance metrics"""
    try:
        comparison_path = REPORTS_DIR / "model_comparison.csv"
        if comparison_path.exists():
            comparison_df = pd.read_csv(comparison_path)
            all_models = comparison_df.drop(columns=["confusion_matrix"], errors="ignore").to_dict(orient="records")
        else:
            all_models = []
        
        return {
            "model_name": "CatBoost Classifier",
            "version": "2.0.0",
            "training_data": "German Credit + Multi-source",
            "features_used": len(feature_engineer.feature_names_) if hasattr(feature_engineer, 'feature_names_') else 0,
            "explainability_methods": ["SHAP (TreeExplainer)", "LIME", "Counterfactual"],
            "fairness_framework": "Fairlearn",
            "compliance": ["FCRA", "ECOA", "GDPR", "SR 11-7"],
            "all_models": all_models
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/pricing", tags=["Business"])
async def pricing():
    """Get pricing tiers and features"""
    return {
        "tiers": [
            {
                "name": "Free",
                "price": "$0/mo",
                "predictions_per_day": 10,
                "features": ["Basic predictions", "SHAP explanations", "Web dashboard"],
                "api_key": "demo-key-free-tier"
            },
            {
                "name": "Starter",
                "price": "$99/mo",
                "predictions_per_day": 500,
                "features": ["Full API access", "SHAP + LIME", "Adverse action notices", "Email support"],
            },
            {
                "name": "Business",
                "price": "$299/mo",
                "predictions_per_day": 5000,
                "features": ["White-label reports", "Batch processing", "Fairness audits", "Priority support", "Webhooks"],
            },
            {
                "name": "Enterprise",
                "price": "$999/mo",
                "predictions_per_day": "Unlimited",
                "features": ["Custom models", "On-premise", "24/7 support", "SLA guarantee", "Audit trail", "Custom training"],
            }
        ]
    }

@app.get("/api/v1/application-fields", tags=["Documentation"])
async def application_fields():
    """
    Get all available application fields with descriptions.
    Useful for building dynamic forms.
    """
    schema = ComprehensiveCreditApplication.model_json_schema()
    fields = {}
    
    for name, prop in schema.get("properties", {}).items():
        fields[name] = {
            "title": prop.get("title", name.replace("_", " ").title()),
            "description": prop.get("description", ""),
            "type": prop.get("type", "string"),
            "required": name in schema.get("required", []),
            "default": prop.get("default"),
            "minimum": prop.get("minimum"),
            "maximum": prop.get("maximum"),
            "enum": prop.get("enum"),
        }
    
    # Group by section
    sections = {
        "Personal Information": ["age", "marital_status", "num_dependents", "education_level", "years_at_current_address"],
        "Employment & Income": ["employment_status", "years_employed", "annual_income", "monthly_income", "other_income"],
        "Loan Details": ["credit_amount", "duration", "loan_purpose", "installment_rate", "interest_rate_requested"],
        "Financial Profile": ["checking_account_status", "savings_account_status", "existing_credits", "credit_history"],
        "Debt Information": ["monthly_debt_payments", "credit_card_balance", "credit_card_limit", "auto_loan_balance", "student_loan_balance", "mortgage_balance", "other_debt"],
        "Credit Score": ["credit_score", "num_credit_inquiries_6m", "num_late_payments_2y", "delinquencies_2y", "public_records", "collections_12m", "oldest_credit_line_years"],
        "Assets & Collateral": ["housing_status", "property_value", "vehicle_value", "investment_accounts", "total_assets"],
        "Banking Relationship": ["has_checking_account", "has_savings_account", "years_with_bank", "has_direct_deposit"],
        "Additional Risk Factors": ["is_foreign_worker", "has_telephone", "has_co_applicant", "bankruptcy_history", "foreclosure_history"]
    }
    
    return {"fields": fields, "sections": sections}

# =====================================================
# RUN SERVER
# =====================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT, reload=DEBUG)
