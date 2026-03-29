"""JWT Security Checks Module

Extensible check system for JWT vulnerabilities.
"""

from .none_alg import check_none_algorithm
from .weak_secret import check_weak_secret
from .expiration import check_expiration
from .algorithm_swap import check_algorithm_swap
from .key_confusion import check_key_confusion
from .kid_injection import check_kid_injection
from .jku_injection import check_jku_injection
from .signature_bypass import check_signature_bypass
from .token_issuance import check_token_issuance

__all__ = [
    "check_none_algorithm",
    "check_weak_secret",
    "check_expiration",
    "check_algorithm_swap",
    "check_key_confusion",
    "check_kid_injection",
    "check_jku_injection",
    "check_signature_bypass",
    "check_token_issuance",
]
