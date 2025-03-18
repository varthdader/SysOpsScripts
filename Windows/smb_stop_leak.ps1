<# Script: smb_stop_leak.ps1
A PowerShell script that users Windows Firewall to block SMB calls outside of the local network range
Author: VarthDader (https://github.com/varthdader)
#>

# Define the local network range
$localNetwork = "192.168.1.0/24"  # Adjust this to your local network range

# Convert the local network range to an object
$localNetworkObject = New-NetIPAddress -IPAddress $localNetwork

# Create a firewall rule to block SMB traffic to external hosts
New-NetFirewallRule -DisplayName "Block SMB to External Hosts" `
    -Direction Outbound `
    -Protocol TCP `
    -LocalPort 445,139 `
    -Action Block `
    -RemoteAddress "0.0.0.0/0" `
    -Description "Blocks SMB communication to any hosts not on the local network"

# Allow SMB traffic to the local network
New-NetFirewallRule -DisplayName "Allow SMB to Local Network" `
    -Direction Outbound `
    -Protocol TCP `
    -LocalPort 445,139 `
    -Action Allow `
    -RemoteAddress $localNetworkObject.IPAddress `
    -Description "Allows SMB communication to the local network"


    
