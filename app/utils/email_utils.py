from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from app.core.config import settings
import smtplib
from typing import Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def create_email_template(shareholder_name: str, issuance_data: dict) -> str:
    """Generate beautiful HTML email template"""
    # Handle price formatting safely
    price_per_share = issuance_data.get('price_per_share')
    price_display = f"${price_per_share:.2f}" if price_per_share is not None else "N/A"
    
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Share Certificate</title>
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', sans-serif; background-color: #f4f4f4;">

    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f4f4; padding: 40px 0;">
        <tr>
            <td align="center">
                <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 0 10px rgba(0,0,0,0.05);">
                    
                    <!-- Header -->
                    <tr>
                        <td style="background-color: #2d89ef; color: white; padding: 20px; text-align: center;">
                            <h2 style="margin: 0; font-size: 24px;">Your Share Certificate</h2>
                        </td>
                    </tr>

                    <!-- Content -->
                    <tr>
                        <td style="padding: 30px;">
                            <p style="font-size: 16px; color: #333;">Dear <strong>{shareholder_name}</strong>,</p>

                            <p style="font-size: 16px; color: #333;">
                                We're pleased to inform you that your share certificate is now ready.
                            </p>

                            <table cellpadding="0" cellspacing="0" width="100%" style="margin-top: 20px; border: 1px solid #ddd; border-radius: 6px;">
                                <tr>
                                    <td colspan="2" style="background-color: #f9f9f9; padding: 10px 15px; border-bottom: 1px solid #ddd;">
                                        <h3 style="margin: 0; font-size: 18px; color: #444;">Certificate Details</h3>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding: 12px 15px; font-weight: bold; color: #555;">Certificate ID:</td>
                                    <td style="padding: 12px 15px; color: #333;">{issuance_data['id']}</td>
                                </tr>
                                <tr style="background-color: #fafafa;">
                                    <td style="padding: 12px 15px; font-weight: bold; color: #555;">Number of Shares:</td>
                                    <td style="padding: 12px 15px; color: #333;">{issuance_data['number_of_shares']}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 12px 15px; font-weight: bold; color: #555;">Issue Date:</td>
                                    <td style="padding: 12px 15px; color: #333;">{issuance_data['issue_date'].strftime('%B %d, %Y')}</td>
                                </tr>
                                <tr style="background-color: #fafafa;">
                                    <td style="padding: 12px 15px; font-weight: bold; color: #555;">Price Per Share:</td>
                                    <td style="padding: 12px 15px; color: #333;">{price_display}</td>
                                </tr>
                            </table>

                            <p style="margin-top: 25px; font-size: 16px; color: #333;">
                                You can also download your certificate anytime from your account dashboard.
                            </p>

                            <p style="font-size: 16px; color: #333;">
                                Thank you for being a valued shareholder.
                            </p>
                        </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f4f4f4; text-align: center; padding: 20px; font-size: 13px; color: #888;">
                            &copy; {datetime.now().year} {settings.COMPANY_NAME}. All rights reserved.
                        </td>
                    </tr>

                </table>
            </td>
        </tr>
    </table>

</body>
</html>
    """
def send_certificate_email(
    to_email: str,
    shareholder_name: str,
    issuance_data: dict,
    pdf_attachment: bytes
) -> bool:
    """Send beautiful HTML email with certificate attachment"""
    try:
        logger.info(f"Preparing email to {to_email} for certificate {issuance_data['id']}")
        
        # Create message container
        msg = MIMEMultipart('alternative')
        msg['From'] = settings.SMTP_FROM
        msg['To'] = to_email
        msg['Subject'] = f"Your Share Certificate - {issuance_data['id']}"
        
        # Create HTML email body
        html = create_email_template(shareholder_name, issuance_data)
        msg.attach(MIMEText(html, 'html'))
        
        # Attach PDF
        part = MIMEApplication(
            pdf_attachment,
            Name=f"share_certificate_{issuance_data['id']}.pdf"
        )
        part['Content-Disposition'] = f'attachment; filename="share_certificate_{issuance_data["id"]}.pdf"'
        msg.attach(part)
        
        if settings.ENVIRONMENT == "testing":
            logger.info(f"Email simulation (not sent): To: {to_email}")
            return True
        
        # Connect to SMTP server
        logger.info(f"Connecting to SMTP server at {settings.SMTP_HOST}:{settings.SMTP_PORT}")
        
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.ehlo()
            
            # Only start TLS if explicitly configured
            if getattr(settings, 'SMTP_USE_TLS', True):  # Safely get attribute with default
                server.starttls()
                server.ehlo()
            
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
            logger.info("Email sent successfully")
            return True
            
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}", exc_info=True)
        return False