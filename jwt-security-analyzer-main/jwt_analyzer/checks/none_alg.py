"""Check for alg:none vulnerability"""

import jwt


def check_none_algorithm(token: str) -> dict:
    """
    Check if JWT uses the 'none' algorithm (no signature required).
    
    Args:
        token: JWT token string
        
    Returns:
        Dictionary with vulnerability details or None
    """
    try:
        header = jwt.get_unverified_header(token)
        alg = header.get("alg")
        
        if alg == "none":
            return {
                "name": "1. None Algorithm",
                "status": "CRITICAL",
                "detail": "alg:none vulnerability detected",
                "cve": None
            }
        
        return {
            "name": "1. None Algorithm",
            "status": "PASS",
            "detail": "Algorithm set properly",
            "cve": None
        }
    except Exception:
        return None
