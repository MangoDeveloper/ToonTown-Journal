#!/bin/sh
cd ..

# Get the user input:
read -p "Username: " ttjUsername
read -s -p "Password: " ttjPassword
TTJ_GAMESERVER="158.69.209.131"

# Export the environment variables:
export ttjUsername=$ttjUsername
export ttjPassword=$ttjPassword

export TTJ_PLAYCOOKIE=$ttjUsername:$ttjPassword
export TTJ_GAMESERVER=$TTJ_GAMESERVER

echo "==============================="
echo "Starting Toontown Journey..."
echo "Username: $ttjUsername"
echo "Gameserver: $TTJ_GAMESERVER"
echo "==============================="

ppython -m toontown.toonbase.ClientStart
