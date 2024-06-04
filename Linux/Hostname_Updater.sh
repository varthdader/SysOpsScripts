#!/bin/bash

#----------------------------------------------------------------------
#       Local Host Updater (for Debian)
#
# Copyright 2021 Varth Dader
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

# This script will read hostnames from target.hosts.txt and add them to the local /etc/hosts file
# This is useful for testing environments when targets are not found in a DNS server

# Root Check
if [ "$EUID" -ne 0 ]; then
    echo "This script must be run as root. Please use sudo."
    exit 1
fi

# Read hostnames from the file
while IFS= read -r line; do

# Split the line into ipaddress and hostname
  ipaddress=$(echo $line | cut -d ' ' -f1)
  hostname=$(echo $line | cut -d ' ' -f2-)

# Add the hostname to /etc/hosts
  echo "Adding $hostname to /etc/hosts"
  echo "$ipaddress   $hostname" >> /etc/hosts
done < target.hosts.txt

# Zero out the list to avoid duplicates
echo "" > target.hosts.txt

## Tip: Quickly add your hostnames like so 
##         echo "1.1.1.1 random.hostname" >> target.hosts.txt
## Tip2: Try to run this as a cron job to allow it to update in the background
