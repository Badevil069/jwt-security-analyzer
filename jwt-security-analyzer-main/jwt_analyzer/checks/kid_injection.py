"""Check for KID path traversal vulnerabilities"""

import jwt


def check_kid_injection(token: str) -> dict:
    """
    Check for KID (Key ID) path traversal vulnerability.
    
    Args:
        token: JWT token string
        
    Returns:
        Dictionary with vulnerability details
    """
    try:
        header = jwt.get_unverified_header(token)
        kid = header.get("kid")
        
        if not kid:
            return {
                "name": "6. KID Path Traversal",
                "status": "MEDIUM",
                "detail": "No KID claim (JWKS matching impossible)",
                "cve": None
            }
        
        # If KID contains path traversal patterns
        if "../" in kid or ".." in kid:
            return {
                "name": "6. KID Path Traversal",
                "status": "HIGH",
                "detail": "Potential KID path traversal detected",
                "cve": None
            }
        
        return {
            "name": "6. KID Path Traversal",
            "status": "MEDIUM",
            "detail": "KID present - requires verification",
            "cve": None
        }
    except Exception:
        return None
