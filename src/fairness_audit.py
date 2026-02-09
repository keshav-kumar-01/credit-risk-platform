import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from fairlearn.metrics import (
    MetricFrame,
    demographic_parity_difference,
    equalized_odds_difference,
    selection_rate
)

# =====================================================
# PATH SETUP (ABSOLUTE & SAFE)
# =====================================================

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
TRAINED_MODELS_DIR = os.path.join(MODELS_DIR, "trained")
FIGURES_DIR = os.path.join(REPORTS_DIR, "figures")

os.makedirs(FIGURES_DIR, exist_ok=True)


# =====================================================
# FAIRNESS AUDITOR
# =====================================================

class FairnessAuditor:
    """
    Audit ML models for fairness and bias
    Suitable for regulatory & compliance checks
    """

    def __init__(self, model, X_test, y_test, sensitive_features):
        self.model = model
        self.X_test = X_test
        self.y_test = y_test
        self.sensitive_features = sensitive_features

    def calculate_fairness_metrics(self):

        y_pred = self.model.predict(self.X_test)
        results = {}

        for feature_name, feature_values in self.sensitive_features.items():

            metric_frame = MetricFrame(
                metrics={
                    "accuracy": lambda y_true, y_pred: (y_true == y_pred).mean(),
                    "selection_rate": selection_rate,
                    "false_positive_rate": lambda y_true, y_pred:
                        ((y_pred == 1) & (y_true == 0)).sum() / max((y_true == 0).sum(), 1)
                },
                y_true=self.y_test,
                y_pred=y_pred,
                sensitive_features=feature_values
            )

            dp = demographic_parity_difference(
                self.y_test, y_pred, sensitive_features=feature_values
            )

            eo = equalized_odds_difference(
                self.y_test, y_pred, sensitive_features=feature_values
            )

            results[feature_name] = {
                "metric_frame": metric_frame,
                "demographic_parity": dp,
                "equalized_odds": eo
            }

            print(f"\n{'='*50}")
            print(f"Fairness Metrics for: {feature_name}")
            print(f"{'='*50}")
            print(f"Demographic Parity Difference: {dp:.4f}")
            print(f"Equalized Odds Difference: {eo:.4f}")
            print("\nMetrics by Group:")
            print(metric_frame.by_group)

        return results

    def plot_fairness_comparison(self, results, metric="selection_rate"):

        fig, axes = plt.subplots(1, len(results), figsize=(14, 5))
        if len(results) == 1:
            axes = [axes]

        for idx, (feature_name, result) in enumerate(results.items()):
            mf = result["metric_frame"]
            mf.by_group[metric].plot(kind="bar", ax=axes[idx])
            axes[idx].set_title(f"{metric} by {feature_name}")
            axes[idx].axhline(
                y=mf.overall[metric], color="red", linestyle="--", label="Overall"
            )
            axes[idx].legend()
            axes[idx].grid(alpha=0.3)

        plt.tight_layout()
        plt.savefig(
            os.path.join(FIGURES_DIR, "fairness_comparison.png"),
            dpi=300,
            bbox_inches="tight"
        )
        plt.show()

    def generate_fairness_report(self, results):

        report = """
FAIRNESS AUDIT REPORT
====================

This report evaluates model bias across protected attributes.
Thresholds:
• |metric| < 0.10 → PASS
• |metric| < 0.20 → REVIEW
• |metric| ≥ 0.20 → FAIL
"""

        for feature, res in results.items():
            dp, eo = res["demographic_parity"], res["equalized_odds"]

            dp_status = "PASS" if abs(dp) < 0.1 else "REVIEW" if abs(dp) < 0.2 else "FAIL"
            eo_status = "PASS" if abs(eo) < 0.1 else "REVIEW" if abs(eo) < 0.2 else "FAIL"

            report += f"""
--------------------------------------------------
Protected Attribute: {feature}
--------------------------------------------------
Demographic Parity Difference: {dp:.4f} [{dp_status}]
Equalized Odds Difference:     {eo:.4f} [{eo_status}]
"""

        report += """
--------------------------------------------------
Recommendations:
• Review biased features
• Consider fairness-aware training
• Apply post-processing mitigation
• Escalate to compliance if FAIL
--------------------------------------------------
"""

        return report


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    model = joblib.load(
        os.path.join(TRAINED_MODELS_DIR, "best_model_catboost.pkl")
    )

    X_train, X_test, y_train, y_test = joblib.load(
        os.path.join(PROCESSED_DIR, "train_test_data.pkl")
    )

    # Synthetic sensitive attributes (replace with real ones in production)
    np.random.seed(42)
    sensitive_features = {
        "age_group": np.random.choice(["young", "middle", "senior"], size=len(X_test)),
        "gender": np.random.choice(["M", "F"], size=len(X_test))
    }

    auditor = FairnessAuditor(model, X_test, y_test, sensitive_features)

    results = auditor.calculate_fairness_metrics()
    auditor.plot_fairness_comparison(results)

    report = auditor.generate_fairness_report(results)
    print(report)

    with open(
        os.path.join(REPORTS_DIR, "fairness_audit_report.txt"),
        "w",
        encoding="utf-8"
    ) as f:
        f.write(report)

    print("✅ Fairness audit completed and saved")
