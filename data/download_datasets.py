import pandas as pd
from pathlib import Path

# ===============================
# Project Paths (robust & safe)
# ===============================
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

# Create directories if they don't exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


# ===============================
# German Credit Dataset
# ===============================
def download_german_credit():
    """Download German Credit Dataset from UCI"""

    url = (
        "https://archive.ics.uci.edu/ml/"
        "machine-learning-databases/statlog/german/german.data"
    )

    columns = [
        'checking_status', 'duration', 'credit_history', 'purpose',
        'credit_amount', 'savings_status', 'employment', 'installment_rate',
        'personal_status', 'other_parties', 'residence_since', 'property_magnitude',
        'age', 'other_payment_plans', 'housing', 'existing_credits',
        'job', 'num_dependents', 'own_telephone', 'foreign_worker', 'target'
    ]

    df = pd.read_csv(url, sep=' ', names=columns)

    # Convert target: 1 = default, 0 = non-default
    df['target'] = df['target'].apply(lambda x: 0 if x == 1 else 1)

    output_path = RAW_DATA_DIR / "german_credit.csv"
    df.to_csv(output_path, index=False)

    print(f"✅ Downloaded German Credit: {df.shape}")
    print(f"📁 Saved to: {output_path}")

    return df


# ===============================
# Lending Club Dataset (Sample)
# ===============================
def download_lending_club(n_rows=100_000):
    """
    Download a safe sample of Lending Club dataset
    (Full dataset is very large)
    """

    url = "https://resources.lendingclub.com/LoanStats_2018Q4.csv.zip"

    df = pd.read_csv(
        url,
        skiprows=1,
        compression="zip",
        nrows=n_rows,
        low_memory=False
    )

    output_path = RAW_DATA_DIR / "lending_club_sample.csv"
    df.to_csv(output_path, index=False)

    print(f"✅ Downloaded Lending Club Sample: {df.shape}")
    print(f"📁 Saved to: {output_path}")

    return df


# ===============================
# Main Execution
# ===============================
if __name__ == "__main__":
    download_german_credit()
    download_lending_club(n_rows=100_000)
