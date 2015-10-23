#!/bin/sh
cd `dirname $0`
cd ..


# Get the user input:
read -p "Username: " ttrUsername

# Export the environment variables:
export ttrUsername=$ttrUsername
export ttrPassword=$ttrPassword
export password=$ttrPassword
export TTR_PLAYTOKEN=$ttrUsername:$ttrPassword
export TTR_GAMESERVER="127.0.0.1"

echo "==============================="
echo "Starting Operation Toontown"
echo "Username: $ttrUsername"
echo "Gameserver: $TTR_GAMESERVER"
echo "==============================="

ppython -m toontown.toonbase.ToontownStart
