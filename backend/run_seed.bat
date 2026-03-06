@echo off
cd /d "%~dp0\.."
echo Seeding Database for Liana-KT...
"c:\Users\poona\AppData\Local\Programs\Python\Python313\python.exe" -m backend.seed
if %errorlevel% neq 0 (
    echo Seeding Failed!
) else (
    echo Seeding Complete!
)
pause
