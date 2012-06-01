#!/bin/sh

if [ -f "/usr/bin/optimus" ]; then
    echo "Removing......"
    sudo rm -f /usr/bin/optimus
    sudo rm -f /usr/share/applications/bumblebee-optimus.desktop
else
    echo "Optimus isn't installed"
fi