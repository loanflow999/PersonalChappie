@echo off
REM Testlauncher: startet Chappie explizit mit SWG/Gigi-Maskottchen.
REM Ueberschreibt die chappie.toml-Einstellung [ui].orb_style fuer diese Session.
set CHAPPIE_ORB_STYLE=mascot
call "%~dp0run.bat" %*
