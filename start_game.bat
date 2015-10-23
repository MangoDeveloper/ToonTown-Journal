@echo off
cd

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

rem Get the user input:
set /P ttrUsername="Username: "
set /P TTR_GAMESERVER="Gameserver (DEFAULT: 192.168.1.7): " || ^
set TTR_GAMESERVER=23.92.65.229

rem Export the environment variables:
set ttrPassword=password
set TTR_PLAYTOKEN=%ttrUsername%

echo ===============================
echo Starting Operation Toontown…
echo ppython: %PPYTHON_PATH%
echo Username: %ttrUsername%
echo Gameserver: %TTR_GAMESERVER%
echo ===============================

%PPYTHON_PATH% -m toontown.toonbase.ToontownStart
pause
