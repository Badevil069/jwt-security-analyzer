#!/usr/bin/env python
"""JWT Analyzer Entry Point

This is the main executable entry point for the JWT Security Analyzer.
The core logic is implemented in the jwt_analyzer package.
"""

from jwt_analyzer import cli


if __name__ == "__main__":
    cli()