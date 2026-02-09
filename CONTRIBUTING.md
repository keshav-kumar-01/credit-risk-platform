# 🤝 Contributing to Credit Risk Platform

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [How to Contribute](#how-to-contribute)
4. [Development Setup](#development-setup)
5. [Coding Standards](#coding-standards)
6. [Testing](#testing)
7. [Pull Request Process](#pull-request-process)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors.

### Expected Behavior

- Be respectful and considerate
- Provide constructive feedback
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Publishing others' private information
- Any unethical or unprofessional conduct

---

## Getting Started

### Prerequisites

- Python 3.9+
- Git
- Basic understanding of machine learning
- Familiarity with scikit-learn, pandas, numpy

### Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/credit-risk-platform.git
cd credit-risk-platform

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/credit-risk-platform.git
```

---

## How to Contribute

### Types of Contributions

1. **Bug Reports**: Found a bug? Open an issue!
2. **Feature Requests**: Have an idea? We'd love to hear it!
3. **Code Contributions**: Fix bugs, add features, improve docs
4. **Documentation**: Improve README, add tutorials, fix typos
5. **Testing**: Add test cases, improve coverage

### Reporting Bugs

When filing a bug report, include:

- **Clear Title**: Descriptive and specific
- **Environment**: Python version, OS, dependencies
- **Steps to Reproduce**: Minimal example
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Screenshots**: If applicable

**Example:**

```markdown
**Bug**: Model prediction fails for missing features

**Environment**: Python 3.9, Windows 10

**Steps**:
1. Create input with only 3 features
2. Call /predict endpoint
3. See error

**Expected**: Graceful handling with default values
**Actual**: KeyError exception
```

### Suggesting Features

When suggesting features:

- **Use Case**: Why is this needed?
- **Proposed Solution**: How should it work?
- **Alternatives**: Other approaches considered?
- **Impact**: Who benefits? Breaking changes?

---

## Development Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If exists
```

### 3. Install Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install
```

### 4. Run Initial Tests

```bash
pytest tests/ -v
```

---

## Coding Standards

### Python Style

We follow **PEP 8** with some exceptions:

- **Line Length**: 88 characters (Black default)
- **Imports**: Group stdlib, third-party, local
- **Type Hints**: Encouraged for functions
- **Docstrings**: Google style

### Example

```python
from typing import List, Dict
import pandas as pd
from sklearn.model_selection import train_test_split


def train_model(X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
    """
    Train credit risk model.

    Args:
        X: Feature matrix
        y: Target vector

    Returns:
        Dictionary with performance metrics

    Raises:
        ValueError: If data is empty
    """
    if len(X) == 0:
        raise ValueError("Empty dataset")
    
    # Implementation here
    return {"accuracy": 0.85}
```

### Code Formatting

We use **Black** for auto-formatting:

```bash
# Install
pip install black

# Format code
black .

# Check without formatting
black --check .
```

### Linting

We use **Flake8**:

```bash
# Install
pip install flake8

# Run linter
flake8 src/ tests/
```

---

## Testing

### Running Tests

```bash
# All tests
pytest tests/ -v

# Specific file
pytest tests/test_api.py -v

# With coverage
pytest tests/ --cov=src --cov-report=html
```

### Writing Tests

- **Naming**: `test_<function_name>_<scenario>`
- **Structure**: Arrange-Act-Assert
- **Coverage**: Aim for 80%+

**Example:**

```python
def test_predict_single_valid_input():
    """Test single prediction with valid input"""
    # Arrange
    client = TestClient(app)
    payload = {
        "age": 30,
        "credit_amount": 5000,
        "duration": 24,
        "installment_rate": 4
    }
    
    # Act
    response = client.post("/predict", json=payload)
    
    # Assert
    assert response.status_code == 200
    assert "decision" in response.json()
```

---

## Pull Request Process

### 1. Create a Branch

```bash
git checkout -b feature/amazing-feature
```

**Branch naming**:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation
- `refactor/` - Code refactoring
- `test/` - Adding tests

### 2. Make Changes

- Write clean, documented code
- Add tests for new functionality
- Update documentation if needed
- Follow coding standards

### 3. Commit Changes

Use **conventional commits**:

```bash
git commit -m "feat: add SHAP waterfall plots"
git commit -m "fix: handle missing features in prediction"
git commit -m "docs: update API documentation"
```

**Commit types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

### 4. Push and Create PR

```bash
git push origin feature/amazing-feature
```

Then create a Pull Request on GitHub with:

- **Clear Title**: What does this PR do?
- **Description**: Why is this needed?
- **Testing**: How was it tested?
- **Screenshots**: If UI changes
- **Breaking Changes**: If any

**PR Template:**

```markdown
## Description
Adds SHAP waterfall plot visualization for better explanations.

## Motivation
Current force plots are hard to interpret for non-technical users.

## Changes
- Added waterfall plot function in explainability.py
- Updated frontend to display waterfall charts
- Added tests for new visualization

## Testing
- [ ] All tests pass
- [ ] Added new tests
- [ ] Manually tested in Streamlit

## Screenshots
[Attach screenshot]

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes
```

### 5. Code Review

- Address reviewer feedback promptly
- Keep scopes small and focused
- Be open to suggestions
- Update PR description if scope changes

### 6. Merge

Once approved:
- We'll merge using **squash and merge**
- Your contribution will be credited
- Branch will be deleted automatically

---

## Project Structure

```
credit-risk-platform/
├── src/              # Core ML code
├── api/              # FastAPI backend
├── frontend/         # Streamlit UI
├── tests/            # Unit tests
├── docs/             # Documentation
├── models/           # Saved models
├── data/             # Datasets
└── reports/          # Outputs
```

---

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Acknowledged in documentation

---

## Questions?

- **Issues**: Open a GitHub issue
- **Discussions**: Use GitHub Discussions
- **Email**: contribute@creditrisk.ai

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for making credit risk modeling more transparent and fair! 🙏**
