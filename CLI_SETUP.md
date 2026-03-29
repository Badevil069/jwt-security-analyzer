# JWT Analyzer CLI Setup & Usage Guide

## Installation Status ✅

The `jwt` command is now fully configured and ready to use! Here's what was set up:

### What Was Configured:
1. **CLI Entry Points**: Created `jwt.bat` script wrapper for Windows
2. **PowerShell Integration**: Added `jwt` function to your PowerShell profile
3. **JSON Output**: Implemented `--json` flag for structured output
4. **Enhanced Banner**: Shows "JWT Security Analyzer v1.0" and "Advanced Mode Enabled"

---

## Using the `jwt` Command

### Basic Usage

```powershell
# Scan a token with interactive table output and PDF report
jwt scan eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Scan a token and display the banner
jwt scan eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Scan without the banner (quiet mode)
jwt scan eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... --no-banner

# Get version information
jwt --version

# Get help
jwt --help
jwt scan --help
```

---

## New Features

### 1. **JSON Output Mode** 

Get structured JSON output for automation/scripting:

```powershell
jwt scan eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... --json
```

**Sample Output:**
```json
{
  "tool": "JWT Security Analyzer",
  "version": "1.0.0",
  "timestamp": "2026-02-22T22:12:02.203197",
  "mode": "advanced",
  "vulnerabilities": [
    {
      "check": "1. None Algorithm",
      "status": "PASS",
      "detail": "Algorithm set properly",
      "cve": null
    },
    {
      "check": "5. Token Expiration",
      "status": "CRITICAL",
      "detail": "No expiration claim",
      "cve": "CVE-2020-28169"
    }
    // ... more results
  ],
  "score": 95
}
```

**Use Cases:**
- CI/CD pipeline integration
- Automated security scanning
- Report generation
- Vulnerability tracking systems
- SIEM integration

### 2. **Banner Display** 

When you run `jwt scan`, you'll now see:

```
╔════════════════════════════════════════╗
║   JWT Security Analyzer v1.0           ║
║   Advanced Mode Enabled                ║
╚════════════════════════════════════════╝
```

To suppress the banner, use `--no-banner`:
```powershell
jwt scan TOKEN --no-banner
```

### 3. **Custom Output Filename**

You can specify where to save the PDF report:

```powershell
jwt scan TOKEN --output my-report.pdf
jwt scan TOKEN -o security-audit.pdf
```

---

## Command Reference

### `jwt --version`
Display the tool version
```
JWT Analyzer v1.0.0
```

### `jwt --help`
Show help for the main tool

### `jwt scan TOKEN [OPTIONS]`

**Arguments:**
- `TOKEN` - The JWT token to analyze (required)

**Options:**
- `--json` - Output results as JSON (no table, no PDF)
- `--no-banner` - Suppress the banner output
- `--output, -o FILENAME` - Specify PDF report filename (default: report.pdf)
- `--help` - Show command help

**Examples:**

```powershell
# Standard analysis with table and PDF
jwt scan eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# JSON output for scripting
jwt scan eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... --json | ConvertFrom-Json

# Custom report name
jwt scan eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... --output "jwt-audit-2026.pdf"

# Automation friendly (no banner, custom output)
jwt scan eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... --no-banner --output "report.pdf"
```

---

## Integration Examples

### PowerShell Scripting

```powershell
# Store JSON results and process them
$result = jwt scan $token --json | ConvertFrom-Json

# Check for critical vulnerabilities
$critical = $result.vulnerabilities | Where-Object { $_.status -eq "CRITICAL" }
if ($critical.Count -gt 0) {
    Write-Host "CRITICAL VULNERABILITIES FOUND!" -ForegroundColor Red
    $critical | Format-Table check, detail, cve
}
```

### CI/CD Pipeline (GitHub Actions)

```yaml
- name: Scan JWT Token
  run: jwt scan ${{ secrets.JWT_TOKEN }} --json > jwt-scan.json

- name: Check Results
  run: |
    if grep -q "CRITICAL" jwt-scan.json; then
      echo "Security issues found!"
      exit 1
    fi
```

### Batch Processing

```powershell
# Scan multiple tokens
@(
  "token1...",
  "token2...",
  "token3..."
) | ForEach-Object {
  jwt scan $_ --json | ConvertFrom-Json | Select-Object -Property timestamp, score
}
```

---

## Troubleshooting

### Command Not Found

If you get "jwt is not recognized", try one of these:

1. **Reload PowerShell Profile:**
   ```powershell
   . $PROFILE
   ```

2. **Run from Project Directory:**
   ```powershell
   cd c:\Users\abhia\jwt-analyzer
   .\jwt.bat scan TOKEN
   ```

3. **Manually Run via Python:**
   ```powershell
   python c:\Users\abhia\jwt-analyzer\main.py scan TOKEN
   ```

### JSON Output Contains Color Codes

The JSON output has special handling to strip ANSI color codes. If you see color codes in the JSON "detail" field, they're cleaned during export.

### PDF Report Not Generated with `--json`

This is intentional - when using `--json` mode, only the JSON output is produced (no PDF). To get both:

```powershell
jwt scan TOKEN              # Gets table + PDF
jwt scan TOKEN --json       # Gets JSON only
```

---

## Accessing the JWT Command from Anywhere

The PowerShell profile has been configured so you can run:

```powershell
jwt scan TOKEN
```

from any directory. If this doesn't work:

1. Check execution policy:
   ```powershell
   Get-ExecutionPolicy
   # Should show: RemoteSigned
   ```

2. Verify profile exists:
   ```powershell
   Test-Path $PROFILE
   Test-Path "C:\Users\abhia\OneDrive\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1"
   ```

3. Manual setup (if needed):
   ```powershell
   $profilePath = $PROFILE
   Add-Content -Path $profilePath -Value "`nfunction jwt { & 'c:\Users\abhia\jwt-analyzer\jwt.bat' @args }"
   . $PROFILE
   ```

---

## Example Workflows

### Security Audit Workflow

```powershell
# Scan token and save detailed report
jwt scan $myToken --output "audit-$(Get-Date -Format 'yyyy-MM-dd').pdf"

# Generate JSON for tool integration
$results = jwt scan $myToken --json | ConvertFrom-Json

# Export for further analysis
$results | Export-Csv "jwt-scan-results.csv"
```

### Continuous Scanning

```powershell
# Monitor tokens for vulnerabilities
$tokens = Get-Content "tokens.txt"
$vulnerabilities = @()

foreach ($token in $tokens) {
  $result = jwt scan $token --json | ConvertFrom-Json
  if ($result.score -lt 85) {
    $vulnerabilities += @{
      Token = $token.Substring(0, 20) + "..."
      Score = $result.score
      Issues = $result.vulnerabilities | Where-Object { $_.status -ne "PASS" } | Measure-Object | Select-Object -ExpandProperty Count
    }
  }
}

$vulnerabilities | Format-Table
```

---

## Files Created

- ✅ `jwt.bat` - Windows batch script wrapper for command execution
- ✅ `setup.py` - Python package configuration with CLI entry points
- ✅ `POWERSHELL_SETUP.md` - PowerShell profile setup documentation
- ✅ Updated `main.py` - Added JSON output support and banner display

---

## Support

For issues or questions about the JWT analyzer:
- Check `README.md` for vulnerability details
- Review `ADVANCED_MODE.md` for attack vector documentation
- See `COLOR_SCHEME.md` for risk level explanations
- Run `jwt --help` for command reference

**Happy token hunting!** 🔐
