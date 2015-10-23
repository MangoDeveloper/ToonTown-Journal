@echo off
cd ..

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

rem Get the user input:
set /P ttiUsername="Username: "

rem Export the environment variables:
set ttiPassword=password
set TTR_PLAYTOKEN=%ttiUsername%
set TTR_GAMESERVER=127.0.0.1

echo ===============================
echo Starting Toontown Custom…
echo ppython: %PPYTHON_PATH%
echo Username: %ttiUsername%
echo Gameserver: %TTR_GAMESERVER%
echo ===============================

%PPYTHON_PATH% -m toontown.toonbase.ToontownStart
pause
