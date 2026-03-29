"""PDF Report Generation"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime
from rich import print


def generate_pdf(results, risk_assessment, filename="report.pdf"):
    """
    Generate professional security report PDF.
    
    Args:
        results: List of vulnerability check dictionaries
        risk_assessment: Dictionary with risk assessment details
        filename: Output PDF filename
    """
    try:
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        
        # Header
        c.setFont("Helvetica-Bold", 16)
        c.drawString(40, height - 50, "JWT Security Analysis Report")
        
        # Metadata
        c.setFont("Helvetica", 10)
        c.drawString(40, height - 70, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        c.drawString(40, height - 85, f"Overall Risk Score: {risk_assessment['score']}/100")
        c.drawString(40, height - 100, f"Risk Level: {risk_assessment['risk_level']}")
        
        # Separator
        c.line(40, height - 110, width - 40, height - 110)
        
        # Findings
        c.setFont("Helvetica-Bold", 11)
        c.drawString(40, height - 130, "JWT Vulnerability Assessment:")
        
        y_position = height - 150
        c.setFont("Helvetica", 9)
        
        for check in results:
            # Format: Vulnerability | Status | CVE
            text = f"{check['name']} [{check['status']}]"
            if check.get('cve'):
                text += f" {check['cve']}"
            
            # Add detail on next line
            detail = f"  → {check['detail']}"
            
            c.drawString(50, y_position, text)
            y_position -= 12
            c.drawString(50, y_position, detail)
            y_position -= 12
            
            if y_position < 50:
                c.showPage()
                y_position = height - 50
        
        # Risk Assessment Summary
        y_position -= 20
        if y_position < 100:
            c.showPage()
            y_position = height - 50
        
        c.setFont("Helvetica-Bold", 11)
        c.drawString(40, y_position, "Risk Assessment Summary")
        y_position -= 20
        
        c.setFont("Helvetica", 10)
        c.drawString(50, y_position, f"Critical Vulnerabilities: {risk_assessment['critical_count']}")
        y_position -= 15
        c.drawString(50, y_position, f"High Vulnerabilities: {risk_assessment['high_count']}")
        y_position -= 15
        c.drawString(50, y_position, f"Medium Vulnerabilities: {risk_assessment['medium_count']}")
        y_position -= 15
        c.drawString(50, y_position, f"Passed Checks: {risk_assessment['pass_count']}")
        y_position -= 15
        c.drawString(50, y_position, f"Overall Score: {risk_assessment['score']}/100")
        
        # Footer
        c.setFont("Helvetica-Oblique", 8)
        c.drawString(40, 20, "[WARNING] For authorized security testing only. Analyze responsibly.")
        
        c.save()
        print(f"[bold green]PDF report saved as {filename}[/bold green]")
    except Exception as e:
        print(f"[bold red]Error generating PDF: {str(e)}[/bold red]")
