#!/bin/sh
cd ..

# Get the user input:
read -p "Username: " TTRUsername

# Export the environment variables:
export TTRUsername=$TTRUsername
export TTRPassword="password"
export TTR_PLAYTOKEN=$TTRUsername
export TTR_GAMESERVER="127.0.0.1"

echo "==============================="
echo "Starting Toontown Custom”
echo "Username: $TTRUsername"
echo "Gameserver: $TTR_GAMESERVER"
echo "==============================="

/usr/bin/python2 -m toontown.toonbase.ToontownStart
