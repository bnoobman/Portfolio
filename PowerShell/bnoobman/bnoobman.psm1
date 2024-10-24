# QoL.ps1 functions
function vscode { ... }
function open-web { ... }
function copy-path { ... }
function Get-FolderSize { ... }
function ll { ... }
function zip { ... }
function unzip { ... }
function backup-file { ... }
function find-process { ... }
function uptime { ... }
function git-status { ... }
function new-uuid { ... }
function kill-process { ... }
function Get-DiskUsage { ... }
function restart-network { ... }
function clear-dns { ... }
function exec-time { ... }
function download-file { ... }
function test-connection { ... }

# sys-admin.ps1 functions
function Monitor-DiskSpace { ... }
function Get-Uptime { ... }
function Get-DetailedSystemInfo { ... }
function Shutdown-System { ... }
function Restart-NetworkAdapter { ... }
function Get-NetworkInfo { ... }
function Get-NetworkConnections { ... }
function Get-SystemPerformance { ... }
function Get-ServicesByStatus { ... }
function Flush-DnsCache { ... }
function Unlock-User { ... }
function Lock-User { ... }
function Get-LocalUsers { ... }
function New-LocalUser { ... }
function Check-EventLog { ... }
function Check-DriveSpace { ... }
function Restart-ServiceByName { ... }
function Get-ServiceStatus { ... }
function Get-SystemInfo { ... }

# Export all functions
Export-ModuleMember -Function vscode, open-web, copy-path, Get-FolderSize, ll, zip, unzip, backup-file, find-process, uptime, git-status, new-uuid, kill-process, Get-DiskUsage, restart-network, clear-dns, exec-time, download-file, test-connection, Monitor-DiskSpace, Get-Uptime, Get-DetailedSystemInfo, Shutdown-System, Restart-NetworkAdapter, Get-NetworkInfo, Get-NetworkConnections, Get-SystemPerformance, Get-ServicesByStatus, Flush-DnsCache, Unlock-User, Lock-User, Get-LocalUsers, New-LocalUser, Check-EventLog, Check-DriveSpace, Restart-ServiceByName, Get-ServiceStatus, Get-SystemInfo
