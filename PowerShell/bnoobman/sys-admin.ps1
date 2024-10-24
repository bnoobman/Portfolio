function Monitor-DiskSpace {
    param (
        [string[]]$servers = @("localhost"),
        [int]$thresholdGB = 10
    )
    foreach ($server in $servers) {
        $disks = Get-WmiObject -Class Win32_LogicalDisk -ComputerName $server | Where-Object {$_.DriveType -eq 3}
        foreach ($disk in $disks) {
            $freeSpaceGB = [math]::round($disk.FreeSpace / 1GB, 2)
            if ($freeSpaceGB -lt $thresholdGB) {
                Write-Host "Alert: Disk space on $server $($disk.DeviceID) is below threshold ($freeSpaceGB GB free)"
            }
        }
    }
}

# Usage: Monitor-DiskSpace -servers @("Server1", "Server2") -thresholdGB 20

function Get-Uptime {
    param (
        [string[]]$computers = @('localhost')
    )
    foreach ($computer in $computers) {
        $os = Get-CimInstance -ClassName Win32_OperatingSystem -ComputerName $computer
        [PSCustomObject]@{
            ComputerName = $computer
            Uptime       = ((Get-Date) - $os.LastBootUpTime).Days
            LastBoot     = $os.LastBootUpTime
        }
    }
}

# Usage: Get-Uptime -computers @("Server1", "Server2", "localhost")

function Get-DetailedSystemInfo {
    $os = Get-CimInstance -ClassName Win32_OperatingSystem
    $cpu = Get-CimInstance -ClassName Win32_Processor
    $ram = Get-CimInstance -ClassName Win32_PhysicalMemory | Measure-Object Capacity -Sum
    $disk = Get-PSDrive -PSProvider FileSystem | Where-Object {$_.Name -eq "C"}

    [PSCustomObject]@{
        ComputerName = $os.CSName
        OS           = $os.Caption
        CPU          = $cpu.Name
        RAM_GB       = [math]::round($ram.Sum / 1GB, 2)
        Disk_GB      = [math]::round($disk.Used / 1GB, 2)
        FreeDisk_GB  = [math]::round($disk.Free / 1GB, 2)
        LastBoot     = $os.LastBootUpTime
    }
}

# Usage: Get-DetailedSystemInfo

function Shutdown-System {
    param(
        [switch]$restart
    )
    if ($restart) {
        Restart-Computer
    } else {
        Stop-Computer
    }
}

# Usage: Shutdown-System -restart (Restarts the system)
#        Shutdown-System (Shuts down the system)

function Restart-NetworkAdapter {
    param(
        [string]$adapterName = "Ethernet"
    )
    Disable-NetAdapter -Name $adapterName -Confirm:$false
    Start-Sleep -Seconds 5
    Enable-NetAdapter -Name $adapterName -Confirm:$false
}

# Usage: Restart-NetworkAdapter "Wi-Fi"

function Get-NetworkInfo {
    Get-NetAdapter | Select-Object Name, Status, MacAddress, LinkSpeed, MediaType
}

# Usage: Get-NetworkInfo

function Get-NetworkConnections {
    Get-NetTCPConnection | Select-Object LocalAddress, LocalPort, RemoteAddress, RemotePort, State
}

# Usage: Get-NetworkConnections

function Get-SystemPerformance {
    Get-WmiObject Win32_Processor | Select-Object Name, @{Name="CPU Load (%)";Expression={$_.LoadPercentage}}
    Get-WmiObject Win32_OperatingSystem | Select-Object @{Name="Free Memory (MB)";Expression={[math]::round($_.FreePhysicalMemory / 1KB, 2)}}, @{Name="Total Memory (MB)";Expression={[math]::round($_.TotalVisibleMemorySize / 1KB, 2)}}
}

# Usage: Get-SystemPerformance

function Get-ServicesByStatus {
    param(
        [string]$status = "Running"
    )
    Get-Service | Where-Object { $_.Status -eq $status }
}

# Usage: Get-ServicesByStatus "Stopped"

function Flush-DnsCache {
    Clear-DnsClientCache
    Write-Host "DNS Cache Cleared"
}

# Usage: Flush-DnsCache

function Unlock-User {
    param(
        [string]$username
    )
    Enable-LocalUser -Name $username
}

# Usage: Unlock-User "adminuser"

function Lock-User {
    param(
        [string]$username
    )
    Disable-LocalUser -Name $username
}

# Usage: Lock-User "adminuser"

function Get-LocalUsers {
    Get-LocalUser | Select-Object Name, Enabled, LastLogon
}

# Usage: Get-LocalUsers

function New-LocalUser {
    param(
        [string]$username,
        [string]$password
    )
    New-LocalUser -Name $username -Password (ConvertTo-SecureString $password -AsPlainText -Force) -FullName $username -AccountNeverExpires -PasswordNeverExpires
}

# Usage: New-LocalUser "adminuser" "password123"

function Check-EventLog {
    param(
        [string]$logName = "System",
        [int]$lastDays = 1
    )
    Get-EventLog -LogName $logName -After (Get-Date).AddDays(-$lastDays) | Select-Object TimeGenerated, EntryType, Source, EventID, Message
}

# Usage: Check-EventLog "System" 7 (Checks system event logs for the past 7 days)

function Check-DriveSpace {
    param(
        [string]$driveLetter = "C"
    )
    Get-PSDrive -Name $driveLetter | Select-Object Name, @{Name="Used (GB)";Expression={[math]::round(($_.Used / 1GB), 2)}}, @{Name="Free (GB)";Expression={[math]::round(($_.Free / 1GB), 2)}}
}

# Usage: Check-DriveSpace "C"

function Restart-ServiceByName {
    param(
        [string]$serviceName
    )
    Restart-Service -Name $serviceName -Force
}

# Usage: Restart-ServiceByName "Spooler"

function Get-ServiceStatus {
    param(
        [string]$serviceName
    )
    Get-Service -Name $serviceName
}

# Usage: Get-ServiceStatus "Spooler"

function Get-SystemInfo {
    Get-CimInstance -ClassName Win32_OperatingSystem | Select-Object Caption, CSName, OSArchitecture, Version, BuildNumber, @{Name="Last Boot Time";Expression={$_.LastBootUpTime}}, @{Name="Free Physical Memory (MB)";Expression={[math]::round($_.FreePhysicalMemory / 1KB, 2)}}
}

# Usage: Get-SystemInfo

