# PowerShell script to replace the username in paths, then compress the modified path to a zip file.

# Prompt for the username
$Username = Read-Host "Enter the username"

# Define the base paths
$ChromeBasePath = "C:\Users\<username>\AppData\Local\Google\Chrome\User Data\Default"
$EdgeBasePath = "C:\Users\<username>\AppData\Local\Microsoft\Edge\User Data\Default"

# Replace <username> in the paths
$ChromePath = $ChromeBasePath -replace "<username>", $Username
$EdgePath = $EdgeBasePath -replace "<username>", $Username

# Output the username and modified paths
Write-Host "Username entered: $Username"
Write-Host "Chrome Path: $ChromePath"
Write-Host "Edge Path: $EdgePath"

# Define the path to be compressed (using Chrome path for this example, you can choose either or both)
$PathToCompress = $ChromePath

# Check if the path to compress exists
if (Test-Path -Path $PathToCompress) {
    Write-Host "Path to compress found: $PathToCompress"

    # Create the zip file name with username and timestamp
    $Timestamp = Get-Date -Format "yyyyMMddHHmmss"
    $ZipFileName = "$Username`_$Timestamp.zip"
    $ZipFilePath = Join-Path -Path (Split-Path -Path $PathToCompress -Parent) -ChildPath $ZipFileName

    Write-Host "Creating zip file: $ZipFilePath"

    # Compress the path into a zip file
    try {
        Compress-Archive -Path $PathToCompress -DestinationPath $ZipFilePath -Force
        Write-Host "Successfully created zip file: $ZipFilePath"
    }
    catch {
        Write-Error "Error creating zip file: $($_.Exception.Message)"
        exit
    }
}
else {
    Write-Error "Path to compress not found: $PathToCompress"
    exit
}

Write-Host "Script completed."
