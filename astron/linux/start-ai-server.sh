#!/bin/sh
cd ../..

# Define some constants for our AI server:
MAX_CHANNELS=999999
STATESERVER=4002
ASTRON_IP="127.0.0.1:7199"
EVENTLOGGER_IP="127.0.0.1:7197"

# Get the user input:
read -p "District name (DEFAULT: NuttyCity): " DISTRICT_NAME
DISTRICT_NAME=${DISTRICT_NAME:-NuttyCity}
read -p "Base channel (DEFAULT: 401000000): " BASE_CHANNEL
BASE_CHANNEL=${BASE_CHANNEL:-401000000}

echo "==============================="
echo "Starting Operation Toontown AI server..."
echo "District name: Nutty City"
echo "Base channel: $BASE_CHANNEL"
echo "Max channels: $MAX_CHANNELS"
echo "State Server: $STATESERVER"
echo "Astron IP: $ASTRON_IP"
echo "Event Logger IP: $EVENTLOGGER_IP"
echo "==============================="

while [ true ]
do
    /usr/bin/python2 -m toontown.ai.ServiceStart --base-channel $BASE_CHANNEL \
                     --max-channels $MAX_CHANNELS --stateserver $STATESERVER \
                     --astron-ip $ASTRON_IP --eventlogger-ip $EVENTLOGGER_IP \
                     --district-name $DISTRICT_NAME
done
