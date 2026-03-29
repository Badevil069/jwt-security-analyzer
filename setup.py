#!/usr/bin/env python
"""
Setup configuration for JWT Security Analyzer
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="jwt-analyzer",
    version="1.0.0",
    author="Security Team",
    description="Production-grade JWT security analyzer with 9 critical vulnerability detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/jwt-analyzer",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8+",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Topic :: Internet :: WWW/HTTP",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pyjwt>=2.8.1",
        "cryptography>=41.0.7",
        "click>=8.1.7",
        "rich>=13.7.0",
        "reportlab>=4.0.9",
    ],
    entry_points={
        "console_scripts": [
            "jwt-analyzer=jwt_analyzer.cli:cli",
            "jwt=jwt_analyzer.cli:cli",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["secrets.txt"],
    },
)
