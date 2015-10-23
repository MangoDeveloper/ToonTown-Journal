#!/bin/sh
cd `dirname $0`
cd ..


# Get the user input:
read -p "Username: " ttrUsername
read -p "Password: " ttrPassword
read -p "Gameserver (DEFAULT:  107.173.88.117): " TTR_GAMESERVER
TTR_GAMESERVER=${TTR_GAMESERVER:-"107.173.88.117"}

# Export the environment variables:
export ttrUsername=$ttrUsername
export TTR_GAMESERVER=$TTR_GAMESERVER
export ttrPassword=$ttrPassword
export password=$ttrPassword
export TTR_PLAYTOKEN=$ttrUsername:$ttrPassword

echo "==============================="
echo "Starting Operation Toontown"
echo "Username: $ttrUsername"
echo "Gameserver: $TTR_GAMESERVER"
echo "==============================="

ppython -m toontown.toonbase.ToontownStart

