"""Check for key confusion vulnerabilities"""

import jwt


def check_key_confusion(token: str) -> dict:
    """
    Check for key confusion vulnerability (CVE-2015-9235).
    
    Args:
        token: JWT token string
        
    Returns:
        Dictionary with vulnerability details
    """
    try:
        header = jwt.get_unverified_header(token)
        alg = header.get("alg")
        
        if alg and alg.startswith("HS"):
            return {
                "name": "4. Key Confusion",
                "status": "HIGH",
                "detail": "Symmetric algorithm vulnerable to key exposure",
                "cve": "CVE-2015-9235"
            }
        return None
    except Exception:
        return None
