"""Tests for JWT Scanner Module"""

import pytest
from jwt_analyzer.scanner import run_scanner, analyze_token


TEST_TOKEN = (
    "eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9."
    "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0."
    "owv7q9nVbW5tqUezF_G2nHTra-ANW3HqW9epyVwh08Y-Z-FKsnG8eBIpC4GTfTVU"
)


def test_scanner_runs():
    """Test that scanner runs and returns a non-None table"""
    table = run_scanner(TEST_TOKEN)
    assert table is not None


def test_scanner_returns_table_with_rows():
    """Test that scanner returns table with analysis rows"""
    table = run_scanner(TEST_TOKEN)
    # Rich Table object should have rows
    assert hasattr(table, 'rows')
    assert len(table.rows) > 0


def test_scanner_handles_invalid_token():
    """Test that scanner gracefully handles invalid tokens"""
    invalid_token = "not.a.jwt"
    table = run_scanner(invalid_token)
    assert table is not None


def test_analyze_token_returns_complete_results():
    """Test that analyze_token returns table, results, and risk assessment"""
    table, results, risk_assessment = analyze_token(TEST_TOKEN)
    
    assert table is not None
    assert isinstance(results, list)
    assert len(results) == 9  # 9 checks
    assert isinstance(risk_assessment, dict)
    assert 'score' in risk_assessment
    assert 'risk_level' in risk_assessment
    assert 'critical_count' in risk_assessment


def test_risk_assessment_calculations():
    """Test that risk assessment scores are calculated correctly"""
    table, results, risk_assessment = analyze_token(TEST_TOKEN)
    
    # Verify score is between 0-100
    assert 0 <= risk_assessment['score'] <= 100
    
    # Verify counts add up to number of checks
    total_checks = (
        risk_assessment['critical_count'] +
        risk_assessment['high_count'] +
        risk_assessment['medium_count'] +
        risk_assessment['pass_count']
    )
    assert total_checks == 9
