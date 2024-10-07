function Invoke-WebRequestV2 {  
    param(
        [Parameter(mandatory,
        Position = 0,
        ValueFromPipeline = $true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $uri 
    )  

    try {
        $webrequest = [System.Net.WebRequest]::Create($uri)
        $response = $webrequest.GetResponse()
        $response |Select-Object ResponseUri,Method,StatusCode
    }
    catch [System.Net.WebException]{
        throw $error[0].exception.innerexception
    }  
}