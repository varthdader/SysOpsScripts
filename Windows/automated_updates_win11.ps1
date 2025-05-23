<# Script: automated_updates_win11.ps1
A PowerShell script to automate Windows 11 updates
Author: VarthDader (https://github.com/varthdader)
#>

# Function to check for updates
function Check-ForUpdates {
    Write-Host "Checking for updates..."
    $updates = Get-WindowsUpdate -AcceptAll -AutoReboot -ErrorAction Stop
    return $updates
}

# Function to install updates
function Install-Updates {
    Write-Host "Installing updates..."
    Install-WindowsUpdate -AcceptAll -AutoReboot -ErrorAction Stop
}

# Run the update check and installation
try {
    $updates = Check-ForUpdates
    if ($updates) {
        Install-Updates
        Write-Host "Updates installed successfully."
    } else {
        Write-Host "No updates available."
    }
} catch {
    Write-Host "An error occurred: $_"
}
