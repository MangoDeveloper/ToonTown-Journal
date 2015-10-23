#!/bin/bash
cd ..

# Get the user input:
read -p "Username: " TTRUsername
read -s -p "Password: " TTRPassword
echo
read -p "Gameserver (DEFAULT: 167.114.28.238): " TTR_GAMESERVER
TTR_GAMESERVER=${TTR_GAMESERVER:-"167.114.28.238"}

# Export the environment variables:
export TTRUsername=$TTRUsername
export TTRPassword=$TTRPassword
export TTR_PLAYTOKEN=$TTRUsername
export TTR_GAMESERVER=$TTR_GAMESERVER

echo "==============================="
echo "Starting Toontown Custom”
echo "Username: $TTRUsername"
echo "Gameserver: $TTR_GAMESERVER"
echo "==============================="

/usr/bin/python2 -m toontown.toonbase.ToontownStartRemoteDB
