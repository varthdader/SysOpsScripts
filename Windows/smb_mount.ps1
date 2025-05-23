<#  Script Name: smb_mount.ps1
Script to mount an SMB shared volume with a user and password.
The password is called from a flat file and converted to a secure string before being stored into memory.
Author: VarthDader (https://github.com/varthdader)
#>

# Mandatory Banner
Write-Host 'Powershell' $PsVersionTable.PSVersion '-' (Get-date)
Write-Host 'Mounting SMB Share....'
Write-Host ''

# Path to password file
# (Should contain only 1 line with a clear text password, ACL rights should be used to limit file access)
$passwordFile = "C:\path\to\password.txt"

# Read password from file
$password = Get-Content $passwordFile | ConvertTo-SecureString

# Credentials
# Change domain\username to match the environment
$creds = New-Object System.Management.Automation.PSCredential ("domain\username", $password)

# Shared folder details
$shareName = "\\server\share"
$localPath = "C:\mount\point"

# Mount shared folder
New-PSDrive -Name X -PSProvider FileSystem -Root $shareName -Credential $creds -Persist

# Check if mounted
Get-PSDrive X

# Unmount on exit
Register-PSSessionConfiguration -Name Microsoft.PowerShell -Force
Remove-PSDrive -Name X
