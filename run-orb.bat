@echo off
REM Testlauncher: erzwingt den prozeduralen Orb, egal was in chappie.toml steht.
set CHAPPIE_ORB_STYLE=orb
call "%~dp0run.bat" %*
