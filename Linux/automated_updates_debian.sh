#!/bin/sh

#----------------------------------------------------------------------
#       Upgrade All The Things (for Debian)
#
# Copyright 2015 Varth Dader
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#----------------------------------------------------------------------

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
