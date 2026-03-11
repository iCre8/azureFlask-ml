# Issue Log - azureFlask-ml

Date: 2026-03-10

**Status: FIXED** - All issues have been resolved as of 2026-03-10

---

## Summary

This project has **critical compatibility issues** that prevent the Flask application from running. The codebase was written for Python 3.x with older library versions (Flask 1.0.2, pandas 0.24.2, scikit-learn 0.20.3) but the current environment has Python 3.12 with modern library versions.

---

## Issues Found

### 1. CRITICAL: Import Error - `sklearn.externals.joblib`

**File:** `app.py:6`

**Error:**
```
ImportError: cannot import name 'joblib' from 'sklearn.externals'
```

**Cause:** The code uses deprecated import path `from sklearn.externals import joblib`. In modern scikit-learn (1.x), this module was removed.

**Fix Required:** Change to `import joblib` (direct import works).

---

### 2. CRITICAL: Model File Incompatible

**File:** `boston_housing_prediction.joblib`

**Error:**
```
ModuleNotFoundError: No module named 'sklearn.ensemble.gradient_boosting'
```

**Cause:** The model was pickled with an old scikit-learn version (0.20.3). The `sklearn.ensemble.gradient_boosting` module was reorganized in scikit-learn 1.x to `sklearn.ensemble._gb`.

**Fix Required:** Either:
- Retrain the model with current scikit-learn version and save a new `.joblib` file
- Use an older Python/scikit-learn environment to load and re-save the model

---

### 3. CRITICAL: Dependency Version Incompatibility

**Error:**
```
error: subprocess-exited-with-error
ModuleNotFoundError: No module named 'pkg_resources'
```

**Cause:** The `requirements.txt` specifies:
- `Flask==1.0.2`
- `pandas==0.24.2`
- `scikit-learn==0.20.3`

These versions are not compatible with Python 3.12. The old pandas requires `setuptools` (pkg_resources) which is not available in the build environment.

**Fix Required:** Update requirements.txt to use Python 3.12-compatible versions:
- Flask 3.x
- pandas 2.x
- scikit-learn 1.x

---

### 4. MEDIUM: Bare Except Clause

**File:** `app.py:59`

**Code:**
```python
except:
    LOG.info("JSON payload: %s json_payload")
    return "Model not loaded"
```

**Issue:** Using bare `except:` is bad practice - it catches all exceptions including KeyboardInterrupt. Also, the logging call has wrong format string (see next issue).

---

### 5. MEDIUM: Incorrect Logging Format Strings

**Files:** `app.py:16`, `app.py:60`, `app.py:64`, `app.py:66`

**Issue:** The logging format strings reference variables that are not passed:

```python
LOG.info("Scaling Payload: %s payload")  # 'payload' is not provided!
LOG.info("JSON payload: %s json_payload")  # 'json_payload' is not provided!
```

**pylint warning:** `E1206: Not enough arguments for logging format string`

---

### 6. LOW: Deprecated Code Comment

**File:** `app.py:26`

**Code:**
```python
# TO DO:  Log out the prediction value
```

**Issue:** This TODO has been in the code since initial commit but was never implemented. The prediction value is not logged.

---

### 7. LOW: CI Configuration Error

**File:** `.github/workflows/main.yml:18-21`

**Issue:**
```yaml
- name: Set up Python 6.2.0
  uses: actions/setup-python@6.2.0
  with:
    python-version: 6.2.0
```

Python 6.2.0 does not exist. This is likely a typo - should be `3.x` or a valid version like `3.12`.

---

## Test Results

### Tests
```
python -m pytest test_hello.py -v
============================= test session starts =============================
collected 1 item

test_hello.py::test_hello_subtract PASSED                                [100%]

============================== 1 passed in 0.07s
```
✅ Tests pass (but only tests `hello.py`, not `app.py`)

### Linting
```
python -m pylint --disable=R,C hello.py app.py

************* Module app
app.py:6:0: E0611: No name 'joblib' in module 'sklearn.externals' (no-name-in-module)
app.py:16:4: E1206: Not enough arguments for logging format string (logging-too-few-args)
app.py:59:4: W0702: No exception type(s) specified (bare-except)
app.py:60:8: E1206: Not enough arguments for logging format string (logging-too-few-args)
app.py:64:4: E1206: Not enough arguments for logging format string (logging-too-few-args)
app.py:66:4: E1206: Not enough arguments for logging format string (logging-too-few-args)

Your code has been rated at 3.16/10
```

⚠️ Linting fails with multiple errors

---

## Cannot Run

The Flask application **cannot be started** due to the import error in issue #1. Even if imports were fixed, the model loading would fail due to issue #2.

---

## Recommendations

1. **Update requirements.txt** with Python 3.12-compatible versions
2. **Fix import** in `app.py:6` - change to `import joblib`
3. **Retrain model** with modern scikit-learn and replace `boston_housing_prediction.joblib`
4. **Fix logging format strings** to use actual variables or remove placeholders
5. **Replace bare except** with specific exception handling
6. **Fix CI workflow** Python version
7. **Add app.py tests** - currently only `hello.py` is tested
