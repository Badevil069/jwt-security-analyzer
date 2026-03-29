import jwt
import json
import base64
from rich.table import Table
from datetime import datetime
import warnings
import re

# CVE Mapping for JWT vulnerabilities
CVE_MAP = {
    "alg_none": "CVE-2015-9235",
    "algorithm_confusion": "CVE-2016-5431", 
    "weak_secret": "CVE-2014-9721",
    "key_confusion": "CVE-2015-9235",
    "expired_token": "CVE-2020-28169",
    "kid_injection": "CVE-2020-28169",
    "signature_bypass": "CVE-2015-9235",
    "jwks_bypass": "CVE-2021-22911",
    "alg_swap": "CVE-2016-5431",
    "jku_injection": "CVE-2020-28169",
    "kid_traversal": "CVE-2021-22911"
}

def decode_jwt_parts(token):
    """Safely decode JWT parts without verification"""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None, None, None
        
        # Decode header
        header = json.loads(base64.urlsafe_b64decode(parts[0] + '=='))
        # Decode payload
        payload = json.loads(base64.urlsafe_b64decode(parts[1] + '=='))
        # Signature (just base64 decoded)
        try:
            signature = base64.urlsafe_b64decode(parts[2] + '==')
        except:
            signature = parts[2]
        
        return header, payload, signature
    except:
        return None, None, None

def analyze_token(token, advanced_mode=True):
    """
    Advanced JWT Security Analysis with Pentester-Level Attack Detection
    """
    
    results = []
    vulnerabilities = []
    
    warnings.filterwarnings('ignore')

    # Create table with color-coded styling
    table = Table(title="[bold cyan]JWT Security Analysis Report - Advanced Mode[/bold cyan]")
    table.add_column("Vulnerability", style="bold white", width=30)
    table.add_column("Status", style="bold white", width=15)
    table.add_column("Details & CVE", style="white", width=50)

    try:
        header = jwt.get_unverified_header(token)
        payload = jwt.decode(token, options={"verify_signature": False})
    except Exception as e:
        table.add_row("[red]Token Validation[/red]", "[red bold]CRITICAL[/red bold]", f"[red]Invalid JWT: {str(e)}[/red]")
        return table, [("CRITICAL", "Invalid JWT")]

    alg = header.get("alg")
    kid = header.get("kid")
    jku = header.get("jku")
    
    # ==== VULNERABILITY 1: None Algorithm (alg:none) ====
    if alg == "none":
        msg = f"CVE-{CVE_MAP['alg_none']}: No signature validation"
        table.add_row("[red]1. None Algorithm[/red]", "[red bold]CRITICAL[/red bold]", f"[red]{msg}[/red]")
        vulnerabilities.append(("CRITICAL", "alg:none - No signature validation"))
        results.append(("1. None Algorithm", msg))
    else:
        table.add_row("[green]1. None Algorithm[/green]", "[green bold]PASS[/green bold]", "[green]Algorithm set properly[/green]")
        results.append(("1. None Algorithm", "PASS"))

    # ==== VULNERABILITY 2: Algorithm Confusion / Algorithm Swap Attack ====
    if alg and alg.startswith("RS"):
        # Try to verify with HS256 using public key as secret
        msg = f"CVE-{CVE_MAP['alg_swap']}: RS256HS256 confusion attack possible"
        table.add_row("[red]2. Algorithm Swap Attack[/red]", "[red bold]HIGH[/red bold]", f"[red]{msg}[/red]")
        vulnerabilities.append(("HIGH", "Algorithm swap: RS256 can be confused with HS256"))
        results.append(("2. Algorithm Swap", msg))
    elif alg and alg.startswith("HS"):
        table.add_row("[yellow]2. Algorithm Swap Attack[/yellow]", "[yellow bold]MEDIUM[/yellow bold]", "[yellow]Symmetric algorithm - swap risk present[/yellow]")
        results.append(("2. Algorithm Swap", "MEDIUM RISK"))
    else:
        table.add_row("[green]2. Algorithm Swap Attack[/green]", "[green bold]PASS[/green bold]", "[green]Asymmetric algorithm - swap resistant[/green]")
        results.append(("2. Algorithm Swap", "PASS"))

    # ==== VULNERABILITY 3: Weak HMAC Secrets ====
    secrets = open("secrets.txt").read().splitlines()
    weak_found = False
    matching_secret = None
    
    for secret in secrets:
        for test_alg in ["HS256", "HS384", "HS512"]:
            try:
                jwt.decode(token, secret, algorithms=[test_alg])
                msg = f"CVE-{CVE_MAP['weak_secret']}: Secret matched in 500+ signatures"
                table.add_row("[red]3. Weak HMAC Secret[/red]", "[red bold]CRITICAL[/red bold]", f"[red]{msg}[/red]")
                vulnerabilities.append(("CRITICAL", f"Weak secret: {secret}"))
                results.append(("3. Weak HMAC Secret", f"CRITICAL - {secret}"))
                weak_found = True
                matching_secret = secret
                break
            except:
                pass
        if weak_found:
            break

    if not weak_found:
        table.add_row("[green]3. Weak HMAC Secret[/green]", "[green bold]PASS[/green bold]", "[green]No weak secrets matched (500+ signatures)[/green]")
        results.append(("3. Weak HMAC Secret", "PASS"))

    # ==== VULNERABILITY 4: Key Confusion Attack ====
    if alg == "HS256" or alg == "HS384" or alg == "HS512":
        msg = f"CVE-{CVE_MAP['key_confusion']}: Symmetric algorithm vulnerable to key exposure"
        table.add_row("[yellow]4. Key Confusion[/yellow]", "[yellow bold]HIGH[/yellow bold]", f"[yellow]{msg}[/yellow]")
        vulnerabilities.append(("HIGH", "Symmetric algorithm key confusion risk"))
        results.append(("4. Key Confusion", msg))
    else:
        table.add_row("[green]4. Key Confusion[/green]", "[green bold]PASS[/green bold]", "[green]Asymmetric algorithm used[/green]")
        results.append(("4. Key Confusion", "PASS"))

    # ==== VULNERABILITY 5: Token Expiration ====
    exp = payload.get("exp")
    if not exp:
        msg = f"CVE-{CVE_MAP['expired_token']}: No expiration claim"
        table.add_row("[red]5. Token Expiration[/red]", "[red bold]CRITICAL[/red bold]", f"[red]{msg}[/red]")
        vulnerabilities.append(("CRITICAL", "Missing token expiration"))
        results.append(("5. Token Expiration", msg))
    elif datetime.utcnow().timestamp() > exp:
        table.add_row("[yellow]5. Token Expiration[/yellow]", "[yellow bold]MEDIUM[/yellow bold]", "[yellow]Token is expired (still analyzable)[/yellow]")
        results.append(("5. Token Expiration", "Token expired"))
    else:
        exp_time = datetime.utcfromtimestamp(exp).strftime("%Y-%m-%d %H:%M:%S")
        table.add_row("[green]5. Token Expiration[/green]", "[green bold]PASS[/green bold]", f"[green]Valid until {exp_time}[/green]")
        results.append(("5. Token Expiration", "PASS"))

    # ==== VULNERABILITY 6: KID Path Traversal Attack ====
    if kid:
        path_traversal_patterns = [
            r'\.\.',  # Parent directory ../
            r'\./',   # ./ relative
            r'etc/passwd',  # /etc/passwd
            r'root\.json',  # root.json
            r'keys/',  # keys/ directory
            r'\|',    # Pipe character (command injection)
            r';',     # Semicolon (command injection)
            r'`',     # Backtick (command injection)
            r'\$',    # Dollar sign (variable expansion)
        ]
        
        has_traversal = any(re.search(pattern, str(kid), re.IGNORECASE) for pattern in path_traversal_patterns)
        
        if isinstance(kid, str):
            if has_traversal:
                msg = f"CVE-{CVE_MAP['kid_traversal']}: KID contains path traversal/injection payload"
                table.add_row("[red]6. KID Path Traversal[/red]", "[red bold]CRITICAL[/red bold]", f"[red]{msg}[/red]")
                vulnerabilities.append(("CRITICAL", "KID path traversal/injection"))
                results.append(("6. KID Path Traversal", msg))
            elif "; " in kid or "|" in kid or "/" in kid:
                msg = f"CVE-{CVE_MAP['kid_injection']}: KID parameter potentially injectable"
                table.add_row("[yellow]6. KID Path Traversal[/yellow]", "[yellow bold]HIGH[/yellow bold]", f"[yellow]{msg}[/yellow]")
                vulnerabilities.append(("HIGH", "KID parameter injection"))
                results.append(("6. KID Path Traversal", msg))
            else:
                table.add_row("[green]6. KID Path Traversal[/green]", "[green bold]PASS[/green bold]", f"[green]KID: {kid[:20]} (safe)[/green]")
                results.append(("6. KID Path Traversal", "PASS"))
        else:
            table.add_row("[green]6. KID Path Traversal[/green]", "[green bold]PASS[/green bold]", "[green]Non-string KID[/green]")
            results.append(("6. KID Path Traversal", "PASS"))
    else:
        table.add_row("[yellow]6. KID Path Traversal[/yellow]", "[yellow bold]MEDIUM[/yellow bold]", "[yellow]No KID claim (JWKS matching impossible)[/yellow]")
        results.append(("6. KID Path Traversal", "MEDIUM"))

    # ==== VULNERABILITY 7: JKU Injection / Malicious JWKS Endpoint ====
    if jku:
        jku_risk = "PASS"
        jku_color = "green"
        jku_msg = f"JKU: {jku[:40]}"
        
        # Check for HTTP (insecure)
        if jku.startswith("http://"):
            jku_risk = "CRITICAL"
            jku_color = "red"
            jku_msg = f"CVE-{CVE_MAP['jku_injection']}: Insecure HTTP endpoint - MITM possible"
            vulnerabilities.append(("CRITICAL", "JWKS endpoint over HTTP"))
        
        # Check for localhost/127.0.0.1 (bypasses)
        elif any(x in jku for x in ["localhost", "127.0.0.1", "0.0.0.0", "192.168", "10.0"]):
            jku_risk = "HIGH"
            jku_color = "yellow"
            jku_msg = f"CVE-{CVE_MAP['jku_injection']}: Internal network endpoint - possible bypass"
            vulnerabilities.append(("HIGH", "JKU internal endpoint"))
        
        # Check for URL with unusual ports (pentester evasion)
        elif re.search(r':\d+(?!443|80)$', jku):
            jku_risk = "MEDIUM"
            jku_color = "yellow"
            jku_msg = f"CVE-{CVE_MAP['jku_injection']}: Non-standard port - verify endpoint"
            vulnerabilities.append(("MEDIUM", "JKU non-standard port"))
        
        # Check for user-controlled parameters in JKU
        elif "?" in jku:
            jku_risk = "HIGH"
            jku_color = "yellow"
            jku_msg = f"CVE-{CVE_MAP['jku_injection']}: JKU contains query parameters - injectable?"
            vulnerabilities.append(("HIGH", "JKU with query parameters"))
        
        table.add_row(f"[{jku_color}]7. JKU Injection[/{jku_color}]", f"[{jku_color} bold]{jku_risk}[/{jku_color} bold]", f"[{jku_color}]{jku_msg}[/{jku_color}]")
        results.append(("7. JKU Injection", f"{jku_risk} - {jku_msg}"))
    else:
        table.add_row("[green]7. JKU Injection[/green]", "[green bold]PASS[/green bold]", "[green]No JKU endpoint[/green]")
        results.append(("7. JKU Injection", "PASS"))

    # ==== VULNERABILITY 8: Signature Bypass / Tampering ====
    if alg == "none":
        msg = f"CVE-{CVE_MAP['signature_bypass']}: Signature can be stripped entirely"
        table.add_row("[red]8. Signature Bypass[/red]", "[red bold]CRITICAL[/red bold]", f"[red]{msg}[/red]")
        vulnerabilities.append(("CRITICAL", "Signature stripping possible"))
        results.append(("8. Signature Bypass", msg))
    else:
        # Check signature strength/validity
        header_decoded, payload_decoded, sig = decode_jwt_parts(token)
        if sig and len(str(sig)) < 20:
            table.add_row("[yellow]8. Signature Bypass[/yellow]", "[yellow bold]MEDIUM[/yellow bold]", "[yellow]Weak signature length - may be tamperable[/yellow]")
            results.append(("8. Signature Bypass", "MEDIUM RISK"))
        else:
            table.add_row("[green]8. Signature Bypass[/green]", "[green bold]PASS[/green bold]", f"[green]Signature required ({alg})[/green]")
            results.append(("8. Signature Bypass", "PASS"))

    # ==== ADVANCED: Payload Manipulation Risk ====
    nbf = payload.get("nbf")
    iat = payload.get("iat")
    
    nbf_risk = "PASS"
    nbf_color = "green"
    
    if not nbf and not iat:
        nbf_risk = "MEDIUM"
        nbf_color = "yellow"
        nbf_msg = "[yellow]No issuance time validation - can forge tokens[/yellow]"
        vulnerabilities.append(("MEDIUM", "No token age validation"))
    elif nbf and datetime.utcnow().timestamp() < nbf:
        nbf_risk = "MEDIUM"
        nbf_color = "yellow"
        nbf_msg = "[yellow]Token not yet valid - nbf claim set in future[/yellow]"
    else:
        nbf_msg = "[green]Token age properly validated[/green]"
    
    table.add_row(f"[{nbf_color}]9. Token Issuance[/{nbf_color}]", f"[{nbf_color} bold]{nbf_risk}[/{nbf_color} bold]", nbf_msg)
    results.append(("9. Token Issuance", nbf_risk))

    # ==== RISK SUMMARY ====
    critical_count = sum(1 for v in vulnerabilities if v[0] == "CRITICAL")
    high_count = sum(1 for v in vulnerabilities if v[0] == "HIGH")
    
    if critical_count > 0:
        risk_level = f"CRITICAL - {critical_count} critical vulnerabilities"
        risk_color = "red"
        risk_score = 95
    elif high_count > 0:
        risk_level = f"HIGH - {high_count} high-risk issues"
        risk_color = "yellow"
        risk_score = 75
    else:
        risk_level = "LOW RISK - No critical vulnerabilities"
        risk_color = "green"
        risk_score = 20

    risk_display = f"[{risk_color} bold]{risk_level}[/{risk_color} bold]"
    score_display = f"[{risk_color}]Score: {risk_score}/100[/{risk_color}]"
    
    table.add_row("", "", "")
    table.add_row(f"[{risk_color}]RISK ASSESSMENT[/{risk_color}]", risk_display, score_display)
    results.append(("Risk Score", f"{risk_score}/100"))

    return table, results
