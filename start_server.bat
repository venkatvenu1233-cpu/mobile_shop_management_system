@echo off
cd /d "c:\xampp\htdocs\mobile engineer"
echo Starting Mobile Engineer Web Server...
echo Please wait a moment for the server to start...
echo.
echo Server will be available at: http://127.0.0.1:5000
echo Press Ctrl+C to stop the server
echo.

"C:\Program Files (x86)\Python314-32\python.exe" app.py

pause
