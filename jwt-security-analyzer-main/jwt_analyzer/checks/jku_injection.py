"""Check for JKU injection vulnerabilities"""

import jwt


def check_jku_injection(token: str) -> dict:
    """
    Check for JKU (JSON Web Key URL) injection vulnerability.
    
    Args:
        token: JWT token string
        
    Returns:
        Dictionary with vulnerability details
    """
    try:
        header = jwt.get_unverified_header(token)
        jku = header.get("jku")
        
        if not jku:
            return {
                "name": "7. JKU Injection",
                "status": "PASS",
                "detail": "No JKU endpoint",
                "cve": None
            }
        
        # If JKU uses http (not https)
        if jku.startswith("http://"):
            return {
                "name": "7. JKU Injection",
                "status": "HIGH",
                "detail": "JKU uses insecure HTTP",
                "cve": None
            }
        
        return {
            "name": "7. JKU Injection",
            "status": "MEDIUM",
            "detail": "JKU endpoint present - requires verification",
            "cve": None
        }
    except Exception:
        return None
