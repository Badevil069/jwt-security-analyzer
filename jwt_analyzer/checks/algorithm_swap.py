"""Check for algorithm confusion/swap attacks"""

import jwt


def check_algorithm_swap(token: str) -> dict:
    """
    Check if token uses symmetric algorithm vulnerable to algorithm swap attacks.
    
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
                "name": "2. Algorithm Swap Attack",
                "status": "MEDIUM",
                "detail": "Symmetric algorithm - swap risk present",
                "cve": None
            }
        return None
    except Exception:
        return None
