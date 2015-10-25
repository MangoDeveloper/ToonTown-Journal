@echo off
cd ..

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

rem Get the user input:
set /P ttjUsername="Username: "

rem Export the environment variables:
set TTJ_PLAYCOOKIE=%ttjUsername%
set TTJ_GAMESERVER=127.0.0.1

echo ===============================
echo Starting Toontown Infinite...
echo ppython: %PPYTHON_PATH%
echo Username: %ttjUsername%
echo Gameserver: %TTJ_GAMESERVER%
echo ===============================

%PPYTHON_PATH% -m toontown.toonbase.ClientStart
pause
