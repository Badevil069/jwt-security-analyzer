# JWT Analyzer - Linux Setup Guide

This guide provides complete instructions for running the JWT Security Analyzer on Linux systems.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/jwt-security-analyzer.git
cd jwt-security-analyzer
```

### 2. Create a Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Running the Analyzer

### Basic Usage

#### Scan a Token with Interactive Output
```bash
python main.py scan <YOUR_JWT_TOKEN_HERE>
```

#### Output as JSON
```bash
python main.py scan <YOUR_JWT_TOKEN_HERE> --json
```

#### Specify Custom PDF Report Name
```bash
python main.py scan <YOUR_JWT_TOKEN_HERE> -o my_report.pdf
```

#### Suppress Banner
```bash
python main.py scan <YOUR_JWT_TOKEN_HERE> --no-banner
```

### Example Token
```bash
python main.py scan "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
```

## Docker Setup (Optional)

### Build Docker Image
```bash
docker build -t jwt-analyzer .
```

### Run with Docker
```bash
docker run jwt-analyzer scan <YOUR_JWT_TOKEN_HERE>
```

### Run with Report Output
```bash
docker run -v $(pwd)/reports:/app/reports jwt-analyzer scan <YOUR_JWT_TOKEN_HERE>
```

## Creating a CLI Alias (Optional)

To use `jwt` command directly instead of `python main.py`:

### For Bash
Add the following to `~/.bashrc`:
```bash
alias jwt='python /path/to/jwt-security-analyzer/main.py'
```

Then reload:
```bash
source ~/.bashrc
```

### For Zsh
Add the following to `~/.zshrc`:
```bash
alias jwt='python /path/to/jwt-security-analyzer/main.py'
```

Then reload:
```bash
source ~/.zshrc
```

## Troubleshooting

### Module Not Found Error
If you get `ModuleNotFoundError: No module named 'jwt_analyzer'`, ensure:
1. You're in the correct directory (jwt-security-analyzer root)
2. Virtual environment is activated (if using one)
3. Dependencies are installed: `pip install -r requirements.txt`

### Secrets File Not Found Warning
The analyzer automatically locates `secrets.txt` in the project root. If you get warnings:
1. Verify `secrets.txt` exists in the project root
2. Ensure proper file permissions: `chmod 644 secrets.txt`

### Permission Denied on Script Files
If you need to make scripts executable:
```bash
chmod +x main.py
chmod +x jwt_analyzer/cli.py
```

### Python Version Issues
Ensure you're using Python 3.8 or higher:
```bash
python3 --version
```

If needed, explicitly use `python3` instead of `python`:
```bash
python3 main.py scan <TOKEN>
```

## Running Tests

```bash
python -m pytest tests/ -v
```

## Project Structure

```
jwt-security-analyzer/
├── main.py                          # Entry point
├── requirements.txt                 # Python dependencies
├── secrets.txt                      # Weak secrets for testing
├── jwt_analyzer/
│   ├── __init__.py
│   ├── cli.py                       # Command-line interface
│   ├── scanner.py                   # Core analysis engine
│   ├── report.py                    # PDF report generation
│   └── checks/                      # Security checks
│       ├── algorithm_swap.py
│       ├── expiration.py
│       ├── jku_injection.py
│       ├── key_confusion.py
│       ├── kid_injection.py
│       ├── none_alg.py
│       ├── signature_bypass.py
│       ├── token_issuance.py
│       └── weak_secret.py
└── tests/
    └── test_scanner.py              # Unit tests
```

## Next Steps

- Review vulnerabilities found in your JWT tokens
- Check the generated PDF reports in the project root
- Test with the example token above
- Add custom weak secrets to `secrets.txt` if needed

## Additional Documentation

- [README.md](README.md) - Full project overview
- [ADVANCED_MODE.md](ADVANCED_MODE.md) - Advanced usage guide
- [CLI_SETUP.md](CLI_SETUP.md) - CLI configuration details
