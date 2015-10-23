@echo off


rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH


set TTR_GAMESERVER=23.92.65.229


%PPYTHON_PATH% -m toontown_launcher
pause
