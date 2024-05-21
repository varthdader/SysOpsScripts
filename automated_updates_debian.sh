#!/bin/sh

#       Upgrade All The Things (for Debian)

#       Give a final warning
echo "This script will automatically install all available patches"
#read -p "If you are sure this is what you want Press [Enter] key to start [CTRL                                                                                                                                                             +C to quit]"
read -p "Press [Enter] key to start backup..."
echo "Let me update all the things!"

#       Paste Upgrade Steps Below
apt-get clean
apt-get autoclean
apt-get autoremove
apt-get update
apt-get -y upgrade
apt-get update
apt-get -y dist-upgrade
apt-get clean
apt-get autoclean
apt-get autoremove
apt-get update

#       Upgrade is done now prompt for reboot
echo "All done with the updates.."
while true; do
    read -p "Do you want me to reboot?" yn
    case $yn in
        [Yy]* ) reboot; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done
