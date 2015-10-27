@echo off
cd ..

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

rem Get the user input:
set /P ttjUsername="Username: "
set TTJ_GAMESERVER=167.114.28.238

rem Export the environment variables:
set TTJ_PLAYCOOKIE=%ttjUsername%

echo ===============================
echo Starting Toontown Journey...
echo ppython: %PPYTHON_PATH%
echo Username: %ttjUsername%
echo Gameserver: %TTJ_GAMESERVER%
echo ===============================

%PPYTHON_PATH% -m toontown.toonbase.ClientStart
pause
