from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime
import os
from app.core.config import settings

def generate_share_certificate(issuance_data: dict, shareholder_data: dict) -> BytesIO:
    """Generate a PDF share certificate"""
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    
    # Set up styles
    styles = getSampleStyleSheet()
    
    # Certificate Header
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawCentredString(300, 750, "SHARE CERTIFICATE")
    
    # Company Info
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 700, f"Company: {settings.COMPANY_NAME}")
    pdf.drawString(100, 680, f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    
    # Certificate Number
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(100, 650, f"Certificate No: {issuance_data['id']}")
    
    # Shareholder Info
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 620, f"This certifies that {shareholder_data['full_name']}")
    pdf.drawString(100, 600, f"is the registered owner of {issuance_data['number_of_shares']} shares")
    
    # Share Details Table
    data = [
        ["Shareholder ID", shareholder_data['id']],
        ["Issue Date", issuance_data['issue_date'].strftime('%Y-%m-%d')],
        ["Number of Shares", str(issuance_data['number_of_shares'])],
        ["Price Per Share", f"${issuance_data['price_per_share']:.2f}" if issuance_data['price_per_share'] else "N/A"],
    ]
    
    table = Table(data, colWidths=[200, 200])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    table.wrapOn(pdf, 100, 550)
    table.drawOn(pdf, 100, 550)
    
    # Footer
    pdf.setFont("Helvetica-Oblique", 10)
    pdf.drawString(100, 100, "This is an electronically generated certificate")
    pdf.drawString(100, 80, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    pdf.save()
    buffer.seek(0)
    return buffer