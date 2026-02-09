"""
Unit tests for feature engineering module
"""

import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add src to path
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR / "src"))

from feature_engineering import CreditFeatureEngineering


@pytest.fixture
def sample_data():
    """Create sample credit data for testing"""
    return pd.DataFrame({
        'age': [25, 35, 45, 55],
        'credit_amount': [1000, 5000, 10000, 20000],
        'duration': [12, 24, 36, 48],
        'installment_rate': [2, 4, 3, 5],
        'target': [0, 1, 0, 1]
    })


def test_create_features(sample_data):
    """Test feature creation"""
    fe = CreditFeatureEngineering()
    df_transformed = fe.create_features(sample_data)
    
    # Check new features exist
    assert 'age_group' in df_transformed.columns
    assert 'credit_category' in df_transformed.columns
    assert 'duration_category' in df_transformed.columns
    assert 'monthly_burden' in df_transformed.columns


def test_encode_categorical(sample_data):
    """Test categorical encoding"""
    fe = CreditFeatureEngineering()
    df_transformed = fe.create_features(sample_data)
    df_encoded = fe.encode_categorical(df_transformed, fit=True)
    
    # Check no categorical columns remain
    assert df_encoded.select_dtypes(include=['object', 'category']).shape[1] == 0
    
    # Check feature_names_ is stored
    assert hasattr(fe, 'feature_names_')
    assert len(fe.feature_names_) > 0


def test_scale_numerical(sample_data):
    """Test numerical scaling"""
    fe = CreditFeatureEngineering()
    df_transformed = fe.create_features(sample_data)
    df_encoded = fe.encode_categorical(df_transformed.drop('target', axis=1), fit=True)
    df_scaled = fe.scale_numerical(df_encoded, fit=True)
    
    # Check scaler is fitted
    assert fe.scaler is not None
    assert hasattr(fe, 'numerical_cols')


def test_pipeline_consistency():
    """Test that the full pipeline works end-to-end"""
    fe = CreditFeatureEngineering()
    
    # Training data
    train_data = pd.DataFrame({
        'age': [25, 35, 45],
        'credit_amount': [1000, 5000, 10000],
        'duration': [12, 24, 36],
        'installment_rate': [2, 4, 3]
    })
    
    # Test data
    test_data = pd.DataFrame({
        'age': [30],
        'credit_amount': [7500],
        'duration': [18],
        'installment_rate': [3]
    })
    
    # Fit on training
    train_transformed = fe.create_features(train_data)
    train_encoded = fe.encode_categorical(train_transformed, fit=True)
    train_scaled = fe.scale_numerical(train_encoded, fit=True)
    
    # Transform test
    test_transformed = fe.create_features(test_data)
    test_encoded = fe.encode_categorical(test_transformed, fit=False)
    test_aligned = test_encoded.reindex(columns=fe.feature_names_, fill_value=0)
    test_scaled = fe.scale_numerical(test_aligned, fit=False)
    
    # Check shapes match
    assert train_scaled.shape[1] == test_scaled.shape[1]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
