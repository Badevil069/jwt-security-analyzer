"""JWT Analyzer Package

A production-grade JWT security analyzer with modular checks,
clean architecture, and extensibility built-in.
"""

__version__ = "1.0.0"
__author__ = "Security Team"

from .cli import cli
from .scanner import analyze_token

__all__ = ["cli", "analyze_token"]
