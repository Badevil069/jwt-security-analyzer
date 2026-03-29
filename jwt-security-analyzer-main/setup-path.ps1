# JWT Analyzer Setup - Add to PATH
# This script permanently adds the jwt-analyzer directory to the Windows PATH environment variable

$jwtAnalyzerPath = "c:\Users\abhia\jwt-analyzer"
$currentPath = [System.Environment]::GetEnvironmentVariable("Path", "User")

if ($null -eq $currentPath) {
    $newPath = $jwtAnalyzerPath
} elseif ($currentPath -contains $jwtAnalyzerPath) {
    Write-Host "JWT Analyzer path already in PATH" -ForegroundColor Green
    exit 0
} else {
    $newPath = "$currentPath;$jwtAnalyzerPath"
}

[System.Environment]::SetEnvironmentVariable("Path", $newPath, "User")
Write-Host "Successfully added JWT Analyzer to PATH" -ForegroundColor Green
Write-Host "You may need to restart your terminal for changes to take effect" -ForegroundColor Yellow
