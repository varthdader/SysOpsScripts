<# Script: svc_account_recred.ps1
A PowerShell script loads a named users password hash into the memory of the local host. 
This should be run as a GPO upon boot for all critical servers.

Author: VarthDader (https://github.com/varthdader)
#>

# Modify Variables as Needed
    
    $Domain = "mydomain.com"
    $UserName = "VarthDaderAdmin"
    $Password = "3asyd03s1T!"
    $PSPassword = $Password | ConvertTo-SecureString -asPlainText -Force

    $SystemModule = [Microsoft.Win32.IntranetZoneCredentialPolicy].Module
    $NativeMethods = $SystemModule.GetType('Microsoft.Win32.NativeMethods')
    $SafeNativeMethods = $SystemModule.GetType('Microsoft.Win32.SafeNativeMethods')
    $CreateProcessWithLogonW = $NativeMethods.GetMethod('CreateProcessWithLogonW', [Reflection.BindingFlags] 'NonPublic, Static')
    $LogonFlags = $NativeMethods.GetNestedType('LogonFlags', [Reflection.BindingFlags] 'NonPublic')
    $StartupInfo = $NativeMethods.GetNestedType('STARTUPINFO', [Reflection.BindingFlags] 'NonPublic')
    $ProcessInformation = $SafeNativeMethods.GetNestedType('PROCESS_INFORMATION', [Reflection.BindingFlags] 'NonPublic')

    $Flags = [Activator]::CreateInstance($LogonFlags)
    $Flags.value__ = 2 # LOGON_NETCREDENTIALS_ONLY 
    $StartInfo = [Activator]::CreateInstance($StartupInfo)
    $ProcInfo = [Activator]::CreateInstance($ProcessInformation)

    $Credential = New-Object System.Management.Automation.PSCredential("$($Domain)\$($UserName)",$PSPassword)

    $PasswordPtr = [System.Runtime.InteropServices.Marshal]::SecureStringToCoTaskMemUnicode($Credential.Password)
    $StrBuilder = New-Object System.Text.StringBuilder
    $null = $StrBuilder.Append('cmd.exe')

    $Result = $CreateProcessWithLogonW.Invoke($null, @([String] $UserName,
                                             [String] $Domain,
                                             [IntPtr] $PasswordPtr,
                                             ($Flags -as $LogonFlags),     # LOGON_NETCREDENTIALS_ONLY 
                                             $null,
                                             [Text.StringBuilder] $StrBuilder,
                                             0x08000000, # Don't display a window
                                             $null,
                                             $null,
                                             $StartInfo,
                                             $ProcInfo))

    if (-not $Result) {
        throw 'Unable to create process as user.'
    }

    if ($ProcInfo.dwProcessId) {
        # Kill the cmd.exe process
        Stop-Process -Id $ProcInfo.dwProcessId
    }

    '"Honey hash" injected into LSASS successfully! Use Mimikatz to confirm.'
	do{
	'"Let me sleep!!!'
	sleep 10
	[GC]::Collect()
	[System.GC]::Collect()
	}
	while (1)
