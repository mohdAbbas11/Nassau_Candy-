@echo off
echo ==============================================
echo Nassau Candy Distributor Optimization Project
echo ==============================================
echo.

echo 1. Generating mock data...
python generate_mock_data.py
if %ERRORLEVEL% neq 0 (
    echo Error generating data!
    exit /b %ERRORLEVEL%
)

echo.
echo 2. Training machine learning models...
python train_pipeline.py
if %ERRORLEVEL% neq 0 (
    echo Error training models!
    exit /b %ERRORLEVEL%
)

echo.
echo 3. Launching Streamlit Web Application...
python -m streamlit run app.py
