#!/bin/sh
cd ..



# Get the user input:
read -p "Username: " ttjUsername

# Export the environment variables:
export ttjUsername=$ttjUsername
export TTJ_PLAYCOOKIE=$ttjUsername
export TTJ_GAMESERVER="127.0.0.1"

echo "==============================="
echo "Starting Toontown Infinite..."
echo "Username: $ttjUsername"
echo "Gameserver: $TTJ_GAMESERVER"
echo "==============================="

ppython -m toontown.toonbase.ClientStart
