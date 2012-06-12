#!/bin/sh

echo "Checking bumblebee....."
sleep 3
if [ -f "/usr/bin/optirun" ]; then
    echo "Bumblebee was installed"
    sleep 1
    if [ -f "/usr/bin/optimus" ]; then
	echo "Update bumblebee optimus...."
    else
	echo "Install bumblebee optimus....."
    fi

    sudo cp -Rv optimus.py /usr/bin/optimus
    sudo chmod o+x /usr/bin/optimus
    
    if [ -f "/usr/bin/kdesu" ]; then
	sudo cp -Rv bumblebee-optimus.desktop.kde /usr/share/applications/bumblebee-optimus.desktop
    fi
    
    if [ -f "/usr/bin/gtksu" ]; then
	sudo cp -Rv bumblebee-optimus.desktop.gtk /usr/share/applications/bumblebee-optimus.desktop
    fi
    
    sudo cp -Rv optimus.png /usr/share/icons
    sleep 1
    echo "Done."
else
    echo "Bumblebee isn't installed. Please install now."
fi