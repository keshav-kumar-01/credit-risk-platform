"""
End-to-End Test Script for Credit Risk Platform v2.0
Tests all API endpoints and validates responses
"""
import requests
import json
import time
import sys

BASE = "http://localhost:8000"
HEADERS = {"X-API-Key": "demo-key-free-tier", "Content-Type": "application/json"}
passed = 0
failed = 0

def test(name, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  ✅ {name}")
    else:
        failed += 1
        print(f"  ❌ {name} — {detail}")

print("=" * 60)
print("CREDIT RISK PLATFORM v2.0 — END-TO-END TEST")
print("=" * 60)

# 1. Health Check
print("\n📋 1. Health Check")
r = requests.get(f"{BASE}/api/v1/health")
test("Status 200", r.status_code == 200)
d = r.json()
test("Model loaded", d["model_loaded"] == True)
test("Status healthy", d["status"] == "healthy")
test("Version 2.0.0", d["version"] == "2.0.0")

# 2. Quick Check
print("\n⚡ 2. Quick Credit Check")
r = requests.post(f"{BASE}/api/v1/quick-check", 
    json={"age": 30, "credit_amount": 15000, "duration": 24, "installment_rate": 4},
    headers=HEADERS)
test("Status 200", r.status_code == 200)
d = r.json()
test("Has decision", d["decision"] in ["APPROVED", "DECLINED"])
test("Has probability", 0 <= d["probability"] <= 1)
test("Has risk_grade", d["risk_grade"] in ["AAA","AA","A","BBB","BB","B","CCC","CC","D"])
test("Has score equiv", 300 <= d["credit_score_equivalent"] <= 850)
test("Has top factors", len(d["top_factors"]) > 0)
test("Has explainability", d["explainability"]["method"] == "SHAP (TreeExplainer)")
test("Has processing time", d["processing_time_ms"] > 0)
test("Has request_id", len(d["request_id"]) > 0)

# 3. Full Assessment
print("\n🏦 3. Full Credit Assessment")
full_app = {
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
    "credit_history": "existing_paid",
    "existing_credits": 2,
    "monthly_debt_payments": 1200,
    "credit_card_balance": 3500,
    "credit_card_limit": 15000,
    "credit_score": 720,
    "num_credit_inquiries_6m": 1,
    "num_late_payments_2y": 0,
    "housing_status": "mortgage",
    "property_value": 350000,
    "years_with_bank": 5,
    "has_checking_account": True,
    "has_savings_account": True,
    "has_direct_deposit": True,
    "has_co_applicant": False,
    "has_telephone": True,
    "is_foreign_worker": False,
    "bankruptcy_history": False,
    "foreclosure_history": False
}
r = requests.post(f"{BASE}/api/v1/assess", json=full_app, headers=HEADERS)
test("Status 200", r.status_code == 200)
d = r.json()
test("Has decision", d["decision"] in ["APPROVED", "DECLINED"])
test("Has DTI ratio", d["debt_to_income_ratio"] is not None)
test("Has LTV ratio", d["loan_to_value_ratio"] is not None)
test("Has explanation text", len(d["explainability"]["explanation_text"]) > 50)

# 4. Model Info
print("\n🤖 4. Model Info")
r = requests.get(f"{BASE}/api/v1/model-info")
test("Status 200", r.status_code == 200)
d = r.json()
test("Model name", d["model_name"] == "CatBoost Classifier")
test("Has compliance", len(d["compliance"]) >= 4)
test("Has explainability methods", len(d["explainability_methods"]) >= 3)

# 5. Pricing
print("\n💰 5. Pricing")
r = requests.get(f"{BASE}/api/v1/pricing")
test("Status 200", r.status_code == 200)
d = r.json()
test("4 tiers", len(d["tiers"]) == 4)

# 6. Application Fields
print("\n📋 6. Application Fields")
r = requests.get(f"{BASE}/api/v1/application-fields")
test("Status 200", r.status_code == 200)
d = r.json()
test("Has 9 sections", len(d["sections"]) == 9)
test("Has 30+ fields", len(d["fields"]) >= 30)

# 7. LIME Explanation
print("\n🧪 7. LIME Explanation")
r = requests.post(f"{BASE}/api/v1/explain/lime",
    json={"age": 30, "credit_amount": 15000, "duration": 24, "installment_rate": 4},
    headers=HEADERS)
test("Status 200", r.status_code == 200)
d = r.json()
test("Method is LIME", d["method"] == "LIME")
test("Has explanations", len(d["explanations"]) > 0)

# 8. Website Serving
print("\n🌐 8. Website")
r = requests.get(f"{BASE}/")
test("Status 200", r.status_code == 200)
test("HTML content", "CreditRisk" in r.text)
test("Has assess form", "quick-assess-form" in r.text)
test("Has pricing section", "pricing-section" in r.text)

r = requests.get(f"{BASE}/static/styles.css")
test("CSS served", r.status_code == 200)
r = requests.get(f"{BASE}/static/app.js")
test("JS served", r.status_code == 200)

# 9. Swagger Docs
print("\n📡 9. API Documentation")
r = requests.get(f"{BASE}/docs")
test("Swagger UI", r.status_code == 200)
r = requests.get(f"{BASE}/redoc")
test("ReDoc", r.status_code == 200)

# 10. Rate Limiting
print("\n🔒 10. Auth / Rate Limiting")
r = requests.post(f"{BASE}/api/v1/quick-check",
    json={"age": 30, "credit_amount": 5000, "duration": 12, "installment_rate": 2},
    headers={"X-API-Key": "invalid-key", "Content-Type": "application/json"})
test("Invalid key rejected (401)", r.status_code == 401)

# Summary
print("\n" + "=" * 60)
print(f"RESULTS: {passed} passed, {failed} failed, {passed + failed} total")
print("=" * 60)

if failed > 0:
    sys.exit(1)
else:
    print("🎉 ALL TESTS PASSED!")
