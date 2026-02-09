@echo off
REM ===============================================
REM Credit Risk Platform - Startup Script
REM ===============================================

echo.
echo ===================================
echo  Credit Risk Platform Launcher
echo ===================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [1/5] Creating virtual environment...
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment found
)

echo.
echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [3/5] Installing dependencies...
pip install -r requirements.txt --quiet

echo.
echo [4/5] Verifying models are trained...
if not exist "models\trained\best_model_catboost.pkl" (
    echo ! Models not found. Training now...
    python src\feature_engineering.py
    python src\model_training.py
    python src\explainability.py
    python src\fairness_audit.py
    echo ✓ Models trained successfully
) else (
    echo ✓ Models found
)

echo.
echo [5/5] Choose what to launch:
echo.
echo  1. Streamlit Web App (Frontend)
echo  2. FastAPI Backend
echo  3. Both (Frontend + Backend)
echo  4. Run Tests
echo  5. Exit
echo.

set /p choice="Enter choice (1-5): "

if "%choice%"=="1" (
    echo.
    echo Starting Streamlit Web App...
    echo Access at: http://localhost:8501
    cd frontend
    streamlit run app.py
)

if "%choice%"=="2" (
    echo.
    echo Starting FastAPI Backend...
    echo Access at: http://localhost:8000/docs
    cd api
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
)

if "%choice%"=="3" (
    echo.
    echo Starting both services...
    echo Frontend: http://localhost:8501
    echo Backend: http://localhost:8000/docs
    start cmd /k "cd frontend && streamlit run app.py"
    timeout /t 3
    start cmd /k "cd api && uvicorn main:app --reload --host 0.0.0.0 --port 8000"
    echo.
    echo Both services started in separate windows!
    pause
)

if "%choice%"=="4" (
    echo.
    echo Running tests...
    pytest tests\ -v
    echo.
    pause
)

if "%choice%"=="5" (
    echo.
    echo Goodbye!
    exit
)

pause
