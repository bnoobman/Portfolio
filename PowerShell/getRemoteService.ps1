# List of servers
$serverList = @("server1","server2")
# List of services to check for
$serviceList = @("SW_*","VisualCron","SplunkForwarder")


foreach ($server in $serverList) {
    $fqdn = "$server.production.seamlessweb.com"
    Write-Host "Service Status List for: $server`n"
    foreach-object ($service in $serviceList) {
        Get-Service -Name $service -ComputerName $fqdn | Select-Object Status, Name, DisplayName | Format-Table -A
    }
}