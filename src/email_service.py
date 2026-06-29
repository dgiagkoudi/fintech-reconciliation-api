from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import aiosmtplib
from src.config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, EMAIL_FROM, EMAIL_TO

async def send_unmatched_alert(unmatched_count: int, details_html: str):
    message = MIMEMultipart("alternative")
    message["From"] = EMAIL_FROM
    message["To"] = EMAIL_TO
    message["Subject"] = f"[FINTECH ALERT] Βρέθηκαν {unmatched_count} Unmatched Κινήσεις"
    
    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif;">
        <h2 style="color: #d9534f;">Εκκρεμεί Λογιστική Διευθέτηση</h2>
        <p>Βρέθηκαν <b>{unmatched_count}</b> τιμολόγια χωρίς αντίστοιχη τραπεζική κίνηση.</p>
        <table border="1" style="border-collapse:collapse; width:100%; text-align:left;">
          <tr style="background-color:#f2f2f2;">
            <th style="padding: 8px;">Αρχείο</th>
            <th style="padding: 8px;">ΑΦΜ</th>
            <th style="padding: 8px;">Ποσό</th>
            <th style="padding: 8px;">Ημερομηνία</th>
          </tr>
          {details_html}
        </table>
      </body>
    </html>
    """
    message.attach(MIMEText(html, "html", "utf-8"))
    
    await aiosmtplib.send(
        message, hostname=SMTP_HOST, port=int(SMTP_PORT), username=SMTP_USER, password=SMTP_PASSWORD, use_tls=False
    )