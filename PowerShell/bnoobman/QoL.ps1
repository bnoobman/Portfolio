function vscode {
    param(
        [string]$path = (Get-Location)
    )
    code $path
}

# Usage: vscode "C:\path\to\folder"
# If no path is provided, it will open the current folder

function open-web {
    param(
        [string]$url
    )
    Start-Process $url
}

# Usage: open-web "https://www.example.com"

function copy-path {
    param (
        [Alias('File')][string]$item = (Get-Location)
    )
    $fullPath = Resolve-Path $item
    $fullPath | clip
    Write-Output "$fullPath copied to clipboard"
}

# Usage: copy-path "C:\path\to\file.txt"

function Get-FolderSize {
    param(
        [string]$folder = (Get-Location)
    )
    Get-ChildItem $folder -Recurse | Measure-Object -Property Length -Sum | Select-Object @{Name="Size (MB)";Expression={[math]::round($_.Sum / 1MB, 2)}}
}

# Usage: Get-FolderSize "C:\path\to\folder"

function ll {
    Get-ChildItem -Force | Format-Table Name, Length, LastWriteTime
}

# Usage: ll (Lists files in current directory with details)

function zip {
    param(
        [string]$source,
        [string]$destination
    )
    Compress-Archive -Path $source -DestinationPath $destination
}

# Usage: zip "C:\path\to\folder" "C:\path\to\archive.zip"

function unzip {
    param(
        [string]$zipfile,
        [string]$destination
    )
    Expand-Archive -Path $zipfile -DestinationPath $destination
}

# Usage: unzip "C:\path\to\archive.zip" "C:\destination\folder"

function backup-file {
    param(
        [string]$filePath,
        [string]$backupDir = "$env:USERPROFILE\Documents\Backups"
    )
    if (-not (Test-Path $backupDir)) {
        New-Item -ItemType Directory -Path $backupDir | Out-Null
    }
    Copy-Item $filePath -Destination "$backupDir\$((Get-Date).ToString('yyyyMMdd_HHmmss'))_$(Split-Path -Leaf $filePath)"
}

# Usage: backup-file "C:\path\to\file.txt"

function find-process {
    param(
        [string]$processName
    )
    Get-Process | Where-Object { $_.Name -like "*$processName*" }
}

# Usage: find-process "chrome"

function uptime {
    (Get-CimInstance Win32_OperatingSystem).LastBootUpTime
}

# Usage: uptime

function git-status {
    Set-Location -Path (git rev-parse --show-toplevel)
    git status
}

# Usage: git-status

function new-uuid {
    [guid]::NewGuid().ToString()
}

# Usage: new-uuid

function kill-process {
    param(
        [string]$processName
    )
    Stop-Process -Name $processName -Force
}

# Usage: kill-process "chrome"

function Get-DiskUsage {
    Get-PSDrive -PSProvider FileSystem | Select-Object Name, @{Name="Used (GB)";Expression={[math]::round(($_.Used/1GB), 2)}}, @{Name="Free (GB)";Expression={[math]::round(($_.Free/1GB), 2)}}, @{Name="Total (GB)";Expression={[math]::round(($_.Used/1GB + $_.Free/1GB), 2)}}
}

# Usage: Get-DiskUsage

function restart-network {
    Restart-Service -Name "Dhcp" -Force
}

# Usage: restart-network (Restarts the DHCP service to renew IP addresses)

function clear-dns {
    Clear-DnsClientCache
}

# Usage: clear-dns

function exec-time {
    $ExecutionTime = $(Measure-Command { Invoke-Expression "$($MyInvocation.Line)" }).TotalSeconds
    Write-Host "Execution Time: $ExecutionTime seconds"
}

# Usage: You can run any command prefixed with exec-time, e.g., exec-time Get-Process

function download-file {
    param(
        [string]$url,
        [string]$destination
    )
    Invoke-WebRequest -Uri $url -OutFile $destination
}

# Usage: download-file "https://example.com/file.zip" "C:\path\to\file.zip"

function test-connection {
    param(
        [string]$hostname = "8.8.8.8"
    )
    Test-Connection -ComputerName $hostname -Count 4
}

# Usage: test-connection "google.com"
