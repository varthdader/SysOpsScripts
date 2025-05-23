###
#  __         ______     ______        __    __     ______     __   __     __     ______   ______     ______    
# /\ \       /\  __ \   /\  ___\      /\ "-./  \   /\  __ \   /\ "-.\ \   /\ \   /\__  _\ /\  __ \   /\  == \   
# \ \ \____  \ \ \/\ \  \ \ \__ \     \ \ \-./\ \  \ \ \/\ \  \ \ \-.  \  \ \ \  \/_/\ \/ \ \ \/\ \  \ \  __<   
#  \ \_____\  \ \_____\  \ \_____\     \ \_\ \ \_\  \ \_____\  \ \_\\"\_\  \ \_\    \ \_\  \ \_____\  \ \_\ \_\ 
#  \/_____/   \/_____/   \/_____/      \/_/  \/_/   \/_____/   \/_/ \/_/   \/_/     \/_/   \/_____/   \/_/ /_/ 

## Example: We monitor a flat log for for "Login Failed" events and report those to the local system logs                                                                                                            
##

# Define the path to the log files
# Define the path to the log files
$logPath = "C:\Application\Logs\LoginActivity.txt"
$exclusionFile = "C:\Application\Logs\excluded_events.txt"
$backupDir = "C:\Application\Logs\Backup"

# Create backup directory if it doesn't exist
if (-not (Test-Path $backupDir)) {
    New-Item -ItemType Directory -Path $backupDir
}

# Get the newest log file
$newestFile = Get-ChildItem -Path $logPath | Sort-Object LastWriteTime -Descending | Select-Object -First 1

if ($newestFile) {
    # Move the current log file to the backup location
    $backupFile = Join-Path -Path $backupDir -ChildPath $newestFile.Name
    Move-Item -Path $newestFile.FullName -Destination $backupFile -Force

    # Initialize a counter and read excluded events
    $eventCount = 0
    $excludedEvents = @{}

    if (Test-Path $exclusionFile) {
        $excludedEvents = Get-Content $exclusionFile | ForEach-Object { $_.Trim() }
    }

    # Read the log file and filter for "Access Denied:" events
    $events = Get-Content $backupFile | Where-Object {
        $_ -like "*Login Failed*" -and -not ($excludedEvents -contains $_)
    }

    # Output matching lines and count them
    foreach ($event in $events) {
        Write-Host $event
        $eventCount++

        # Add the event to the exclusion list if it's not already there
        if (-not ($excludedEvents -contains $event)) {
            Add-Content -Path $exclusionFile -Value $event
        }
    }

    # Only alert if more than 3 new events were found
    if ($eventCount -gt 3) {
        # Write to the system log
        $message = "A User has failed multiple login attempts"
        Write-EventLog -LogName Application -Source "Application" -EventId 1001 -EntryType Warning -Message $message
        
        # Output to terminal
        Write-Host "Alert: $message"
    }

    # Create a new empty log file in place of the moved log file
    New-Item -Path $newestFile.FullName -ItemType File -Force
} else {
    Write-Host "No log files found."
}
