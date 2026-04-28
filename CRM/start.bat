@echo off
cd /d "%~dp0"
echo.
echo ======================================
echo   NBB CRM -- starter op...
echo ======================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
  echo FEJL: Python er ikke installeret.
  echo Hent det fra https://www.python.org og proev igen.
  echo Husk at saette hak ved "Add Python to PATH" under installation.
  pause
  exit /b 1
)

echo Installerer nodvendige pakker...
pip install -r requirements.txt -q

echo Klar -- aabner i browseren...
echo Stop: luk dette vindue eller tryk Ctrl+C
echo.

set DEMO=true
python app.py

pause
