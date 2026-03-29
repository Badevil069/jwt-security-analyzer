"""JWT Token Scanner and Analysis Engine"""

import jwt
import warnings
from rich.table import Table

from .checks import (
    check_none_algorithm,
    check_weak_secret,
    check_expiration,
    check_algorithm_swap,
    check_key_confusion,
    check_kid_injection,
    check_jku_injection,
    check_signature_bypass,
    check_token_issuance,
)


def _colorize_status(status: str) -> str:
    """Apply color to status based on severity level."""
    color_map = {
        "CRITICAL": "[red]CRITICAL[/red]",
        "HIGH": "[orange1]HIGH[/orange1]",
        "MEDIUM": "[yellow]MEDIUM[/yellow]",
        "PASS": "[green]PASS[/green]",
    }
    return color_map.get(status, status)


def _colorize_detail(detail: str, status: str) -> str:
    """Apply color to detail text based on status."""
    if status == "CRITICAL":
        return f"[red]{detail}[/red]"
    elif status == "HIGH":
        return f"[orange1]{detail}[/orange1]"
    elif status == "MEDIUM":
        return f"[yellow]{detail}[/yellow]"
    elif status == "PASS":
        return f"[green]{detail}[/green]"
    return detail


def analyze_token(token: str, secrets_file: str = "secrets.txt") -> tuple[Table, list, dict]:
    """
    Analyze a JWT token for security vulnerabilities.
    
    Args:
        token: JWT token string
        secrets_file: Path to weak secrets file
        
    Returns:
        Tuple of (rich.Table for display, list of check results, risk assessment dict)
    """
    results = []
    
    # Suppress security warnings
    warnings.filterwarnings('ignore', message='.*HMAC key.*')
    
    table = Table(title="JWT Security Analysis")
    table.add_column("Vulnerability", style="cyan")
    table.add_column("Status", style="white")
    table.add_column("Details & CVE", style="white")
    
    try:
        jwt.get_unverified_header(token)
    except Exception:
        table.add_row("Token Validation", "[red]FAIL[/red]", "[red]Invalid JWT format[/red]")
        return table, [{"name": "Token Validation", "status": "FAIL", "detail": "Invalid JWT", "cve": None}], {"critical_count": 1, "score": 0}
    
    # Run all 9 security checks
    checks = [
        (check_none_algorithm, [token]),
        (check_algorithm_swap, [token]),
        (check_weak_secret, [token, secrets_file]),
        (check_key_confusion, [token]),
        (check_expiration, [token]),
        (check_kid_injection, [token]),
        (check_jku_injection, [token]),
        (check_signature_bypass, [token]),
        (check_token_issuance, [token]),
    ]
    
    for check_func, args in checks:
        result = check_func(*args)
        if result:
            results.append(result)
            
            # Format CVE info
            cve_info = f" | {result['cve']}" if result.get('cve') else ""
            
            # Apply colors
            colored_status = _colorize_status(result['status'])
            colored_detail = _colorize_detail(f"{result['detail']}{cve_info}", result['status'])
            
            table.add_row(
                result['name'],
                colored_status,
                colored_detail
            )
    
    # Calculate risk assessment
    critical_count = sum(1 for r in results if r['status'] == 'CRITICAL')
    high_count = sum(1 for r in results if r['status'] == 'HIGH')
    medium_count = sum(1 for r in results if r['status'] == 'MEDIUM')
    pass_count = sum(1 for r in results if r['status'] == 'PASS')
    
    # Calculate overall score (out of 100)
    score = max(0, 100 - (critical_count * 25 + high_count * 15 + medium_count * 5))
    
    # Determine risk level
    if critical_count > 0:
        risk_level = f"CRITICAL - {critical_count} critical"
        risk_level_colored = f"[red]CRITICAL - {critical_count} critical[/red]"
    elif high_count > 0:
        risk_level = f"HIGH - {high_count} high"
        risk_level_colored = f"[orange1]HIGH - {high_count} high[/orange1]"
    elif medium_count > 0:
        risk_level = f"MEDIUM - {medium_count} medium"
        risk_level_colored = f"[yellow]MEDIUM - {medium_count} medium[/yellow]"
    else:
        risk_level = "LOW"
        risk_level_colored = "[green]LOW[/green]"
    
    # Color score based on value
    if score >= 80:
        score_colored = f"[green]Score: {score}/100[/green]"
    elif score >= 60:
        score_colored = f"[yellow]Score: {score}/100[/yellow]"
    elif score >= 40:
        score_colored = f"[orange1]Score: {score}/100[/orange1]"
    else:
        score_colored = f"[red]Score: {score}/100[/red]"
    
    # Add risk assessment row
    table.add_row(
        "RISK ASSESSMENT",
        risk_level_colored,
        score_colored
    )
    
    risk_assessment = {
        "critical_count": critical_count,
        "high_count": high_count,
        "medium_count": medium_count,
        "pass_count": pass_count,
        "score": score,
        "risk_level": risk_level
    }
    
    return table, results, risk_assessment


def run_scanner(token: str, secrets_file: str = "secrets.txt") -> Table:
    """
    Run the scanner and return the analysis table.
    
    Convenience function that wraps analyze_token and returns only the table.
    
    Args:
        token: JWT token string
        secrets_file: Path to weak secrets file
        
    Returns:
        Rich Table containing the analysis results
    """
    table, _, _ = analyze_token(token, secrets_file)
    return table
