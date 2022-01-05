# A cmdlet to simplify the ssh call, providing only the remote IP as a parameter
#   ASSUMES:
#       hostname = ubuntu
#       private key location = ./rsa_private.pem
Function ss {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory = $true)]
        [string] $ip
    )
    BEGIN {}
    PROCESS {
        ssh -i ./rsa_private.pem "ubuntu@$ip"
    }
    END {}
}
