import os
import requests
from dotenv import load_dotenv
from app.utils import generate_email_llama2

load_dotenv()

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL", "onboarding@resend.dev")


def send_sales_email(
    customer_name: str,
    customer_email: str,
    lead_score: float,
    quote_value: float,
    item_count: int,
    subject: str
):
    """
    Generate AI-powered email content and send it via Resend API
    """

    if not RESEND_API_KEY:
        return {
            "success": False,
            "message": "RESEND_API_KEY not configured in environment variables.",
            "email_body": ""
        }

    email_body = generate_email_llama2(
        customer_name=customer_name,
        lead_score=lead_score,
        quote_value=quote_value,
        item_count=item_count
    )

    html_body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <p>{email_body.replace(chr(10), "<br>")}</p>
      </body>
    </html>
    """

    try:
        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "from": FROM_EMAIL,
                "to": [customer_email],
                "subject": subject,
                "html": html_body,
            },
            timeout=30,
        )

        if response.status_code in [200, 201]:
            return {
                "success": True,
                "message": f"Email sent successfully to {customer_email}",
                "email_body": email_body
            }
        else:
            return {
                "success": False,
                "message": f"Resend API error: {response.text}",
                "email_body": email_body
            }

    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to send email: {str(e)}",
            "email_body": email_body
        }