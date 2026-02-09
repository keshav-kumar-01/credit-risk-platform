import os
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    roc_curve,
)
import xgboost as xgb
import lightgbm as lgb
import catboost as cb
import joblib
import matplotlib.pyplot as plt
import seaborn as sns


# =======================
# PATH CONFIGURATION (CRITICAL)
# =======================

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DATA_PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
MODELS_TRAINED_DIR = os.path.join(BASE_DIR, "models", "trained")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
FIGURES_DIR = os.path.join(REPORTS_DIR, "figures")

# Ensure directories exist
os.makedirs(DATA_PROCESSED_DIR, exist_ok=True)
os.makedirs(MODELS_TRAINED_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)


class CreditRiskModels:
    """
    Train and evaluate multiple credit risk models
    """

    def __init__(self):
        self.models = {}
        self.results = {}

    def initialize_models(self):
        """Initialize all models"""

        self.models = {
            "logistic_regression": LogisticRegression(
                max_iter=1000,
                random_state=42,
                class_weight="balanced",
            ),

            "random_forest": RandomForestClassifier(
                n_estimators=200,
                max_depth=10,
                min_samples_split=10,
                min_samples_leaf=5,
                random_state=42,
                class_weight="balanced",
                n_jobs=-1,
            ),

            "xgboost": xgb.XGBClassifier(
                n_estimators=200,
                max_depth=6,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                scale_pos_weight=1,
                n_jobs=-1,
                eval_metric="logloss",
            ),

            "lightgbm": lgb.LGBMClassifier(
                n_estimators=200,
                max_depth=6,
                learning_rate=0.1,
                num_leaves=31,
                random_state=42,
                class_weight="balanced",
                n_jobs=-1,
            ),

            "catboost": cb.CatBoostClassifier(
                iterations=200,
                depth=6,
                learning_rate=0.1,
                random_state=42,
                verbose=False,
                auto_class_weights="Balanced",
            ),

            "gradient_boosting": GradientBoostingClassifier(
                n_estimators=200,
                max_depth=5,
                learning_rate=0.1,
                random_state=42,
            ),
        }

        return self.models

    def train_all_models(self, X_train, y_train):
        """Train all models"""
        for name, model in self.models.items():
            print(f"Training {name}...")
            model.fit(X_train, y_train)
            print(f"✅ {name} trained")
        return self.models

    def evaluate_model(self, model, X_test, y_test, model_name):
        """Evaluate a single model"""

        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]

        report = classification_report(y_test, y_pred, output_dict=True)

        results = {
            "model_name": model_name,
            "accuracy": (y_pred == y_test).mean(),
            "roc_auc": roc_auc_score(y_test, y_pred_proba),
            "precision": report["1"]["precision"],
            "recall": report["1"]["recall"],
            "f1_score": report["1"]["f1-score"],
            "confusion_matrix": confusion_matrix(y_test, y_pred),
        }

        self.results[model_name] = results
        return results

    def evaluate_all_models(self, X_test, y_test):
        """Evaluate all trained models"""

        results_df = []

        for name, model in self.models.items():
            print(f"\nEvaluating {name}...")
            res = self.evaluate_model(model, X_test, y_test, name)
            results_df.append(res)

            print(f"  Accuracy: {res['accuracy']:.4f}")
            print(f"  ROC-AUC: {res['roc_auc']:.4f}")
            print(f"  F1-Score: {res['f1_score']:.4f}")

        comparison_df = (
            pd.DataFrame(results_df)
            .sort_values("roc_auc", ascending=False)
        )

        print("\n" + "=" * 50)
        print("MODEL COMPARISON")
        print("=" * 50)
        print(comparison_df[["model_name", "accuracy", "roc_auc", "f1_score"]])

        return comparison_df

    def plot_roc_curves(self, X_test, y_test):
        """Plot ROC curves"""

        plt.figure(figsize=(12, 8))

        for name, model in self.models.items():
            y_pred_proba = model.predict_proba(X_test)[:, 1]
            fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
            auc = roc_auc_score(y_test, y_pred_proba)
            plt.plot(fpr, tpr, label=f"{name} (AUC={auc:.3f})")

        plt.plot([0, 1], [0, 1], "k--", label="Random")
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title("ROC Curves - Credit Risk Models")
        plt.legend(loc="lower right")
        plt.grid(alpha=0.3)

        plt.savefig(
            os.path.join(FIGURES_DIR, "roc_curves.png"),
            dpi=300,
            bbox_inches="tight",
        )
        plt.show()

    def save_best_model(self, comparison_df):
        """Save best model"""

        best_model_name = comparison_df.iloc[0]["model_name"]
        best_model = self.models[best_model_name]

        joblib.dump(
            best_model,
            os.path.join(
                MODELS_TRAINED_DIR,
                f"best_model_{best_model_name}.pkl",
            ),
        )

        for name, model in self.models.items():
            joblib.dump(
                model,
                os.path.join(MODELS_TRAINED_DIR, f"{name}.pkl"),
            )

        print(f"\n✅ Best model saved: {best_model_name}")
        return best_model, best_model_name


# =======================
# MAIN SCRIPT
# =======================
if __name__ == "__main__":

    # Load processed data safely
    X_train, X_test, y_train, y_test = joblib.load(
        os.path.join(DATA_PROCESSED_DIR, "train_test_data.pkl")
    )

    trainer = CreditRiskModels()
    trainer.initialize_models()
    trainer.train_all_models(X_train, y_train)

    comparison_df = trainer.evaluate_all_models(X_test, y_test)

    trainer.plot_roc_curves(X_test, y_test)

    best_model, best_name = trainer.save_best_model(comparison_df)

    comparison_df.to_csv(
        os.path.join(REPORTS_DIR, "model_comparison.csv"),
        index=False,
    )
