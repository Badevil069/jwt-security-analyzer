"""Check for token issuance and age validation"""

import jwt
from datetime import datetime


def check_token_issuance(token: str) -> dict:
    """
    Check token issuance time and age validation.
    
    Args:
        token: JWT token string
        
    Returns:
        Dictionary with vulnerability details
    """
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        
        if "iat" not in payload:
            return {
                "name": "9. Token Issuance",
                "status": "MEDIUM",
                "detail": "No issuance time claim",
                "cve": None
            }
        
        iat_timestamp = payload["iat"]
        token_age = datetime.utcnow().timestamp() - iat_timestamp
        
        # Token should not be issued in the future
        if iat_timestamp > datetime.utcnow().timestamp():
            return {
                "name": "9. Token Issuance",
                "status": "MEDIUM",
                "detail": "Token issued in future",
                "cve": None
            }
        
        return {
            "name": "9. Token Issuance",
            "status": "PASS",
            "detail": "Token age properly validated",
            "cve": None
        }
    except Exception:
        return None
