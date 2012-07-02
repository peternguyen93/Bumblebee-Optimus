#!/bin/sh

#Bumblebee Optimus Laucher Setup script
#Peter Nguyen

function setup(){

      if [ -f "/usr/bin/optimus" ]; then
	  echo "Update bumblebee optimus...."
      else
	  echo "Install bumblebee optimus....."
      fi

      sudo cp -Rv optimus.py /usr/bin/optimus #install optimus
      sudo chmod o+x /usr/bin/optimus
    
      if [ -f "/usr/bin/kdesu" ]; then
	  sudo cp -Rv bumblebee-optimus.desktop.kde /usr/share/applications/bumblebee-optimus.desktop #for KDE
      elif [ -f "/usr/bin/gksu" ]; then
	  sudo cp -Rv bumblebee-optimus.desktop.gtk /usr/share/applications/bumblebee-optimus.desktop #for Gnome
      fi
    
      sudo cp -Rv optimus.png /usr/share/icons
      sleep 1
      echo "Done."
}

function remove(){

    echo "Checking optimus..."
    sleep 3
    if [ -f "/usr/bin/optimus" ]; then
      echo "Removing......"
      sudo rm -f /usr/bin/optimus 
      sudo rm -f /usr/share/applications/bumblebee-optimus.desktop
      for file in $(sudo ls /usr/share/applications/*.desktop.save); do #restore file
	  sudo mv $file ${file%.*}
      done
      sudo rm -f /usr/share/icons/optimus.png
      sudo rm -f /usr/share/applications/*.desktop.optimus
      sudo rm -f /etc/bumblebee_database
      sudo rm -f /etc/bumblebee_optimus_setting
      echo "Done."
    else
      echo "Optimus isn\'t installed"
    fi
    
}


# Main Control
echo "Checking bumblebee....."
sleep 3
if [ -f "/usr/bin/optirun" ]; then
   echo "Bumblebee was installed"
   sleep 1
   echo "#############################"
   echo "1 - Setup Bumblebee Optimus Laucher"
   echo "2 - Remove Bumblebee Optimus Laucher"
   echo "3 - Quit"
   echo "#############################"
   echo -n "Choices : "; read x
   case "$x" in
      "1" )
	      echo "Setup starting..."
	      setup
	      ;;
      "2" )
	      echo "Removing..."
	      remove
	      ;;
      "3" )   exit 0 ;;
      * )     echo "Press 1 or 2 to choice options";;
   esac
else
   echo "Bumblebee isn't installed. Please install now."
fi