# Import users from Active Directory to PagerDuty
# Requires Windows Server 2008 R2
# Users should be members of a security group named "pagerduty"

Import-Module activedirectory

# Import users via the PD API
function POST_Request ($url,$parameters, $api_key) {
    $http_request = New-Object -ComObject Msxml2.XMLHTTP
    $http_request.open('POST', $url, $false)
    $http_request.setRequestHeader("Content-type", "application/json")
    $token = "Token token=" + $api_key
    $http_request.setRequestHeader("Authorization", $token)
    $http_request.setRequestHeader("Content-length", $parameters.length)
    $http_request.setRequestHeader("Connection", "close")
    $http_request.send($parameters)
    $http_request.statusText 
}

# Pull all users from the pagerduty group within Active Directory
Get-ADGroup "pagerduty" | % { 
    $users = "Name,Email`r`n";
    $_ | Get-ADGroupMember | % { 
        $user = Get-ADUser $_ -Properties *
        $users += $user.Name + "," + $user.EmailAddress + "`r`n"
    }
}

# Get the authentication information and add each users via POST_Request
$subdomain = Read-Host "Enter subdomain (e.g. <subdomain>.pagerduty.com)"
$api_key = Read-Host "Enter API key"
$requester_id = Read-Host "Enter requester_id"
$url = "https://" + $subdomain + ".pagerduty.com/api/v1/users"
$parameters = New-Object Collections.Specialized.NameValueCollection;
$users = ConvertFrom-Csv $users
$users | % { 
    Write-Host "Importing user:" $_.Name
    $parameters = "{`"requester_id`":`"" + $requester_id + "`",`"name`":`"" + $_.Name + "`",`"email`":`"" + $_.Email + "`"}"
    POST_Request $url $parameters $api_key
}