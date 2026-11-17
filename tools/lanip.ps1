# Prints this computer's address on the local network, for phones on the same Wi-Fi.
foreach ($a in [Net.Dns]::GetHostAddresses([Net.Dns]::GetHostName())) {
    $s = $a.ToString()
    if ($a.AddressFamily -eq 'InterNetwork' -and -not $s.StartsWith('127.') -and -not $s.StartsWith('169.254.')) { $s; break }
}
