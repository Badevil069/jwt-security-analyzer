# Advanced Security Mode - Pentester-Level Attacks

## 🔥 Advanced Attack Vectors Detected

Your JWT Analyzer now detects **9 critical attack vectors** including pentester-level techniques used by red teamers:

---

## 1️⃣ Algorithm Swap Attack (CVE-2016-5431)

### What It Does
Attacker switches from RS256 (asymmetric) to HS256 (symmetric), tricking the server into using the public key as HMAC secret.

### Example Attack
```
Original: RS256 with RSA private key (server has RSA public key)
Attack:   Change to HS256 with RSA public key as secret
Result:   Attacker can forge valid tokens!
```

### Detection in Your Tool
```
2. Algorithm Swap Attack │ HIGH/MEDIUM │ CVE-2016-5431
```

---

## 2️⃣ JKU Injection Attack (CVE-2020-28169, CVE-2021-22911)

### What It Does
JKU (JSON Key URL) header points to malicious JWKS endpoint attacker controls, allowing them to inject valid signing keys.

### Attack Variants

#### 🔴 **HTTP Endpoint (Man-in-the-Middle)**
```json
{
  "alg": "RS256",
  "jku": "http://attacker.com/jwks.json"  // NOT HTTPS!
}
```
✅ **YOUR TOOL DETECTS**: "Insecure HTTP endpoint - MITM possible"

#### 🟡 **Localhost Bypass (SSRF)**
```json
{
  "alg": "RS256", 
  "jku": "http://localhost:8080/jwks.json"  // Internal endpoint!
}
```
✅ **YOUR TOOL DETECTS**: "Internal network endpoint - possible bypass"

#### 🟡 **Non-standard Port**
```json
{
  "alg": "RS256",
  "jku": "https://api.example.com:9999/jwks.json"  // Unusual port
}
```
✅ **YOUR TOOL DETECTS**: "Non-standard port - verify endpoint"

#### 🟡 **Query Parameter Injection**
```json
{
  "alg": "RS256",
  "jku": "https://api.example.com/jwks?key=../../../etc/passwd"  // Injectable!
}
```
✅ **YOUR TOOL DETECTS**: "JKU contains query parameters - injectable?"

### Detection in Your Tool
```
7. JKU Injection          │ CRITICAL    │ CVE-2020-28169
                          │ HIGH        │ "Internal endpoint - possible bypass"
                          │ MEDIUM      │ "Non-standard port - verify"
```

---

## 3️⃣ KID Path Traversal Attack (CVE-2021-22911)

### What It Does
KID (Key ID) header used for path traversal or command injection, allowing attackers to:
- Read arbitrary files
- Execute commands
- Bypass authentication

### Attack Variants

#### 🔴 **Path Traversal**
```json
{
  "alg": "HS256",
  "kid": "../../etc/passwd"  // Read system files
}
```
✅ **YOUR TOOL DETECTS**: "KID contains path traversal/injection payload"

#### 🔴 **Command Injection**
```json
{
  "alg": "HS256",
  "kid": "key-id | cat /etc/passwd"  // Execute arbitrary commands
}
```
✅ **YOUR TOOL DETECTS**: Recognizes pipe `|`, semicolon `;`, backticks `` ` ``

#### 🔴 **Variable Expansion**
```json
{
  "alg": "HS256",
  "kid": "key-${PID}-$(id)"  // Shell variable expansion
}
```
✅ **YOUR TOOL DETECTS**: Recognizes `$` character patterns

#### 🔴 **SQL Injection (in KID context)**
```json
{
  "alg": "HS256",
  "kid": "key'; DROP TABLE users; --"  // SQL injection
}
```
✅ **YOUR TOOL DETECTS**: Pattern matching for injection payloads

### Regex Patterns Detected
```
Pattern         │ Attack Type
─────────────────────────────────
\.\.            │ Parent directory traversal
\./             │ Relative path
etc/passwd      │ Unix file read
\|              │ Command piping
;               │ Command chaining
`               │ Command substitution (backticks)
$               │ Variable expansion / command substitution
```

### Detection in Your Tool
```
6. KID Path Traversal     │ CRITICAL    │ CVE-2021-22911
                          │ HIGH        │ "KID parameter injection"
                          │ MEDIUM      │ "No KID claim present"
```

---

## 4️⃣ Key Confusion Attack (CVE-2015-9235)

Symmetric (HS256) vs Asymmetric (RS256) confusion:
```
4. Key Confusion          │ HIGH        │ Symmetric algorithm vulnerable to key exposure
```

---

## 5️⃣ Token Issuance Validation (nbf/iat Claims)

Missing `nbf` (not before) or `iat` (issued at) claims allows token forging:
```
9. Token Issuance         │ MEDIUM      │ No issuance time validation - can forge tokens
```

---

## 🧪 Test Vectors

### Test 1: JKU HTTP Injection
```bash
python main.py scan eyJhbGciOiJIUzI1NiIsImprdSI6Imh0dHA6Ly9hdHRhY2tlci5jb20vandrcy5qc29uIiwidHlwIjoiSldUIn0.eyJzdWIiOiIxMjM0NTY3ODkwIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.fZy3uZS0VZhD_k3i1FxSD-zC_V8ZSXLEEQU0MTL-LBo
```
**Expected**: 🔴 CRITICAL - JKU Injection detected

### Test 2: KID Path Traversal  
```bash
python main.py scan eyJhbGciOiJIUzI1NiIsImtpZCI6Ii4uLy4uL2V0Yy9wYXNzd2QiLCJ0eXAiOiJKV1QifQ.eyJzdWIiOiIxMjM0NTY3ODkwIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.9xTUv8j17iUKNtMr7gToD_ICcRwRuCUeOZ5m5RoK08wQ
```
**Expected**: 🔴 CRITICAL - KID Path Traversal detected

### Test 3: KID Command Injection
```bash
python main.py scan eyJhbGciOiJIUzI1NiIsImtpZCI6ImtleS1pZCB8IGNhdCAvZXRjL3Bhc3N3ZCIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.hZgSHQaksc_ctyhOB05xM21FtvlKgEWhwEwnJp0G-GA
```
**Expected**: 🔴 CRITICAL - KID injection payload detected

### Test 4: JKU Localhost Bypass
```bash
python main.py scan eyJhbGciOiJIUzI1NiIsImprdSI6Imh0dHA6Ly9sb2NhbGhvc3Q6ODA4MC9qd2tzLmpzb24iLCJ0eXAiOiJKV1QifQ.eyJzdWIiOiIxMjM0NTY3ODkwIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.b_8BglJrnAIdcX5JZK3odnVyL6JQP-dZIEZuaXSYys4
```
**Expected**: 🟡 HIGH - JKU localhost internal endpoint detected

---

## 📊 Risk Scoring

How machine scoring works:

```
Vulnerability Type         │ Count  │ Score Multiplier
──────────────────────────────────────────────────────
CRITICAL Vulnerabilities   │ 1+     │ 95/100 RISK
  - alg:none
  - Weak secrets (500+ match)
  - Missing expiration
  - KID path traversal
  - JKU HTTP endpoint
  - Signature stripping
  
HIGH Risk Issues           │ 1+     │ 75/100 RISK
  - Algorithm swap
  - Algorithm confusion
  - Key confusion (symmetric)
  - JKU localhost
  - KID injection
  
MEDIUM Risk Issues         │ 1+     │ 45/100 RISK
  - No KID claim
  - Token expired
  - Weak algorithm
  - Algorithm swap risk
  
PASS (No Risk)             │ All    │ 20/100 RISK
  - Proper algorithm
  - Strong secret
  - Valid expiration
  - No injection vectors
```

---

## 🎯 Pentester Workflow

```
1. Extract JWT from application
   └─ python main.py scan <token>

2. Review color-coded results:
   ├─ 🟢 GREEN = Safe (no action needed)
   ├─ 🟡 YELLOW = Caution (investigate)
   └─ 🔴 RED = Critical (exploit immediately)

3. Check specific vulnerabilities:
   ├─ alg:none? ──→ Bypass completely
   ├─ Weak secret? ──→ Forge tokens
   ├─ JKU injection? ──→ SSRF/MITM
   ├─ KID traversal? ──→ RCE/LFI
   └─ No expiration? ──→ Indefinite access

4. Exploitation techniques:
   ├─ Use jwt.io with detected weak secret
   ├─ Craft malicious JKU endpoint
   ├─ Create KID with payload
   └─ Forward to vulnerable endpoint

5. Generate report:
   └─ report.pdf created automatically
```

---

## 🔐 Remediation Guidance

| Vulnerability | Remediation |
|---|---|
| **alg:none** | Enforce algorithm validation; reject "none" |
| **Algorithm swap** | Whitelist specific algorithms (RS256 only) |
| **Weak secrets** | Use 32+ character random keys for HS256 |
| **JKU injection** | Hardcode JWKS endpoint; validate HTTPS only |
| **KID traversal** | Validate KID against whitelist; sanitize input |
| **Missing exp** | Always include `exp`, `nbf`, `iat` claims |
| **No signature validation** | Always verify signature before trusting token |
| **Key confusion** | Use asymmetric algorithms (RS256/ES256) |

---

## 🛠️ Advanced Mode Features

✅ **9-Vector Analysis**: Covers all major JWT attack vectors  
✅ **Regex Pattern Matching**: Detects injection payloads  
✅ **SSRF Detection**: Identifies localhost/private IP bypasses  
✅ **CVE Mapping**: Every finding mapped to CVE  
✅ **Color-Coded Output**: Visual risk assessment  
✅ **Pentester-Optimized**: Detection for exploitation techniques  
✅ **OWASP Aligned**: Matches OWASP JWT testing guidelines  

---

## 📚 References

- **CVE-2016-5431**: JWT algorithm confusion attacks
- **CVE-2020-28169**: JKU endpoint injection and KID manipulation
- **CVE-2021-22911**: JWKS endpoint abuse
- **CVE-2015-9235**: Signature bypass and alg:none vulnerability
- **Auth0 JWT Security**: https://auth0.com/blog/critical-vulnerabilities-in-json-web-token-libraries/
- **OWASP JWT Cheat Sheet**: https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html

---

**Your JWT Analyzer is now a professional-grade pentesting tool!** 🚀
