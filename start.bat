@echo off
echo ========================================
echo   AI URL Risk Analyzer - Starting...
echo ========================================
echo.

:: Activate virtual environment and run
call venv\Scripts\activate
python app.py

pause
