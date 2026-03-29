"""Check for expired or missing expiration claims"""

import jwt
from datetime import datetime


def check_expiration(token: str) -> dict:
    """
    Check if JWT has expiration claim and if it's expired.
    
    Args:
        token: JWT token string
        
    Returns:
        Dictionary with vulnerability details or None
    """
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        
        if "exp" not in payload:
            return {
                "name": "5. Token Expiration",
                "status": "CRITICAL",
                "detail": "No expiration claim",
                "cve": "CVE-2020-28169"
            }
        
        exp_timestamp = payload["exp"]
        exp_datetime = datetime.utcfromtimestamp(exp_timestamp)
        
        if datetime.utcnow() > exp_datetime:
            return {
                "name": "5. Token Expiration",
                "status": "CRITICAL",
                "detail": f"Token expired at {exp_datetime.isoformat()}",
                "cve": None
            }
        
        return {
            "name": "5. Token Expiration",
            "status": "PASS",
            "detail": f"Token valid until {exp_datetime.isoformat()}",
            "cve": None
        }
    except Exception as e:
        return {
            "name": "5. Token Expiration",
            "status": "MEDIUM",
            "detail": "Could not verify expiration",
            "cve": None
        }
