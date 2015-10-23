#!/bin/sh
cd ..

export DYLD_LIBRARY_PATH=`pwd`/Libraries.bundle
export DYLD_FRAMEWORK_PATH="Frameworks"

# Get the user input:
read -p "Username: " ttrUsername
read -s -p "Password: " ttrPassword
echo
read -p "Gameserver (DEFAULT: 167.114.28.238): " TTR_GAMESERVER
TTR_GAMESERVER=${TTR_GAMESERVER:-"167.114.28.238"}

# Export the environment variables:
export ttrUsername=$ttrUsername
export ttrPassword=$ttrPassword
export TTR_PLAYTOKEN=$ttrUsername
export TTR_GAMESERVER=$TTR_GAMESERVER

echo "==============================="
echo "Starting Operation Toontown”
echo "Username: $ttrUsername"
echo "Gameserver: $TTR_GAMESERVER"
echo "==============================="

ppython -m toontown.toonbase.ToontownStartRemoteDB
