@echo off

echo ________________________Lazy Installer initianted________________________

set /p startQ = "Enter to start... "

rem Install packages through pip
pip install requests
pip install colorama

echo "Packages Installed! "
PAUSE
set /p path = "Enter the directory: "
cd %path%
py start.py


