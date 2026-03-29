"""Check for signature bypass vulnerabilities"""

import jwt


def check_signature_bypass(token: str) -> dict:
    """
    Check if signature verification can be bypassed.
    
    Args:
        token: JWT token string
        
    Returns:
        Dictionary with vulnerability details
    """
    try:
        header = jwt.get_unverified_header(token)
        alg = header.get("alg")
        
        if alg == "none":
            return {
                "name": "8. Signature Bypass",
                "status": "CRITICAL",
                "detail": "alg:none - signature not required",
                "cve": None
            }
        
        return {
            "name": "8. Signature Bypass",
            "status": "PASS",
            "detail": f"Signature required ({alg})",
            "cve": None
        }
    except Exception:
        return None
