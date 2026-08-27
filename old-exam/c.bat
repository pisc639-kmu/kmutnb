@echo off
set "B=cp.py"

python "%B%" %*
if errorlevel 1 (
    echo Error occurred while running %B%: exit code %errorlevel%
    exit /b %errorlevel%
)