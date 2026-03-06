@echo off
cd /d "%~dp0"
echo Starting Liana-KT Backend...
start http://127.0.0.1:8000
"c:\Users\poona\AppData\Local\Programs\Python\Python313\python.exe" -m uvicorn main:app --reload
pause
