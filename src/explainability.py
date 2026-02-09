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
    Supports SHAP, adverse action notices, and recommendations
    """

    def __init__(self, model, X_train, feature_names):
        self.model = model
        self.X_train = X_train
        self.feature_names = feature_names
        self.shap_explainer = None
        self.lime_explainer = None

    # ---------------- SHAP ----------------

    def initialize_shap(self):
        try:
            self.shap_explainer = shap.TreeExplainer(self.model)
        except Exception:
            self.shap_explainer = shap.KernelExplainer(
                self.model.predict_proba,
                shap.sample(self.X_train, 100)
            )
        return self.shap_explainer

    def explain_prediction_shap(self, X_instance: pd.DataFrame):

        if self.shap_explainer is None:
            self.initialize_shap()

        shap_values = self.shap_explainer.shap_values(X_instance)

        if isinstance(shap_values, list):
            shap_values = shap_values[1]

        # Save SHAP force plot
        shap.force_plot(
            self.shap_explainer.expected_value[1]
            if isinstance(self.shap_explainer.expected_value, np.ndarray)
            else self.shap_explainer.expected_value,
            shap_values[0],
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

        importance = (
            pd.DataFrame({
                "feature": self.feature_names,
                "shap_value": shap_values[0]
            })
            .sort_values("shap_value", key=abs, ascending=False)
        )

        return importance

    # ---------------- REPORTS ----------------

    def generate_adverse_action_notice(self, X_instance, prediction):

        importance = self.explain_prediction_shap(X_instance)
        top = importance.head(5)

        notice = f"""
ADVERSE ACTION NOTICE
====================

Decision: {'DECLINED' if prediction == 1 else 'APPROVED'}
Default Risk Probability: {self.model.predict_proba(X_instance)[0][1]:.2%}

Primary Factors:
"""

        for i, row in enumerate(top.itertuples(), 1):
            impact = "NEGATIVE" if row.shap_value > 0 else "POSITIVE"
            notice += f"\n{i}. {row.feature} ({impact}) | Impact: {abs(row.shap_value):.3f}"

        notice += """
------------------------------------------------------
You have the right to:
• Request a free credit report
• Dispute incorrect information
• Request reconsideration
------------------------------------------------------
"""

        return notice

    def actionable_recommendations(self, X_instance):

        importance = self.explain_prediction_shap(X_instance)
        negative = importance[importance["shap_value"] > 0].head(5)

        text = "RECOMMENDATIONS TO IMPROVE APPROVAL ODDS\n"
        text += "======================================\n\n"

        for row in negative.itertuples():
            text += f"• Improve your {row.feature}\n"

        return text

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

    notice = explainer.generate_adverse_action_notice(sample, prediction)
    recommendations = explainer.actionable_recommendations(sample)

    save_txt(notice, os.path.join(OUTPUTS_DIR, "adverse_action_notice.txt"))
    save_pdf(notice, os.path.join(OUTPUTS_DIR, "adverse_action_notice.pdf"))

    save_txt(recommendations, os.path.join(OUTPUTS_DIR, "recommendations.txt"))
    save_pdf(recommendations, os.path.join(OUTPUTS_DIR, "recommendations.pdf"))

    joblib.dump(
        explainer,
        os.path.join(EXPLAINERS_DIR, "credit_explainer.pkl")
    )

    print("✅ CreditExplainer exported successfully")
