@echo off
echo Creating auto-start entry for Mobile Engineer Web Server...

REM Create a shortcut in the startup folder
set startup_folder=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set shortcut_path=%startup_folder%\Mobile Engineer Web Server.lnk
set target_path=c:\xampp\htdocs\mobile engineer\start_server.bat

echo Creating shortcut in startup folder...
echo Target: %target_path%
echo Shortcut: %shortcut_path%

REM Create VBS script to make shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%temp%\CreateShortcut.vbs"
echo sLinkFile = "%shortcut_path%" >> "%temp%\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%temp%\CreateShortcut.vbs"
echo oLink.TargetPath = "%target_path%" >> "%temp%\CreateShortcut.vbs"
echo oLink.WorkingDirectory = "c:\xampp\htdocs\mobile engineer" >> "%temp%\CreateShortcut.vbs"
echo oLink.Description = "Mobile Engineer Web Server" >> "%temp%\CreateShortcut.vbs"
echo oLink.Save >> "%temp%\CreateShortcut.vbs"

REM Execute the VBS script
cscript //nologo "%temp%\CreateShortcut.vbs"

REM Clean up
del "%temp%\CreateShortcut.vbs"

echo.
echo Auto-start shortcut created successfully!
echo The web server will automatically start when you log into Windows.
echo.
echo To remove auto-start, delete this file:
echo %shortcut_path%
echo.
pause
