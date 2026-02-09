# 📋 Model Card: Credit Risk Assessment

## Model Details

**Model Name**: Credit Risk Classifier  
**Version**: 1.0.0  
**Date**: February 2026  
**Model Type**: CatBoost Gradient Boosting Classifier  
**License**: MIT  

---

## Intended Use

### Primary Use Case
Credit risk assessment for personal loans to predict default probability and make lending decisions.

### Intended Users
- Credit unions
- Microfinance institutions
- Online lenders
- FinTech companies
- Small banks

### Out-of-Scope Use Cases
- Corporate/business credit assessment
- Credit card fraud detection
- Identity verification
- Employment screening

---

## Model Architecture

### Algorithm
CatBoost (Categorical Boosting) with the following configuration:
- **Iterations**: 200
- **Depth**: 6
- **Learning Rate**: 0.1
- **Auto Class Weights**: Balanced

### Training Data
- **Primary Dataset**: German Credit Data (UCI Repository)
- **Size**: 1,000 records after preprocessing
- **Features**: 20+ features including age, credit amount, duration, employment status
- **Target**: Binary classification (0 = Good Credit, 1 = Bad Credit/Default)
- **Class Distribution**: Imbalanced (~30% default rate)
- **Preprocessing**: SMOTE oversampling for class balance

### Features
- Demographic: Age, residence duration
- Financial: Credit amount, savings, existing credits
- Employment: Job type, employment duration
- Loan: Purpose, duration, installment rate
- Derived: Age groups, credit categories, debt-to-income ratio

---

## Performance

### Test Set Results

| Model | Accuracy | ROC-AUC | Precision | Recall | F1-Score |
|-------|----------|---------|-----------|--------|----------|
| **CatBoost** | **76%** | **0.791** | **62.5%** | **50%** | **55.6%** |
| Gradient Boosting | 73% | 0.776 | 55.2% | 53.3% | 54.2% |
| Random Forest | 73% | 0.752 | 54.8% | 56.7% | 55.7% |

### Confusion Matrix (CatBoost)

```
                Predicted
               Good | Bad
Actual Good   122  |  18
       Bad     30  |  30
```

**Interpretation**:
- **True Negatives (122)**: Correctly identified good credits
- **False Positives (18)**: Good credits incorrectly rejected (Type I error)
- **False Negatives (30)**: Bad credits incorrectly approved (Type II error)
- **True Positives (30)**: Correctly identified bad credits

### Cost-Benefit Analysis

In credit lending, False Negatives (approving bad loans) are costlier than False Positives (rejecting good applicants):
- **False Negative Cost**: Loss of entire loan amount (~$5,000 average)
- **False Positive Cost**: Lost interest revenue (~$500 average)
- **Cost Ratio**: 10:1

Our model achieves a **balanced trade-off** with moderate recall (50%) and good precision (62.5%).

---

## Explainability

### Global Feature Importance (Top 10)

1. **credit_amount** (25.3%): Loan size is the strongest predictor
2. **duration** (18.7%): Longer loans = higher default risk
3. **age** (12.4%): Younger applicants slightly riskier
4. **employment_duration** (9.8%): Job stability matters
5. **existing_credits** (8.1%): Multiple loans increase risk
6. **installment_rate** (7.2%): Payment burden indicator
7. **savings_account** (6.5%): Financial cushion
8. **purpose_education** (4.3%): Education loans safer
9. **housing_own** (3.9%): Home ownership = stability
10. **residence_duration** (3.8%): Longer residence = lower risk

### SHAP (SHapley Additive exPlanations)

We use TreeExplainer for:
- **Local explanations**: Why was this specific loan rejected?
- **Force plots**: Visual breakdown of prediction
- **Waterfall charts**: Feature contribution breakdown

### LIME (Local Interpretable Model-agnostic Explanations)

Available as alternative explainer for:
- Model-agnostic interpretations
- Rule-based explanations
- Feature perturbation analysis

---

## Fairness & Bias

### Protected Attributes Analyzed
- Age groups (young vs. senior)
- Gender (if available in data)
- Employment status

### Fairness Metrics

| Metric | Threshold | Result | Status |
|--------|-----------|--------|--------|
| Demographic Parity Difference | < 0.10 | 0.08 | ✅ PASS |
| Equalized Odds Difference | < 0.10 | 0.11 | ⚠️ REVIEW |

### Bias Mitigation Strategies
1. **Balanced Training**: Auto class weights in CatBoost
2. **Sensitive Feature Control**: Option to remove protected attributes
3. **Post-processing**: Threshold optimization per group
4. **Monitoring**: Continuous fairness audits in production

---

## Regulatory Compliance

### United States
- ✅ **FCRA (Fair Credit Reporting Act)**: Adverse action notices provided
- ✅ **ECOA (Equal Credit Opportunity Act)**: Bias detection implemented
- ✅ **SR 11-7 (Model Risk Management)**: Documentation complete

### European Union
- ✅ **GDPR Article 22**: Right to explanation (SHAP/LIME)
- ✅ **AI Act**: Transparency requirements met

### Documentation Provided
1. Adverse Action Notices (PDF/TXT)
2. Feature importance explanations
3. Model performance reports
4. Fairness audit reports

---

## Limitations

### Known Issues
1. **Small Training Data**: Only 1,000 records (German Credit)
2. **Geographic Bias**: Trained on European data, may not generalize to other regions
3. **Temporal Drift**: Economic conditions change; requires retraining
4. **Feature Coverage**: Limited financial history features
5. **Class Imbalance**: Original data 70/30 split

### Edge Cases
- **New immigrants**: Limited credit history
- **Self-employed**: Income verification challenges
- **Students**: Low income but high future potential
- **Retirees**: Different risk profile than working age

### Recommendations
- **Regular Retraining**: Every 6 months or 10,000 new predictions
- **A/B Testing**: Compare against human decisions
- **Domain Expansion**: Add more diverse training data
- **Feature Engineering**: Incorporate payment history, credit bureau scores

---

## Ethical Considerations

### Potential Harms
1. **Discriminatory Lending**: Unintended bias against protected groups
2. **Financial Exclusion**: False rejections deny access to credit
3. **Debt Trap**: False approvals can lead to over-indebtedness

### Mitigation Strategies
1. **Continuous Monitoring**: Track approval rates by demographic
2. **Human Override**: Loan officers can override model decisions
3. **Appeals Process**: Rejected applicants can request review
4. **Transparency**: Full explanations provided for all decisions

### Responsible AI Principles
- **Fairness**: Regular bias audits
- **Accountability**: Clear ownership and escalation paths
- **Transparency**: Open-source explainability
- **Privacy**: No PII stored; GDPR compliant

---

## Maintenance & Monitoring

### Production Monitoring
- **Model Drift Detection**: Alert if accuracy drops below 70%
- **Data Drift**: Monitor feature distribution changes
- **Prediction Distribution**: Track approval/rejection rates
- **Fairness Metrics**: Weekly bias audits

### Retraining Triggers
1. Performance degradation (> 5% ROC-AUC drop)
2. Significant economic events (recession, policy changes)
3. 6 months elapsed since last training
4. New data exceeds 10,000 predictions

### Version Control
- Models stored with version tags
- Changelog maintained
- Rollback capability to previous versions

---

## Contact

**Model Owner**: Keshav Kumar  
**Email**: keshavkumarhf@gmail.com  
**Phone**: +91 9266826263  
**Documentation**: https://github.com/keshavkumar/credit-risk-platform  
**Support**: keshavkumarhf@gmail.com  

---

## References

1. German Credit Data: UCI Machine Learning Repository
2. SHAP: Lundberg & Lee (2017), "A Unified Approach to Interpreting Model Predictions"
3. Fairlearn: Microsoft Research, fairlearn.org
4. CatBoost: Prokhorenkova et al. (2018), "CatBoost: unbiased boosting with categorical features"

---

**Last Updated**: February 9, 2026  
**Next Review**: August 2026
