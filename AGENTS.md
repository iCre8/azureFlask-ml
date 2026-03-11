# AGENTS.md - Development Guidelines for azureFlask-ml

## Project Overview

This is a Flask-based machine learning application that serves a Boston Housing prediction model. The app accepts JSON payloads via REST API and returns predictions.

## Technology Stack

- **Python**: 3.x (note: CI shows 6.2.0 which appears to be a typo - use Python 3.x)
- **Flask**: 1.0.2
- **pandas**: 0.24.2
- **scikit-learn**: 0.20.3
- **Testing**: pytest
- **Linting**: pylint
- **Load Testing**: locust

---

## Build, Lint, and Test Commands

### Installation

```bash
# Create virtual environment
make setup

# Install dependencies
make install
# Or manually:
pip install --upgrade pip && pip install -r requirements.txt
```

### Running Tests

```bash
# Run all tests
make test

# Run a single test file
python -m pytest test_hello.py -v

# Run a single test function
python -m pytest test_hello.py::test_hello_subtract -v

# Run with verbose output
python -m pytest -vv test_hello.py
```

### Linting

```bash
# Run pylint on specific files
make lint

# Or run pylint directly
pylint --disable=R,C hello.py app.py
```

### Running the Application

```bash
# Run Flask app
python app.py

# This runs on localhost:5000 with debug mode enabled
```

### Load Testing

```bash
# Run locust load tests
locust -f locustfile.py --host=http://localhost:5000
```

---

## Code Style Guidelines

### Imports

- Standard library imports first
- Third-party imports second
- Local application imports last
- Separate each group with a blank line
- Use explicit imports (avoid `from module import *`)

```python
# Correct
import logging
from flask import Flask, request, jsonify
import pandas as pd
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler

# Avoid
from flask import *
import os, sys, json
```

### Formatting

- Use 4 spaces for indentation (not tabs)
- Maximum line length: 100 characters (soft limit: 120)
- Use blank lines to separate logical sections within functions
- Two blank lines between top-level definitions

### Naming Conventions

- **Functions/Variables**: `snake_case` (e.g., `def scale_payload()`, `LOG`)
- **Classes**: `PascalCase` (e.g., `class MyModel`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_CONNECTIONS`)
- **Private functions**: Prefix with underscore (e.g., `_internal_helper()`)

### Type Annotations

- Use type hints for function parameters and return values when beneficial
- Keep annotations simple for compatibility with older Python versions

```python
def scale(payload: pd.DataFrame) -> pd.DataFrame:
    scaler = StandardScaler().fit(payload)
    return scaler.transform(payload)
```

### Error Handling

- Always use specific exception types instead of bare `except:`
- Log errors appropriately before returning error responses
- Return meaningful HTTP status codes and error messages

```python
# Good
try:
    clf = joblib.load("boston_housing_prediction.joblib")
except IOError as e:
    LOG.error(f"Failed to load model: {e}")
    return jsonify({'error': 'Model not loaded'}), 500

# Avoid
try:
    clf = joblib.load("boston_housing_prediction.joblib")
except:
    return "Model not loaded"  # Silent failure
```

### Logging

- Use the application's logger (`LOG`) for consistent log formatting
- Include relevant context in log messages
- Use appropriate log levels: DEBUG, INFO, WARNING, ERROR

```python
LOG.info("Scaling payload with shape: %s", payload.shape)
LOG.error("Prediction failed: %s", str(e))
```

### Flask Routes

- Define routes using the `@app.route()` decorator
- Use appropriate HTTP methods (GET, POST, etc.)
- Return JSON responses using `jsonify()` for proper content-type headers

```python
@app.route("/predict", methods=['POST'])
def predict():
    try:
        # ... prediction logic
        return jsonify({'prediction': prediction})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
```

### Testing Guidelines

- Test files should be named `test_<module>.py`
- Test functions should be prefixed with `test_`
- Use descriptive test names that explain what is being tested
- Utilize pytest fixtures for setup/teardown when needed

```python
def test_predict_returns_valid_response():
    response = client.post('/predict', json=sample_payload)
    assert response.status_code == 200
    assert 'prediction' in response.json
```

### General Best Practices

1. **Keep functions small** - Aim for single responsibility
2. **Write docstrings** - Document public APIs and complex logic
3. **Avoid magic numbers** - Use named constants
4. **Handle edge cases** - Check for empty inputs, null values
5. **Validate inputs** - Check data types and ranges early
6. **Version control** - Commit frequently with descriptive messages

---

## CI/CD

The project uses GitHub Actions (`.github/workflows/main.yml`) which runs:
1. `make install` - Install dependencies
2. `make lint` - Run pylint
3. `make test` - Run pytest

All tests must pass before merging to main branch.

---

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [pytest Documentation](https://docs.pytest.org/)
- [pylint Documentation](https://pylint.pycqa.org/)
- [scikit-learn Documentation](https://scikit-learn.org/)
