@echo off
title MOBILE ENGINEER - Working Server
color 0A
echo.
echo ====================================================
echo              MOBILE ENGINEER WEBSITE
echo ====================================================
echo.
echo Starting FIXED web server...
echo.
echo Your website will open at: http://localhost:5000
echo.
echo Google Search: "localhost 5000"
echo.
echo Press any key to start...
pause > nul
echo.
echo [STARTING SERVER]
cd /d "c:\xampp\htdocs\mobile engineer"
"C:\Program Files (x86)\Python314-32\python.exe" working_server.py
echo.
echo [SERVER STOPPED]
pause
