@echo off
setlocal
title Launch CRE Acquisition Orchestrator (Ollama 32k)

echo =======================================================
echo   Launching CRE Acquisition Orchestrator
echo   Engine: Local Ollama (gemma4-32k:latest)
echo =======================================================

cd /d "%~dp0"

:: Set local LLM environment variables
set CRE_LLM_PROVIDER=ollama
set OLLAMA_HOST=http://127.0.0.1:11434
set OLLAMA_MODEL=gemma4-32k:latest
set CRE_AGENT_CONVERSATIONS=1

echo Starting dashboard and server services...
start "CRE Orchestrator Server" cmd /k "npm run dev"

echo Waiting 4 seconds for Vite and backend watcher to bind...
timeout /t 4 /nobreak >nul

echo Opening browser at http://localhost:5173/
start http://localhost:5173/

echo.
echo Dashboard launched in browser.
echo You can also test agent workflows directly via:
echo   python scripts/run_local_agent.py
echo.
pause
