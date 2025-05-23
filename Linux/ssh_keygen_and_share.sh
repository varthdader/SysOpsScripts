#!/bin/bash

# Script to generate a secure SSH key and upload it to a remote host for passwordless login.
# Usage: Modify the REMOTE_USER and REMOTE_HOST variables before running the script.
# This script checks for an existing SSH key, generates one if not present,
# and uploads the public key to the specified remote host.
# Author: VarthDader (https://github.com/varthdader)

# Variables
REMOTE_USER="your_username"    # Replace with your remote username
REMOTE_HOST="your_remote_host"  # Replace with your remote host
KEY_PATH="$HOME/.ssh/id_rsa"

# Generate SSH key if it doesn't exist
if [ ! -f "$KEY_PATH" ]; then
    echo "Generating SSH key..."
    ssh-keygen -t rsa -b 4096 -C "your_email@example.com" -f "$KEY_PATH" -N ""
else
    echo "SSH key already exists at $KEY_PATH"
fi

# Upload the public key to the remote host
echo "Uploading SSH key to $REMOTE_HOST..."
ssh-copy-id -i "${KEY_PATH}.pub" "${REMOTE_USER}@${REMOTE_HOST}"

# Test the SSH connection
echo "Testing SSH connection..."
ssh "${REMOTE_USER}@${REMOTE_HOST}" "echo 'SSH key is set up successfully!'"
