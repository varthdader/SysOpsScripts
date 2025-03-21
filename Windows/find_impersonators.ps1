$users = Get-ADUser -Filter *
foreach ($user in $users) {
    $userPrincipalName = $user.UserPrincipalName
    $computer = "yourdomaincontroller" # Modify As Needed for Your Domain
    $session = New-PSSession -ComputerName $computer
    Invoke-Command -Session $session -ScriptBlock {
        param($userPrincipalName)
        $user = Get-ADUser -Identity $userPrincipalName -Properties MemberOf
        $privileges = whoami /priv
        $seImpersonatePrivilege = $privileges | Where-Object { $_ -match "SeImpersonatePrivilege" }
        if ($seImpersonatePrivilege) {
            return $user.UserPrincipalName
        }
    } -ArgumentList $userPrincipalName
    Remove-PSSession -Session $session
}
