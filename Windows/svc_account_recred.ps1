<# Script: svc_account_recred.ps1
A PowerShell script that changes the password for a named domain service account and updates the password stored in a SQL Server instance. 
Make sure to run this script with appropriate permissions.
Author: VarthDader (https://github.com/varthdader)
#>
# Modify Variables as Needed


$domainServiceAccount = "DOMAIN\ServiceAccount"  # Change to your service account
$newPassword = "NewP@ssword123!"                   # Change to your new password
$sqlServerInstance = "YourSqlServerInstance"       # Change to your SQL Server instance
$sqlDatabase = "YourDatabaseName"                  # Change to your database name

# Change the password for the domain service account
try {
    $securePassword = ConvertTo-SecureString $newPassword -AsPlainText -Force
    $credential = New-Object System.Management.Automation.PSCredential($domainServiceAccount, $securePassword)
    
    # Change password for the domain account
    Set-ADAccountPassword -Identity $domainServiceAccount -NewPassword $securePassword -Reset
    Write-Host "Password for $domainServiceAccount changed successfully."
} catch {
    Write-Host "Failed to change password for $domainServiceAccount: $_"
    exit 1
}

# Update the password in SQL Server
try {
    # Create SQL connection
    $connectionString = "Server=$sqlServerInstance;Database=$sqlDatabase;Integrated Security=True;"
    $sqlConnection = New-Object System.Data.SqlClient.SqlConnection($connectionString)
    $sqlConnection.Open()

    # Update the password in the relevant SQL Server configuration table
    $updateQuery = "UPDATE dbo.ServiceAccounts SET Password = @newPassword WHERE AccountName = @accountName"
    $sqlCommand = $sqlConnection.CreateCommand()
    $sqlCommand.CommandText = $updateQuery
    $sqlCommand.Parameters.Add((New-Object Data.SqlClient.SqlParameter("@newPassword", $newPassword)))
    $sqlCommand.Parameters.Add((New-Object Data.SqlClient.SqlParameter("@accountName", $domainServiceAccount)))

    $rowsAffected = $sqlCommand.ExecuteNonQuery()
    Write-Host "$rowsAffected row(s) updated in the database."
    
    $sqlConnection.Close()
} catch {
    Write-Host "Failed to update password in SQL Server: $_"
    exit 1
}
