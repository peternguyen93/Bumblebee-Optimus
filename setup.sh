#!/bin/bash

#Bumblebee Optimus Laucher Setup script
#Peter Nguyen
database=/etc/bumblebee/optimus_Database.json
dbinfo="{\"status\": 0, \"apps\": []}"
optimus="[Desktop Entry]\r\n
Name=bumblebee-optimus\r\n
GenericName=Bumblebee Optimus\r\n
Comment=Bumblebee Optimus\r\n
Exec=optimus\r\n
Icon=optimus.png\r\n
Terminal=false\r\n
Type=Application\r\r\n
Categories=System"

setup(){
	if [ -f "/usr/bin/optimus" ]; then
		echo -e "\e[1;33m[+]\e[0m Update bumblebee optimus...."
	else
		echo -e "\e[1;33m[+]\e[0m Install bumblebee optimus....."
	fi
	
	echo -e "\e[1;33m[+]\e[0m Copying file:"
	cp -Rv optimus.py /usr/bin/optimus #install optimus
	chgrp bumblebee /usr/bin/optimus
	chgrp -R bumblebee /usr/share/applications #default link containts all application
	chmod -R g+r+w /usr/share/applications
	chmod g+x /usr/bin/optimus
	echo -e $optimus > /usr/share/applications/bumblebee_optimus.desktop
	cp -Rv optimus.png /usr/share/icons
	
	if [ ! -f $database ]; then
		echo -e "\e[1;33m[+]\e[0m Copying database file"
		echo -e $dbinfo > $database
	fi
	chgrp bumblebee $database
	chmod 666 $database
	echo -e "\e[1;33m[+]\e[0m Done."
	echo -e "\e[1;31m[!]\e[0m If you want to increase performance of nvidia, install primus"
}

remove(){
	echo -e "\e[1;33m[+]\e[0m Checking optimus..."
	if [ -f "/usr/bin/optimus" ]; then
		echo -e "\e[1;33m[+]\e[0m Removing......"
		rm -f /usr/bin/optimus 
		rm -f /usr/share/applications/bumblebee-optimus.desktop
		for file in $(find /usr/share/applications/ -name *.desktop.save); do #restore file
			sudo mv $file ${file%.*}
		done
		for file in $(find /usr/share/applications/ -name *.desktop.optimus); do #remove all file
			sudo rm $file
		done
		chgrp -R root /usr/share/applications
		chown -R root /usr/share/applications
		chmod -R g-w /usr/share/applications
		rm -f /usr/share/icons/optimus.png
		rm -f $database
		rm -f ~/.local/log/optimus_laucher.log
		echo -e "\e[1;33m[+]\e[0m Done."
	else
		echo -e "\e[1;31m[!]\e[0m Optimus isn\'t installed"
	fi
}


# Main Control
if [ $(id -u) -eq 0 ]; then
	echo -e "\e[1;33m[+]\e[0m Checking bumblebee....."
	if [ -f "/usr/bin/optirun" ]; then
		echo -e "\e[1;31m[!]\e[0m Bumblebee was installed."
		if [ -f "/usr/bin/optimus" ]; then
			echo -e "\e[1;31m[!]\e[0m Bumblebee Optimus Laucher was installed."
			menu="\e[1;32m1 - Update Bumblebee Optimus Laucher\e[0m"
		else
			menu="\e[1;32m1 - Setup Bumblebee Optimus Laucher\e[0m"
		fi
		echo -e "\e[1;32m#####################################\e[0m"
		echo -e $menu
		echo -e "\e[1;32m2 - Remove Bumblebee Optimus Laucher\e[0m"
		echo -e "\e[1;32m3 - Quit\e[0m"
		echo -e "\e[1;32m#####################################\e[0m"
		echo -e -n "\e[1;36mChoices : \e[0m"; read x
		case "$x" in
			"1" )
				echo -e "\e[1;33m[+]\e[0m Setup starting..."
				setup
				;;
			"2" )
				echo -e "\e[1;33m[+]\e[0m Remove App starting..."
				remove
				;;
			"3" )   exit 0 ;;
			* )     echo -e "\e[1;31m[!]\e[0m Press 1 or 2 to choice options";;
		esac
	else
			echo -e "\e[1;31m[!]\e[0m Bumblebee isn't installed. Please install now."
	fi
else
	echo -e "\e[1;31m[!]\e[0m You don't have permission to install."
fi