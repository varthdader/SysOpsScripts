<#
Script Name: win_update_audit.ps1
This script will search a windows host for all missing updates and provide them in a list

NOTE:  This must be run in an elevated shell

SOURCE: https://raw.githubusercontent.com/wiltaylor/WindowsUpdate/master/Get-WindowsUpdate.ps1
#>

Set-ExecutionPolicy -ExecutionPolicy Unrestricted

# List out all missing updates
Write-Output "Creating Microsoft.Update.Session COM object" 
$session1 = New-Object -ComObject Microsoft.Update.Session -ErrorAction silentlycontinue

Write-Output "Creating Update searcher" 
$searcher = $session1.CreateUpdateSearcher()

Write-Output "Searching for missing updates..." 
$result = $searcher.Search("IsInstalled=0")

# List updates waiting to be installed 
$updates = $result.Updates;

Write-Output "Found $($updates.Count) updates!" 

$updates | Format-Table Title, AutoSelectOnWebSites, IsDownloaded, IsHiden, IsInstalled, IsMandatory, IsPresent, AutoSelection, AutoDownload -AutoSize

pause
