@echo off
title CRE Acquisition Orchestrator - Clean Boot Manager
cls

echo ====================================================
echo  CRE ACQUISITION ORCHESTRATOR - STANDALONE LAUNCHER
echo ====================================================
echo.

echo [Step 1/4] Killing stuck background processes and ghost nodes...
taskkill /f /im node.exe >nul 2>&1
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im opencode* >nul 2>&1
echo Done.
echo.

echo [Step 2/4] Clearing temporary background runtime cache logs...
if exist "%USERPROFILE%\.cache\opencode" (
    rmdir /s /q "%USERPROFILE%\.cache\opencode" >nul 2>&1
)
echo Done.
echo.

echo [Step 3/4] Initializing Backend Data API Server...
echo.
start "CRE-Orchestrator-Backend-Server" cmd /k "cd /d %~dp0 && npm --prefix dashboard run dev:server"

echo Waiting 5 seconds for network ports to stabilize...
timeout /t 5 /nobreak >nul

echo.
echo [Step 4/4] Initializing Visual Frontend UI Client...
echo.
start "CRE-Orchestrator-Frontend-Client" cmd /k "cd /d %~dp0 && npm --prefix dashboard run dev:client"

echo.
echo ====================================================
echo  BOOT SEQUENCE COMPLETE
echo ====================================================
echo  1. Your servers are spinning up in separate windows.
echo  2. Open your browser and go to: http://localhost:5173
echo  3. Close those terminal windows when you want to stop.
echo ====================================================
echo.
pause
