@echo off
REM Check if venv exists
IF NOT EXIST venv (
    python -m venv venv
)

REM Activate venv
call venv\Scripts\activate

REM Install requirements
pip install --upgrade pip
pip install -r requirements.txt

REM Run main.py
python main.py

pause
