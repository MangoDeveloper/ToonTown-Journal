#!/bin/sh
cd ..



# Get the user input:
read -p "Username: " ttiUsername

# Export the environment variables:
export ttiUsername=$ttiUsername
export TTI_PLAYCOOKIE=$ttiUsername
export TTI_GAMESERVER="127.0.0.1"

echo "==============================="
echo "Starting Toontown Infinite..."
echo "Username: $ttiUsername"
echo "Gameserver: $TTI_GAMESERVER"
echo "==============================="

ppython -m toontown.toonbase.ClientStart
