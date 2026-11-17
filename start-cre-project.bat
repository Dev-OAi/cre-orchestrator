@echo off
title CRE Acquisition Orchestrator
cd /d "%~dp0"
echo ===================================================
echo   CRE Acquisition Orchestrator Launcher
echo   Configured Local Model: gemma4:e2b (Ollama)
echo ===================================================
echo.

:: Ensure environment variables are set
set "CRE_LLM_PROVIDER=ollama"
set "OLLAMA_MODEL=gemma4:e2b"
set "OLLAMA_HOST=http://127.0.0.1:11434"

:: Optional check if Ollama is running
curl -s -m 2 http://127.0.0.1:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Ollama is not responding on 127.0.0.1:11434.
    echo Please make sure Ollama is started.
    echo.
) else (
    echo [OK] Local Ollama service detected.
)

echo Starting dashboard and backend watcher...
cd dashboard
npm run dev
