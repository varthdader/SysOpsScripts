### Create Scheduled Task on Remote Host
To set up the PowerShell script as a scheduled task on a remote host named BEEFY1, follow these steps:

Prerequisites
Remote Management: Ensure that PowerShell Remoting is enabled on BEEFY1. You can enable it by running the following command in an elevated PowerShell session on BEEFY1:

```
Enable-PSRemoting -Force
```
Permissions: Ensure that you have administrative privileges on the remote host and have access to the file path where the script will be stored.

Steps to Create the Scheduled Task
Copy the Script to the Remote Host:
Use Copy-Item to transfer the script to the remote machine. Replace C:\Path\To\YourScript.ps1 with the actual path of your script.

```
Copy-Item -Path "C:\Path\To\YourScript.ps1" -Destination "\\BEEFY1\C$\Path\To\YourScript.ps1"
```
Create the Scheduled Task:
Use the following PowerShell command to create the scheduled task on the remote host. This command connects to BEEFY1 and sets up the task to run the script. Replace the paths accordingly.

```
Invoke-Command -ComputerName BEEFY1 -ScriptBlock {
    $action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-NoProfile -File 'C:\Path\To\YourScript.ps1'"
    $trigger = New-ScheduledTaskTrigger -AtStartup
    $trigger.Repetition.Interval = (New-TimeSpan -Minutes 5)  # Adjust as needed
    $trigger.Repetition.Duration = (New-TimeSpan -Days 1)  # Repeat for 1 day
    $taskSettings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

    Register-ScheduledTask -Action $action -Trigger $trigger -Settings $taskSettings -TaskName "MonitorLoginAttempts" -Description "Monitors login attempts and alerts on failures." -User "SYSTEM" -RunLevel Highest
}
```
Summary
Copy the script to the remote host.
Create the scheduled task using Invoke-Command.
Notes
Ensure that the paths used in the script and the scheduled task creation command are correct.
You may need to adjust firewall settings to allow for PowerShell Remoting.
If you have any questions or need further assistance, feel free to ask!

### Remove A Scheduled Task on Remote Host
To remove the previously created scheduled task named "MonitorLoginAttempts" on the remote host BEEFY1, you can use the following PowerShell command:

```
Invoke-Command -ComputerName BEEFY1 -ScriptBlock {
    Unregister-ScheduledTask -TaskName "MonitorLoginAttempts" -Confirm:$false
}
```

### Check Scheduled Task Status
```
Invoke-Command -ComputerName BEEFY1 -ScriptBlock {
    Get-ScheduledTask -TaskName "MonitorLoginAttempts"
}
```
Additional Details
Task Overview: The command will return details about the scheduled task, including its status, triggers, and actions.

Check Task History: If you want to see the history of the task's runs, you can use:

```
Invoke-Command -ComputerName BEEFY1 -ScriptBlock {
    Get-ScheduledTaskInfo -TaskName "MonitorLoginAttempts"
}
```

### Manually Start the Scheduled Task
```
Invoke-Command -ComputerName BEEFY1 -ScriptBlock {
    Start-ScheduledTask -TaskName "MonitorLoginAttempts"
}
```
