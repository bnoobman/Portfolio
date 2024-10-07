function Search-EventLog {
    param (

        # Specifies the computer to search through event logs on
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $ComputerName,

        # Name of the event log you want to search
        [Parameter(mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $Log,

        # Datetime value to start search at
        [Parameter()]
        [DateTime]
        $Start,

        # Datetime value to end search at
        [Parameter()]
        [DateTime]
        $End,

        # Logging level to filter events on
        [Parameter()]
        [ValidateSet('Info','Warn','Error','Critical')]
        [string]
        $Level = 'Warn'

    )

    $LevelHash = @{
        'Info'=4
        'Warn'=3
        'Error'=2
        'Critical'=1
    }
    
    # TODO Make WAY more secure
    $Username = 'username'
    $pwdTxt = Get-Content "C:\Path\to\txt\file\with\password\so\secure\I\know..."
    $securePwd = $pwdTxt | ConvertTo-SecureString
    $credObject = New-Object System.Management.Automation.PSCredential -ArgumentList $Username, $securePwd 

    Get-WinEvent -FilterHashtable @{
        LogName=$Log
        StartTime=$Start
        EndTime=$End
        Level=$LevelHash[$Level]
    } -ComputerName $ComputerName -Credential $credObject
}

