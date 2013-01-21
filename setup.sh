#!/bin/sh

#Bumblebee Optimus Laucher Setup script
#Peter Nguyen

optimus="[Desktop Entry]\n
Name=nvidia-settings\n
GenericName=Nvidia Settings\n
Comment=Nvidia Settings\n
Exec=optirun nvidia-settings -c :8\n
Exec=nvidia-settings\n
Icon=nvidia-current-settings.png\n
Terminal=false\n
Type=Application\n
Categories=System"

setup(){

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
}

remove(){
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
}


# Main Control
echo "Checking bumblebee....."
sleep 3
if [ -f "/usr/bin/optirun" ]; then
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
fi