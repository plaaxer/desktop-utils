#!/bin/bash

ARG=$1

# use off to kill
if [[ "$ARG" == "off" || "$ARG" == "stop" ]]; then
    echo "Turning off live wallpaper..."
    killall linux-wallpaperengine 2>/dev/null
    exit 0
fi

if [ -z "$ARG" ]; then
    echo "Lock in g - you forgot the ID."
    echo "Usage: ./set_wall.sh <WALLPAPER_ID> (or './set_wall.sh off' to stop)"
    exit 1
fi

echo "Loading wallpaper $ARG..."

# killing old background
killall linux-wallpaperengine 2>/dev/null
sleep 1

# yeah i just access my windows steam library, whatever
/opt/linux-wallpaperengine/linux-wallpaperengine \
  --assets-dir "/media/plaxer/WdBlack1Tb/SteamLibrary/steamapps/common/wallpaper_engine/assets" \
  --window 0x0x1920x1080 \
  --bg "/media/plaxer/WdBlack1Tb/SteamLibrary/steamapps/workshop/content/431960/$ARG" > /dev/null 2>&1 &

sleep 3

xprop -name "wallpaperengine" -f _NET_WM_WINDOW_TYPE 32a -set _NET_WM_WINDOW_TYPE _NET_WM_WINDOW_TYPE_DESKTOP

wmctrl -r "wallpaperengine" -b add,below

echo "Done, enjoy your pseudo-wallpaper"
