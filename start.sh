#!/bin/bash
# ===============================================
# Credit Risk Platform - Startup Script (Linux/Mac)
# ===============================================

echo ""
echo "==================================="
echo " Credit Risk Platform Launcher"
echo "==================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[1/5] Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment found"
fi

echo ""
echo "[2/5] Activating virtual environment..."
source venv/bin/activate

echo ""
echo "[3/5] Installing dependencies..."
pip install -r requirements.txt --quiet

echo ""
echo "[4/5] Verifying models are trained..."
if [ ! -f "models/trained/best_model_catboost.pkl" ]; then
    echo "! Models not found. Training now..."
    python src/feature_engineering.py
    python src/model_training.py
    python src/explainability.py
    python src/fairness_audit.py
    echo "✓ Models trained successfully"
else
    echo "✓ Models found"
fi

echo ""
echo "[5/5] Choose what to launch:"
echo ""
echo "  1. Streamlit Web App (Frontend)"
echo "  2. FastAPI Backend"
echo "  3. Both (Frontend + Backend)"
echo "  4. Run Tests"
echo "  5. Exit"
echo ""

read -p "Enter choice (1-5): " choice

case $choice in
    1)
        echo ""
        echo "Starting Streamlit Web App..."
        echo "Access at: http://localhost:8501"
        cd frontend
        streamlit run app.py
        ;;
    2)
        echo ""
        echo "Starting FastAPI Backend..."
        echo "Access at: http://localhost:8000/docs"
        cd api
        uvicorn main:app --reload --host 0.0.0.0 --port 8000
        ;;
    3)
        echo ""
        echo "Starting both services..."
        echo "Frontend: http://localhost:8501"
        echo "Backend: http://localhost:8000/docs"
        cd frontend
        streamlit run app.py &
        cd ../api
        uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
        wait
        ;;
    4)
        echo ""
        echo "Running tests..."
        pytest tests/ -v
        ;;
    5)
        echo ""
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid choice!"
        exit 1
        ;;
esac
