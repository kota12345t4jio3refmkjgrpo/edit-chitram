@echo off
REM One-step installer for the edit-chitram Claude Code skill (Windows).
REM Usage: unzip edit-chitram.zip, open the edit-chitram folder, double-click install.bat
setlocal
set "SRC=%~dp0"
set "DEST=%USERPROFILE%\.claude\skills\edit-chitram"
echo ==^> Installing edit-chitram skill to %DEST%
if not exist "%USERPROFILE%\.claude\skills" mkdir "%USERPROFILE%\.claude\skills"
if /I not "%SRC%"=="%DEST%\" (
  if exist "%DEST%" (echo !! %DEST% already exists ^(it may hold your learned style^). Move it away first, then run again. & pause & exit /b 1)
  xcopy "%SRC%" "%DEST%\" /E /I /Q /Y >nul
)
cd /d "%DEST%"
where node >nul 2>nul || (echo !! Node.js 18+ is required: https://nodejs.org & pause & exit /b 1)
where ffmpeg >nul 2>nul || echo !! ffmpeg not found - install it: winget install Gyan.FFmpeg
echo ==^> Installing renderer (Playwright + Chromium)
call npm install --silent
call npx playwright-core install chromium
echo ==^> Installing Python packages
python -m pip install --user numpy scipy pillow opencv-python-headless soundfile >nul 2>nul || py -m pip install --user numpy scipy pillow opencv-python-headless soundfile >nul 2>nul || echo !! pip install failed - run: pip install numpy scipy pillow opencv-python-headless soundfile
echo ==^> Installing footage tools (transcription + cut-outs)
python -m pip install --user faster-whisper "rembg[cpu]" >nul 2>nul || py -m pip install --user faster-whisper "rembg[cpu]" >nul 2>nul || echo !! optional: pip install faster-whisper rembg[cpu]  (needed for footage edits)
echo.
echo Done. Restart Claude Code, give it 10-12 of your videos and say: "learn my style".
pause
