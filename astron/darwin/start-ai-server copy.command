#!/bin/sh
cd `dirname $0`
cd /Users/mgracer48/Desktop/Toontown-United


# Define some constants for our AI server:
MAX_CHANNELS=999999
STATESERVER=4002
ASTRON_IP="127.0.0.1:7199"
EVENTLOGGER_IP="127.0.0.1:7197"
export BASE_CHANNEL=403000000
export DISTRICT_NAME=Test
# Get the user input:

echo "==============================="
echo "Starting Toontown Custom AI server..."
echo "District name: Test"
echo "Base channel: 401000001"
echo "Max channels: $MAX_CHANNELS"
echo "State Server: $STATESERVER"
echo "Astron IP: $ASTRON_IP"
echo "Event Logger IP: $EVENTLOGGER_IP"
echo "==============================="

while [ true ]
do
    ppython -m toontown.ai.ServiceStart --base-channel $BASE_CHANNEL \
                     --max-channels $MAX_CHANNELS --stateserver $STATESERVER \
                     --astron-ip $ASTRON_IP --eventlogger-ip $EVENTLOGGER_IP \
                     --district-name $DISTRICT_NAME
done
