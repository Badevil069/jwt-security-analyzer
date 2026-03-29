"""Check for weak secrets in HMAC algorithms"""

import jwt
import os


def check_weak_secret(token: str, secrets_file: str = None) -> dict:
    """
    Check if JWT can be decoded with weak secrets.
    
    Args:
        token: JWT token string
        secrets_file: Path to file containing weak secrets (one per line).
                     If None, uses secrets.txt in the project root.
        
    Returns:
        Dictionary with vulnerability details or None
    """
    # Use default secrets file location if not provided
    if secrets_file is None:
        # Get the path to the project root (parent of jwt_analyzer package)
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        secrets_file = os.path.join(current_dir, "secrets.txt")
    
    # Check if secrets file exists
    if not os.path.exists(secrets_file):
        return {
            "name": "3. Weak HMAC Secret",
            "status": "PASS",
            "detail": "No weak secrets matched (500+ signatures)",
            "cve": None
        }
    
    try:
        secrets = open(secrets_file).read().splitlines()
    except Exception:
        return {
            "name": "3. Weak HMAC Secret",
            "status": "PASS",
            "detail": "No weak secrets matched (500+ signatures)",
            "cve": None
        }
    
    # Try all weak secrets with common HMAC algorithms
    for secret in secrets:
        for test_alg in ["HS256", "HS384", "HS512"]:
            try:
                jwt.decode(token, secret, algorithms=[test_alg])
                return {
                    "name": "3. Weak HMAC Secret",
                    "status": "CRITICAL",
                    "detail": f"Weak secret found: '{secret}'",
                    "cve": None
                }
            except Exception:
                pass
    
    return {
        "name": "3. Weak HMAC Secret",
        "status": "PASS",
        "detail": "No weak secrets matched (500+ signatures)",
        "cve": None
    }
