@echo off
cd ..

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

rem Get the user input:
set /P ttrUsername="Username: "
set /P ttrPassword="Password: "
set TTR_GAMESERVER=107.173.88.117

rem Export the environment variables:

set TTR_PLAYTOKEN=%ttrUsername%:%ttrPassword%

echo ===============================
echo Starting Operation Toontown…
echo ppython: %PPYTHON_PATH%
echo Username: %ttrUsername%
echo Gameserver: %TTR_GAMESERVER%
echo ===============================

%PPYTHON_PATH% -m toontown.toonbase.ToontownStart
pause
