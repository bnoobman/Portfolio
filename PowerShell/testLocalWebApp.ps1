add-type @"
    using System.Net;
    using System.Security.Cryptography.X509Certificates;
    public class TrustAllCertsPolicy : ICertificatePolicy {
        public bool CheckValidationResult(
            ServicePoint srvPoint, X509Certificate certificate,
            WebRequest request, int certificateProblem) {
            return true;
        }
    }
"@

[System.Net.ServicePointManager]::CertificatePolicy = New-Object TrustAllCertsPolicy
[System.Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$log_file = "C:\Path\to\log\file"

function Write-Log {
    [CmdletBinding()]
    param(
        [Parameter()]
        [ValidateNotNullOrEmpty()]
        [string]$Message,
 
        [Parameter()]
        [ValidateNotNullOrEmpty()]
        [ValidateSet('INFO', 'WARN', 'ERROR')]
        [string]$Severity = 'INFO'
    )
 
    [pscustomobject]@{
        Time     = (Get-Date -f g)
        Message  = $Message
        Severity = $Severity
    } | Export-Csv -Path $log_file -Append -NoTypeInformation
}

$page_list = @("/test")
$counter_limit = 5
$sleep_timer = 10

function Send-Request {
    param(
    $uri,
    $counter = 1
    )

    $ip = get-WmiObject Win32_NetworkAdapterConfiguration | Where-Object {$_.Ipaddress.length -gt 1} 
    $local_ip = $ip.ipaddress[0]

    $url = "https://$local_ip$uri"
    $host_headders = ''

    $headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
    $headers.Add('Host',$host_headders)

    $result = Invoke-WebRequest -Uri $url -Headers $headers -UseBasicParsing

    If (-NOT ($result.StatusCode -eq 200) -AND $counter -le $counter_limit) {
        $raw_message = 'Request {0}/5 to {1} returned response code {2}. Trying again in 10 seconds...' -f $counter, $uri, $result.StatusCode
        Write-Log -Message $raw_message -Severity WARN
        $counter += 1
        Start-Sleep -Seconds $sleep_timer
        Send-Request -uri $uri -counter $counter
    } ElseIf (-NOT ($result.StatusCode -eq 200) -AND $counter -gt $counter_limit) {
        $raw_message = '{0}/{1} Test requests to {2} failed! All requests returned non-200 response codes.' -f $counter, $counter_limit, $uri
        Write-Log -Message $raw_message -Severity ERROR
        continue
    } Else {
        $raw_message = 'Request {0}/5 to {1} returned response code 200!' -f $counter, $uri
        Write-Log -Message $raw_message -Severity INFO
        $result.StatusCode
    }
}

foreach ($page in $page_list) {
    Send-Request -uri $page
}