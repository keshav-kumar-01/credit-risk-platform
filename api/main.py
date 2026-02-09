"""
FastAPI Backend for Credit Risk Platform
RESTful API for production deployment
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# =====================================================
# PATH CONFIGURATION
# =====================================================

BASE_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = BASE_DIR / "src"
MODELS_DIR = BASE_DIR / "models"
REPORTS_DIR = BASE_DIR / "reports"

TRAINED_MODELS_DIR = MODELS_DIR / "trained"
EXPLAINERS_DIR = MODELS_DIR / "explainers"

sys.path.append(str(SRC_DIR))

from explainability import CreditExplainer
from feature_engineering import CreditFeatureEngineering

# =====================================================
# FASTAPI APP
# =====================================================

app = FastAPI(
    title="Credit Risk API",
    description="Explainable AI for Credit Risk Assessment",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# LOAD MODELS AT STARTUP
# =====================================================

@app.on_event("startup")
def load_models():
    """Load ML model and preprocessing pipeline on server start"""
    global model, feature_engineer, explainer
    
    try:
        model = joblib.load(TRAINED_MODELS_DIR / "best_model_catboost.pkl")
        feature_engineer = joblib.load(MODELS_DIR / "feature_engineer.pkl")
        explainer = joblib.load(EXPLAINERS_DIR / "credit_explainer.pkl")
        print("✅ Models loaded successfully")
    except Exception as e:
        print(f"❌ Error loading models: {e}")
        raise

# =====================================================
# PYDANTIC MODELS (REQUEST/RESPONSE)
# =====================================================

class CreditApplication(BaseModel):
    """Input schema for single prediction"""
    age: int = Field(..., ge=18, le=100, description="Applicant age")
    credit_amount: float = Field(..., ge=100, le=100000, description="Loan amount")
    duration: int = Field(..., ge=1, le=120, description="Loan duration in months")
    installment_rate: int = Field(..., ge=1, le=10, description="Installment rate as % of disposable income")
    
    class Config:
        schema_extra = {
            "example": {
                "age": 30,
                "credit_amount": 5000,
                "duration": 24,
                "installment_rate": 4
            }
        }

class FeatureImportance(BaseModel):
    """Feature importance for explanations"""
    feature: str
    impact: float
    direction: str  # POSITIVE or NEGATIVE

class PredictionResponse(BaseModel):
    """Output schema for predictions"""
    decision: str
    probability: float
    top_factors: List[FeatureImportance]
    recommendations: Optional[str] = None
    adverse_notice: Optional[str] = None

class BatchPredictionRequest(BaseModel):
    """Batch prediction input"""
    applications: List[CreditApplication]

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model_loaded: bool
    version: str

# =====================================================
# API ENDPOINTS
# =====================================================

@app.get("/", response_model=Dict[str, str])
def root():
    """Root endpoint"""
    return {
        "message": "Credit Risk API is running",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "version": "1.0.0"
    }

@app.post("/predict", response_model=PredictionResponse)
def predict_single(application: CreditApplication):
    """
    Single credit risk prediction with explainability
    
    Returns:
        - decision: APPROVED or DECLINED
        - probability: Default probability (0-1)
        - top_factors: Most influential features
        - recommendations: Actionable advice (if declined)
        - adverse_notice: Legal notice (if declined)
    """
    
    try:
        # Convert to DataFrame
        input_df = pd.DataFrame([application.dict()])
        
        # Feature engineering
        input_df = feature_engineer.create_features(input_df)
        input_df = feature_engineer.encode_categorical(input_df, fit=False)
        input_df = input_df.reindex(
            columns=feature_engineer.feature_names_,
            fill_value=0
        )
        input_df = feature_engineer.scale_numerical(input_df, fit=False)
        
        # Prediction
        prediction = int(model.predict(input_df)[0])
        probability = float(model.predict_proba(input_df)[0][1])
        
        # Explainability
        importance = explainer.explain_prediction_shap(input_df)
        top_5 = importance.head(5)
        
        top_factors = [
            FeatureImportance(
                feature=row.feature,
                impact=abs(float(row.shap_value)),
                direction="NEGATIVE" if row.shap_value > 0 else "POSITIVE"
            )
            for row in top_5.itertuples()
        ]
        
        decision = "DECLINED" if prediction == 1 else "APPROVED"
        
        # If declined, generate notices
        recommendations = None
        adverse_notice = None
        
        if prediction == 1:
            recommendations = explainer.actionable_recommendations(input_df)
            adverse_notice = explainer.generate_adverse_action_notice(input_df, prediction)
        
        return PredictionResponse(
            decision=decision,
            probability=probability,
            top_factors=top_factors,
            recommendations=recommendations,
            adverse_notice=adverse_notice
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.post("/batch-predict")
def predict_batch(batch: BatchPredictionRequest):
    """
    Batch credit risk predictions
    
    Returns:
        List of predictions for all applications
    """
    
    try:
        results = []
        
        for app in batch.applications:
            # Convert each application to prediction
            input_df = pd.DataFrame([app.dict()])
            
            # Feature engineering
            input_df = feature_engineer.create_features(input_df)
            input_df = feature_engineer.encode_categorical(input_df, fit=False)
            input_df = input_df.reindex(
                columns=feature_engineer.feature_names_,
                fill_value=0
            )
            input_df = feature_engineer.scale_numerical(input_df, fit=False)
            
            # Prediction
            prediction = int(model.predict(input_df)[0])
            probability = float(model.predict_proba(input_df)[0][1])
            
            results.append({
                "application": app.dict(),
                "decision": "DECLINED" if prediction == 1 else "APPROVED",
                "probability": probability
            })
        
        return {"predictions": results, "total": len(results)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch prediction error: {str(e)}")

@app.get("/model-info")
def model_info():
    """Get information about the loaded model"""
    
    try:
        # Read model comparison report
        comparison_df = pd.read_csv(REPORTS_DIR / "model_comparison.csv")
        
        return {
            "model_name": "CatBoost",
            "performance": comparison_df.iloc[0].to_dict(),
            "all_models": comparison_df.to_dict(orient="records"),
            "features": feature_engineer.feature_names_ if hasattr(feature_engineer, 'feature_names_') else []
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model info error: {str(e)}")

# =====================================================
# RUN SERVER
# =====================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
