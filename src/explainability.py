import os
import shap
import lime
import lime.lime_tabular
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import joblib

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

# =====================================================
# PATH SETUP (SAFE & ABSOLUTE)
# =====================================================

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
TRAINED_MODELS_DIR = os.path.join(MODELS_DIR, "trained")
EXPLAINERS_DIR = os.path.join(MODELS_DIR, "explainers")

FIGURES_DIR = os.path.join(REPORTS_DIR, "figures")
OUTPUTS_DIR = os.path.join(REPORTS_DIR, "outputs")

for d in [EXPLAINERS_DIR, FIGURES_DIR, OUTPUTS_DIR]:
    os.makedirs(d, exist_ok=True)

# =====================================================
# FILE SAVE UTILITIES
# =====================================================

def save_txt(content: str, filename: str):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)


def save_pdf(content: str, filename: str):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    text = c.beginText()
    text.setTextOrigin(1 * inch, height - 1 * inch)
    text.setFont("Helvetica", 10)

    for line in content.split("\n"):
        text.textLine(line)
        if text.getY() < 1 * inch:
            c.drawText(text)
            c.showPage()
            text = c.beginText()
            text.setTextOrigin(1 * inch, height - 1 * inch)
            text.setFont("Helvetica", 10)

    c.drawText(text)
    c.save()

# =====================================================
# CREDIT EXPLAINER (EXPORTABLE)
# =====================================================

class CreditExplainer:
    """
    Explainable AI module for credit risk decisions
    Supports SHAP (Tree & Kernel), LIME, adverse action notices, and recommendations
    """

    def __init__(self, model, X_train, feature_names):
        self.model = model
        self.X_train = X_train
        self.feature_names = feature_names
        self.shap_explainer = None
        self.lime_explainer = None

    # ---------------- SHAP ----------------

    def initialize_shap(self):
        # We need to ensure we use a model wrapper that aligns CatBoost with SHAP expected inputs
        # But simpler: CatBoost has its own SHAP calculation or we adhere strictly to version compat.
        
        try:
            # Attempt efficient TreeExplainer first (for CatBoost/XGBoost/RF)
            self.shap_explainer = shap.TreeExplainer(self.model)
        except Exception as e:
            print(f"TreeExplainer failed ({e}), falling back to KernelExplainer...")
            # For KernelExplainer, we must use a background summary to avoid slowness
            # And pass the PREDICT PROBA function, not the model object itself
            background_summary = shap.sample(self.X_train, 50)
            self.shap_explainer = shap.KernelExplainer(
                self.model.predict_proba,
                background_summary
            )
        return self.shap_explainer

    def explain_prediction_shap(self, X_instance: pd.DataFrame):
        if self.shap_explainer is None:
            self.initialize_shap()

        # Handle mismatch: Model expects certain columns, ensure X_instance matches
        # X_instance should already be engineered/scaled from the app.
        
        try:
            shap_values = self.shap_explainer.shap_values(X_instance)
        except Exception as e:
            # Fallback if specific features are missing in the pool
            # Re-initialize explicitly with this instance structure if dynamic?
            # Or usually it means X_instance columns != X_train columns used for init.
            print(f"SHAP calculation error: {e}")
            raise e

        # CatBoost/Binary often returns list of arrays [class0, class1] or just raw array
        if isinstance(shap_values, list):
            # We want the positive class (Risk/Default = 1)
            shap_values = shap_values[1]
        
        # Dimensions check
        if len(shap_values.shape) > 1:
            # (1, num_features)
            single_shap = shap_values[0]
        else:
            single_shap = shap_values

        # Generate Force Plot (Safety wrapped)
        try:
            expected_val = self.shap_explainer.expected_value
            if isinstance(expected_val, np.ndarray) or isinstance(expected_val, list):
                expected_val = expected_val[1] # Class 1 base value

            shap.force_plot(
                expected_val,
                single_shap,
                X_instance.iloc[0],
                feature_names=self.feature_names,
                matplotlib=True,
                show=False
            )
            plt.savefig(
                os.path.join(FIGURES_DIR, "shap_force_plot_0.png"),
                dpi=300,
                bbox_inches="tight"
            )
            plt.close()
        except Exception as plot_err:
            print(f"SHAP Plotting Warning: {plot_err}")

        # Return Feature Importance DataFrame
        importance = (
            pd.DataFrame({
                "feature": self.feature_names,
                "shap_value": single_shap
            })
            .sort_values("shap_value", key=abs, ascending=False)
        )

        return importance

    # ---------------- LIME ----------------

    def initialize_lime(self):
        # LIME Tabular Explainer
        # Requires training data (numpy array preferred)
        self.lime_explainer = lime.lime_tabular.LimeTabularExplainer(
            training_data=self.X_train.values,
            feature_names=self.feature_names,
            class_names=['Approved', 'Declined'], # 0, 1
            mode='classification',
            verbose=False,
            random_state=42
        )
        return self.lime_explainer

    def explain_prediction_lime(self, X_instance: pd.DataFrame):
        if self.lime_explainer is None:
            self.initialize_lime()
            
        # LIME expects numpy array for the instance
        instance_array = X_instance.iloc[0].values
        
        exp = self.lime_explainer.explain_instance(
            data_row=instance_array,
            predict_fn=self.model.predict_proba,
            num_features=5
        )
        
        # Parse into structured format
        lime_list = exp.as_list()
        # list of tuples (feature_condition, contribution)
        return lime_list

    # ---------------- REPORTS & COUNTERFACTUALS ----------------

    def generate_adverse_action_notice(self, X_instance, prediction):
        # Get SHAP insights
        importance = self.explain_prediction_shap(X_instance)
        top = importance.head(5)

        prob = self.model.predict_proba(X_instance)[0][1]

        notice = f"""
ADVERSE ACTION NOTICE
====================

Decision: {'DECLINED' if prediction == 1 else 'APPROVED'}
Default Risk Probability: {prob:.2%}

Primary Factors Influencing Decision:
"""
        for i, row in enumerate(top.itertuples(), 1):
            impact = "NEGATIVE (Risk Increasing)" if row.shap_value > 0 else "POSITIVE (Supportive)"
            notice += f"\n{i}. {row.feature} ({impact}) | Impact Score: {abs(row.shap_value):.3f}"

        notice += """
------------------------------------------------------
Your Rights:
• You have the right to request a free copy of your credit report within 60 days.
• You have the right to dispute incomplete or inaccurate information.
• You have the right to request a specific reason for this decision.
------------------------------------------------------
"""
        return notice

    def actionable_recommendations(self, X_instance):
        importance = self.explain_prediction_shap(X_instance)
        
        # Filter for features increasing risk (positive SHAP for class 1)
        # We assume 1 = Default/Risk. Positive SHAP pushes towards 1.
        risk_drivers = importance[importance["shap_value"] > 0].head(5)

        text = "RECOMMENDATIONS TO IMPROVE APPROVAL ODDS\n"
        text += "======================================\n\n"

        if risk_drivers.empty:
            text += "Your profile is strong. Maintain current financial habits."
        else:
            for row in risk_drivers.itertuples():
                feat = row.feature
                # Simple logic for recommendation strings
                if "amount" in feat or "credit" in feat:
                    text += f"• Consider requesting a lower credit amount (Driver: {feat})\n"
                elif "duration" in feat:
                    text += f"• Adjust loan duration to lower monthly burden (Driver: {feat})\n"
                elif "income" in feat or "debt" in feat:
                    text += f"• Reduce existing debt obligations (Driver: {feat})\n"
                elif "age" in feat:
                     text += f"• Build longer credit history over time (Driver: {feat})\n"
                else:
                    text += f"• Improve metric: {feat}\n"

        return text

    def generate_counterfactual_insight(self, X_instance):
        """
        Simple heuristic/perturbation-based counterfactual.
        "What-if" analysis: How much does Income need to increase?
        """
        # Start simplistic: Check if increasing income by 10% flips prediction?
        # Or decreasing amount by 10%?
        
        base_pred = self.model.predict(X_instance)[0]
        if base_pred == 0:
            return "Application is already Approved."
            
        # Try Perturbations
        scenarios = []
        
        # 1. Decrease Credit Amount
        for pct in [0.9, 0.8, 0.7]:
            temp = X_instance.copy()
            if 'credit_amount' in temp.columns: # scaled? assume standard scaler... tough to inverse without scaler object.
                # Since we operate on PRE-PROCESSED data here (X_instance is passed from App after scaling)
                # We can't easily say "$500". We just say "Reduce 'credit_amount' feature value"
                temp['credit_amount'] = temp['credit_amount'] * pct # Rough reduction in scaled space if positive
                new_pred = self.model.predict(temp)[0]
                if new_pred == 0:
                    scenarios.append(f"Reducing Credit Amount by ~{int((1-pct)*100)}%")
                    break
        
        if not scenarios:
            return "No simple single-factor change found to flip decision. Requires multi-factor improvement."
            
        return "Possible Path to Approval: " + ", ".join(scenarios)

# =====================================================
# LOCAL TEST (OPTIONAL)
# =====================================================

if __name__ == "__main__":

    model = joblib.load(
        os.path.join(TRAINED_MODELS_DIR, "best_model_catboost.pkl")
    )

    X_train, X_test, y_train, y_test = joblib.load(
        os.path.join(PROCESSED_DIR, "train_test_data.pkl")
    )

    explainer = CreditExplainer(
        model=model,
        X_train=X_train,
        feature_names=X_train.columns.tolist()
    )

    sample = X_test.iloc[[0]]
    prediction = model.predict(sample)[0]
    
    # Test LIME
    print("Testing LIME...")
    lime_res = explainer.explain_prediction_lime(sample)
    print("LIME Result:", lime_res)

    notice = explainer.generate_adverse_action_notice(sample, prediction)
    recommendations = explainer.actionable_recommendations(sample)
    cf = explainer.generate_counterfactual_insight(sample)
    print("Counterfactual:", cf)

    save_txt(notice, os.path.join(OUTPUTS_DIR, "adverse_action_notice.txt"))
    save_pdf(notice, os.path.join(OUTPUTS_DIR, "adverse_action_notice.pdf"))

    save_txt(recommendations, os.path.join(OUTPUTS_DIR, "recommendations.txt"))
    save_pdf(recommendations, os.path.join(OUTPUTS_DIR, "recommendations.pdf"))

    joblib.dump(
        explainer,
        os.path.join(EXPLAINERS_DIR, "credit_explainer.pkl")
    )

    print("✅ CreditExplainer (LIME+SHAP+CF) exported successfully")
