@echo off
title NIRIKSHAN - Digital Field Drug Testing Platform
echo =======================================================================
echo   NIRIKSHAN (निरीक्षण) - Digital Field Drug Testing & Intelligence Platform
echo   Narcotics Control Bureau (NCB) - Ministry of Home Affairs, Govt of India
echo   Problem Statement ID: 26231
echo =======================================================================
echo.
echo Initializing Local Platform Engine and SQLite Database...
echo Server URL: http://127.0.0.1:8000
echo.
timeout /t 2 >nul
start http://127.0.0.1:8000
py server.py
pause
