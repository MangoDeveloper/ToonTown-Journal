#!/bin/sh
cd ..

# Get the user input:
read -p "Username: " ttrUsername
read -p "Gameserver (DEFAULT: 192.168.1.7): " TTR_GAMESERVER
TTR_GAMESERVER=${TTR_GAMESERVER:-"167.114.28.238"}

# Export the environment variables:
export ttrUsername=$ttrUsername
export ttrPassword="password"
export TTR_PLAYTOKEN=$ttrUsername
export TTR_GAMESERVER=23.92.65.229

echo "==============================="
echo "Starting Toontown Custom"
echo "Username: $ttrUsername"
echo "Gameserver: $TTR_GAMESERVER"
echo "==============================="

/usr/bin/python2 -m toontown.toonbase.ToontownStart
