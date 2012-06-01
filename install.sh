#!/bin/sh

echo "Checking bumblebee....."
sleep 3
if [ -f "/usr/bin/optirun" ]; then
    echo "Bumblebee was installed"
    sleep 1
    echo "Install bumblebee optimus....."
    sudo cp -Rv optimus.py /usr/bin/optimus
    sudo chmod o+x /usr/bin/optimus
    sudo cp -Rv bumblebee-optimus.desktop /usr/share/applications/
    sudo cp -Rv optimus.png /usr/share/icons
    sleep 1
    echo "Done."
else
    echo "Bumblebee isn't installed. Please install now."
fi