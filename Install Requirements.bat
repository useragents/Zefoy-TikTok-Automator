@echo off
setlocal

py -m pip install -r "%~dp0requirements.txt"
if errorlevel 1 (
    echo.
    echo Failed to install requirements. Make sure Python and pip are installed.
    pause
    exit /b 1
)

echo.
echo Requirements installed successfully.
pause
