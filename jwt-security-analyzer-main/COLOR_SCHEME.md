# JWT Analyzer - Color Coding Guide

## Color Scheme by Risk Level

### 🟢 GREEN - PASS (No Risk)
- **Text Color**: Green
- **Indicators**: ✓
- **Examples**:
  - "Algorithm set properly"
  - "No weak secrets matched"
  - "Signature required (HS256)"
  - "No JKU endpoint"
  
When a security check **PASSES**, the entire vulnerability row will display in **GREEN**.

---

### 🟡 YELLOW - MEDIUM Risk (Caution Required)
- **Text Color**: Yellow/Orange
- **Indicators**: ⚠️
- **Examples**:
  - "No KID claim present"
  - "Token is expired"
  - "Algorithm Confusion risk"

When there's a **MEDIUM risk**, the row will display in **YELLOW**.

---

### 🔴 RED - CRITICAL/HIGH Risk (Immediate Action)
- **Text Color**: Red
- **Indicators**: 🚨
- **Examples**:
  - "CVE-2015-9235: No signature validation" (alg:none)
  - "CVE-2014-9721: Secret matched in 500+ signatures" (weak secret)
  - "CVE-2020-28169: No expiration claim"
  - "CVE-2020-28169: KID parameter injectable"
  - "CVE-2021-22911: Insecure JKU endpoint (HTTP)"

When there are **CRITICAL or HIGH risks**, the row will display in **RED**.

---

## Risk Assessment Row (Final Summary)

### Color by Overall Risk Score:
- **🟢 GREEN**: Score 0-29 (LOW RISK)
  - "LOW RISK - No critical vulnerabilities"
  
- **🟡 YELLOW**: Score 30-69 (MEDIUM RISK)
  - "MEDIUM RISK - High-risk issues found"
  
- **🔴 RED**: Score 70-100 (CRITICAL RISK)
  - "HIGH RISK - Critical vulnerabilities found"
  - "CRITICAL - [X] critical vulnerabilities"

---

## 8 Vulnerabilities - Color Display

| # | Vulnerability | PASS (Green) | Risk (Red/Yellow) |
|---|---|---|---|
| 1 | None Algorithm | ✓ Algorithm set properly | 🔴 No signature validation |
| 2 | Algorithm Confusion | ✓ No confusion vectors | 🟡 RS256 confusion risk |
| 3 | Weak HMAC Secret | ✓ No weak secrets matched | 🔴 Secret matched (500+ sigs) |
| 4 | Key Confusion | ✓ Asymmetric algorithm | 🟡 Symmetric key exposure risk |
| 5 | Token Expiration | ✓ Valid until [date] | 🔴 No exp claim OR 🟡 Expired |
| 6 | KID Injection | ✓ KID (validated) | 🔴 KID parameter injectable |
| 7 | Signature Bypass | ✓ Signature required | 🔴 Signature can be stripped |
| 8 | JWKS Endpoint | ✓ No JKU endpoint | 🔴 Insecure JKU (HTTP) |

---

## Example Terminal Output

```
              JWT Security Analysis Report              
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Vulnerability   ┃ Status  ┃ Details & CVE              ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 1. None Algorithm    │ [GREEN]PASS[/GREEN]   │ [GREEN]Proper[/GREEN]  │
│ 2. Algorithm Conf.   │ [YELLOW]MEDIUM[/YELLOW] │ [YELLOW]Risk detected[/YELLOW] │
│ 3. Weak HMAC Secret  │ [RED]CRITICAL[/RED]   │ [RED]Secret matched[/RED] │
│ 4. Key Confusion     │ [GREEN]PASS[/GREEN]   │ [GREEN]Safe[/GREEN]    │
│ 5. Token Expiration  │ [RED]CRITICAL[/RED]   │ [RED]No exp claim[/RED] │
│ Risk Assessment      │ [RED]CRITICAL[/RED]   │ [RED]Score: 95/100[/RED] │
└─────────────────────┴─────────┴────────────────────────┘
```

---

## How to Read the Report

1. **Count the COLORS**:
   - All GREEN = Safe token ✓
   - Any RED = Critical issues ⚠️
   - Any YELLOW = Be cautious ⚡

2. **Check the Risk Score** at the bottom:
   - 0-29 = Low impact (green)
   - 30-69 = Medium risk (yellow)
   - 70-100 = Critical (red)

3. **Review CVE References**:
   - Each vulnerability is mapped to actual CVEs
   - Use these for compliance/reporting

---

## Color Quick Reference

```
GREEN  = No vulnerabilities found in this check ✓
YELLOW = Warning, medium risk ⚠️  
RED    = Danger, critical vulnerabilities detected 🚨
```

---

## Testing the Colors

### Test 1: Safe Token (Mostly Green)
```bash
python main.py scan <valid-high-entropy-hs256-token>
```

### Test 2: Weak Secret Token (Red)
```bash
python main.py scan eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkFkbWluIFVzZXIiLCJlbWFpbCI6ImFkbWluQGV4YW1wbGUuY29tIiwiaWF0IjoxNTE2MjM5MDIyfQ.M2T6vPgzfDxo8y9jfenRwHhX2f7iyObQ2qZMIsmitrQ
```

### Test 3: alg:none Token (Critical Red)
```bash
python -c "import jwt; print(jwt.encode({'sub': '123', 'admin': True}, '', algorithm='none'))" | xargs -I {} python main.py scan {}
```

---

**Remember**: Green = Safe ✓ | Yellow = Caution ⚠️ | Red = Action Required 🚨
