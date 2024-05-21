<# Script: tcp_win_capture.ps1
TCP Traffic Capture Powershell
Author: VarthDader (https://github.com/varthdader)
Function: This script will use the native functions on a Windows host to collect a packet capture as an .etl file.
It will then zip up the capture file and provide a final location of the capture.
#>
Write-Host -Fore Gray "------------------------------------------------------"
Write-Host -Fore Cyan "       TCP_Traffic_Capture.ps1"
Write-Host -Fore DarkCyan "       Written by: VarthDader"
Write-Host -Force Cyan "                        https://github.com/varthdader"
Write-Host -Fore Gray "------------------------------------------------------"

$env:HostIP = (Get-NetIPConfiguration | Where-Object { $_.IPv4DefaultGateway -ne $null -and $_.NetAdapter.Status -ne "Disconnected" }).IPv4Address.IPAddress
netsh trace start capture = yes	IPv4.Address=$env:HostIP tracefile=c:\\windows\\temp\\capture.etl
Start-Sleep 90 # Increase this value to capture more than 90 seconds
netsh trace stop
Compress-Archive -Path "c:\\windows\\temp\\capture.etl" -DestinationPath "c:\\windows\\temp\\capture.zip" -Force
Write-Host -Fore Red "------------------------------------------------------"
Write-Host -Fore Green "       Capture File Saved To: C:\Windows\Temp\capture.etl"
Write-Host -Fore Red "------------------------------------------------------"

#<# 2 Convert from .etl to .pcap
#
#Download the latest etl2pcapng from
#https://github.com/microsoft/etl2pcapng/releases
#
##>
#./etl2pcapng.exe C:\Windows\Temp\capture.etl C:\Windows\Temp\capture.pcap
