@echo off
REM Personal Chappie — Dev-Launcher (Phase 1a)
REM Startet Frontend (Vite HMR) + Backend (FastAPI --dev) parallel.
REM Fenster erscheint sobald beide healthy sind.

setlocal EnableDelayedExpansion
cd /d "%~dp0"

if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

REM 1) Frontend-Dev-Server in eigenem Fenster.
REM    Port 5173 (Vite default). Wird in chappie.toml ui.vite_dev_url erwartet.
pushd chappie\ui\web\frontend
if not exist node_modules (
    echo [dev] node_modules fehlt — npm install...
    call npm install || goto :error
)
start "chappie-vite" cmd /k npm run dev
popd

REM 2) Kurzer Buffer damit Vite binden kann bevor pywebview die URL lädt.
timeout /t 2 /nobreak >nul

REM 3) Backend + Fenster im Foreground (Console-Output sichtbar).
set CHAPPIE_DEV=1
set CHAPPIE_WEBVIEW_DEBUG=1
python -m chappie.ui.web.launcher --dev %*

goto :end

:error
echo [dev] Abbruch — npm install fehlgeschlagen.
exit /b 1

:end
endlocal
