#!/bin/sh

if [ -f "/usr/bin/optirun" ]; then 
    echo "Bumblebee was installed"
    echo "Install bumblebee optimus"
    sudo cp -Rv optimus.py /usr/bin/optimus
    sudo chmod o+x /usr/bin/optimus
    sudo cp -Rv bumblebee-optimus.desktop /usr/share/applications/
    
else
    echo "Bumblebee isn't installed. Please install now."
fi