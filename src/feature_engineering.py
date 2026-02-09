import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib


# =======================
# PATH CONFIGURATION (CRITICAL FIX)
# =======================

# Project root directory (credit-risk-platform)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DATA_RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
DATA_PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Ensure directories exist
os.makedirs(DATA_PROCESSED_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)


class CreditFeatureEngineering:
    """
    Feature engineering for credit risk modeling
    """

    def __init__(self):
        self.scaler = None
        self.categorical_cols = None
        self.numerical_cols = None

    def create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create derived features"""
        df = df.copy()

        # Age groups
        df["age_group"] = pd.cut(
            df["age"],
            bins=[0, 25, 35, 45, 55, 100],
            labels=["very_young", "young", "middle", "senior", "elderly"],
        )

        # Credit amount categories
        df["credit_category"] = pd.cut(
            df["credit_amount"],
            bins=5,
            labels=["very_low", "low", "medium", "high", "very_high"],
        )

        # Debt-to-income proxy
        if "income" in df.columns:
            df["debt_to_income"] = df["credit_amount"] / (df["income"] + 1)

        # Duration categories
        df["duration_category"] = pd.cut(
            df["duration"],
            bins=[0, 12, 24, 36, 100],
            labels=["short", "medium", "long", "very_long"],
        )

        # Installment burden
        if "installment_rate" in df.columns:
            df["monthly_burden"] = (
                df["credit_amount"]
                / (df["duration"] + 1)
                * (df["installment_rate"] / 100)
            )

        return df

    def encode_categorical(self, df: pd.DataFrame, fit: bool = True) -> pd.DataFrame:
        """One-hot encode categorical features (SMOTE-safe)"""
        df = df.copy()

        if fit:
            self.categorical_cols = df.select_dtypes(
                include=["object", "category"]
            ).columns.tolist()

        df = pd.get_dummies(df, columns=self.categorical_cols, drop_first=True)
        
        # Store feature names after encoding
        if fit:
            self.feature_names_ = df.columns.tolist()
        
        return df

    def scale_numerical(self, df: pd.DataFrame, fit: bool = True) -> pd.DataFrame:
        """Scale numerical features"""
        df = df.copy()

        if fit:
            self.numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            self.scaler = StandardScaler()
            df[self.numerical_cols] = self.scaler.fit_transform(
                df[self.numerical_cols]
            )
        else:
            df[self.numerical_cols] = self.scaler.transform(
                df[self.numerical_cols]
            )

        return df

    def handle_imbalance(self, X, y, method="smote"):
        """Handle class imbalance"""
        from imblearn.over_sampling import SMOTE
        from imblearn.under_sampling import RandomUnderSampler
        from imblearn.combine import SMOTEENN

        if method == "smote":
            sampler = SMOTE(random_state=42)
        elif method == "undersample":
            sampler = RandomUnderSampler(random_state=42)
        elif method == "smoteenn":
            sampler = SMOTEENN(random_state=42)
        else:
            raise ValueError("Invalid imbalance method")

        X_resampled, y_resampled = sampler.fit_resample(X, y)

        print(f"Original shape: {X.shape}")
        print(f"Resampled shape: {X_resampled.shape}")
        print(f"Class distribution: {np.bincount(y_resampled)}")

        return X_resampled, y_resampled


# =======================
# MAIN SCRIPT
# =======================
if __name__ == "__main__":

    # Load data safely
    data_path = os.path.join(DATA_RAW_DIR, "german_credit.csv")
    df = pd.read_csv(data_path)

    fe = CreditFeatureEngineering()

    # Feature creation
    df = fe.create_features(df)

    # Split features & target
    X = df.drop("target", axis=1)
    y = df["target"]

    # Train-test split (NO LEAKAGE)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Encode categorical features
    X_train = fe.encode_categorical(X_train, fit=True)
    X_test = fe.encode_categorical(X_test, fit=False)

    # Align train & test columns
    X_train, X_test = X_train.align(
        X_test, join="left", axis=1, fill_value=0
    )

    # Scale numerical features
    X_train = fe.scale_numerical(X_train, fit=True)
    X_test = fe.scale_numerical(X_test, fit=False)

    # Handle imbalance (TRAIN ONLY)
    X_train, y_train = fe.handle_imbalance(X_train, y_train, method="smote")

    # Save outputs safely
    joblib.dump(
        (X_train, X_test, y_train, y_test),
        os.path.join(DATA_PROCESSED_DIR, "train_test_data.pkl"),
    )

    joblib.dump(
        fe,
        os.path.join(MODELS_DIR, "feature_engineer.pkl"),
    )

    print("✅ Feature engineering completed successfully!")
