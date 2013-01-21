#!/bin/sh

#Bumblebee Optimus Laucher Setup script
#Peter Nguyen

<<<<<<< HEAD
optimus="[Desktop Entry]\n
=======
kde="[Desktop Entry]\n
>>>>>>> 9fc8af7e67e2eba7144f67d305e296d4b0d76639
Type=Application\n
Encoding=UTF-8\n
Name=Bumblebee Optimus\n
Comment=Bumblebee Optimus\n
<<<<<<< HEAD
Exec=optimus\n
=======
Exec=kdesudo optimus\n
>>>>>>> 9fc8af7e67e2eba7144f67d305e296d4b0d76639
Icon=/usr/share/icons/optimus.png\n
Categories=System \n
X-Desktop-File-Install-Version=0.19"

<<<<<<< HEAD
=======
gnome="[Desktop Entry]\n
Type=Application\n
Encoding=UTF-8\n
Name=Bumblebee Optimus\n
Comment=Bumblebee Optimus\n
Exec=gksu optimus\n
Icon=/usr/share/icons/optimus.png\n
Categories=System\n
X-Desktop-File-Install-Version=0.19"

>>>>>>> 9fc8af7e67e2eba7144f67d305e296d4b0d76639
nvidia="[Desktop Entry]\n
Name=nvidia-settings\n
GenericName=Nvidia Settings\n
Comment=Nvidia Settings\n
<<<<<<< HEAD
Exec=optirun nvidia-settings -c :8\n
=======
Exec=nvidia-settings\n
>>>>>>> 9fc8af7e67e2eba7144f67d305e296d4b0d76639
Icon=nvidia-current-settings.png\n
Terminal=false\n
Type=Application\n
Categories=System"

setup(){

<<<<<<< HEAD
	if [ -f "/usr/bin/optimus" ]; then
		echo "Update bumblebee optimus...."
	else
		echo "Install bumblebee optimus....."
	fi

	cp -Rv optimus.py /usr/bin/optimus #install optimus
	chgrp bumblebee /usr/bin/optimus
	chgrp -R bumblebee /usr/share/applications
	chmod -R g+w /usr/share/applications
	chmod g+x /usr/bin/optimus
	
	echo -e $optimus > /usr/share/applications/bumblebee_optimus.desktop
	
	cp -Rv optimus.png /usr/share/icons
	
	echo -e $nvidia > /usr/share/applications/nvidia-settings.desktop
	
	if [ ! -f "/etc/bumblebee/bumblebee_database" ]; then
		echo -e "#Database\n@False\nnvidia-settings" > /etc/bumblebee/bumblebee_database
	fi
	chgrp bumblebee /etc/bumblebee/bumblebee_database
	chmod 760 /etc/bumblebee/bumblebee_database
	
	sleep 1
	echo "Done."
	echo "If you want to increase performance of nvidia, install primus"
=======
      if [ -f "/usr/bin/optimus" ]; then
	  echo "Update bumblebee optimus...."
      else
	  echo "Install bumblebee optimus....."
      fi

      sudo cp -Rv optimus.py /usr/bin/optimus #install optimus
      sudo chmod u+x /usr/bin/optimus
    
      if [ -f "/usr/bin/kdesudo" ]; then
	  sudo echo -e $kde > /usr/share/applications/bumblebee_optimus.desktop
      elif [ -f "/usr/bin/gksu" ]; then
	  sudo echo -e $gnome > /usr/share/applications/bumblebee_optimus.desktop
      fi
      
      sudo cp -Rv optimus.png /usr/share/icons
      
      if [ -f "/usr/share/applications/nvidia-settings.desktop" ]; then
	    echo "###"
      else
	    sudo echo -e $nvidia > /usr/share/applications/nvidia-settings.desktop
      fi
      sleep 1
      echo "Done."
>>>>>>> 9fc8af7e67e2eba7144f67d305e296d4b0d76639
}

remove(){

<<<<<<< HEAD
	echo "Checking optimus..."
	sleep 3
	if [ -f "/usr/bin/optimus" ]; then
		echo "Removing......"
		rm -f /usr/bin/optimus 
		rm -f /usr/share/applications/bumblebee-optimus.desktop
		for file in $(find /usr/share/applications/ -name *.desktop.save); do #restore file
			mv $file ${file%.*}
		done
		chgrp -R root /usr/share/applications
		chown -R root /usr/share/applications
		chmod -R g-w /usr/share/applications
		rm -f /usr/share/icons/optimus.png
		rm -f /usr/share/applications/*.desktop.optimus
		rm -f /etc/bumblebee/bumblebee_database
		echo "Done."
	else
		echo "Optimus isn\'t installed"
	fi
=======
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
      echo "Done."
    else
      echo "Optimus isn\'t installed"
    fi
    
>>>>>>> 9fc8af7e67e2eba7144f67d305e296d4b0d76639
}


# Main Control
echo "Checking bumblebee....."
sleep 3
if [ -f "/usr/bin/optirun" ]; then
<<<<<<< HEAD
	echo "Bumblebee was installed."
	sleep 1
	if [ -f "/usr/bin/optimus" ]; then
		echo "Bumblebee Optimus Laucher was installed."
		menu="1 - Update Bumblebee Optimus Laucher"
	else
		menu="1 - Setup Bumblebee Optimus Laucher"
	fi
	sleep 1
	echo "#####################################"
	echo $menu
	echo "2 - Remove Bumblebee Optimus Laucher"
	echo "3 - Quit"
	echo "#####################################"
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
=======
   echo "Bumblebee was installed."
   sleep 1
   if [ -f "/usr/bin/optimus" ]; then
	echo "Bumblebee Optimus Laucher was installed."
	menu="1 - Update Bumblebee Optimus Laucher"
   else
	menu="1 - Setup Bumblebee Optimus Laucher"
   fi
   sleep 1
   echo "#####################################"
   echo $menu
   echo "2 - Remove Bumblebee Optimus Laucher"
   echo "3 - Quit"
   echo "#####################################"
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
>>>>>>> 9fc8af7e67e2eba7144f67d305e296d4b0d76639
fi