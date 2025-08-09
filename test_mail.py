import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# Load từ .env
load_dotenv()

STMP_USER = str(os.getenv("EMAIL_SERVICE"))  # your email service, e.g., gmail
STMP_PASSWORD = str(os.getenv("SMTP_PASSWORD"))

def send_mail_to_admin(subject, message_body, admin_email):
    # Cấu hình SMTP
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SMTP_USER = STMP_USER
    SMTP_PASSWORD = STMP_PASSWORD

    # Tạo email
    msg = MIMEMultipart("alternative")
    msg['From'] = SMTP_USER
    msg['To'] = admin_email
    msg['Subject'] = subject

    # Nội dung HTML
    html_part = MIMEText(message_body, 'html')
    msg.attach(html_part)

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("✅ Email HTML đã được gửi đến admin.")
    except Exception as e:
        print(f"❌ Gửi email thất bại: {e}")

# Email content
admin_email = "lea26462@gmail.com"
subject = "✅ CREATED IMAGE NOTIFICATION"

message = f"""
<html>
<head>
  <style>
    body {{ font-family: Arial, sans-serif; }}
    .container {{
      border: 1px solid #ddd;
      border-radius: 8px;
      padding: 20px;
      background-color: #f9f9f9;
      max-width: 600px;
      margin: auto;
    }}
    h2 {{ color: #2c3e50; }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 10px;
    }}
    td {{
      padding: 8px;
      border-bottom: 1px solid #eee;
    }}
    .label {{ font-weight: bold; color: #555; }}
    .value {{ color: #333; }}
  </style>
</head>
<body>
  <div class="container">
    <h2>🎉 Image Creation Successful</h2>
    <p>Image for <strong>12</strong> has been successfully created and uploaded to Google Drive.</p>
    <table>
      <tr><td class="label">Name:</td><td class="value">{55555}</td></tr>
      <tr><td class="label">Description:</td><td class="value">{55555}</td></tr>
      <tr><td class="label">Upgrade Description:</td><td class="value">{55555}</td></tr>
      <tr><td class="label">Model:</td><td class="value">{55555}</td></tr>
      <tr><td class="label">Image Type:</td><td class="value">{55555}</td></tr>
      <tr><td class="label">Image Link:</td><td class="value"><a href="{55555}">View Image</a></td></tr>
      <tr><td class="label">Time:</td><td class="value">{55555}</td></tr>
    </table>
  </div>
</body>
</html>
"""

send_mail_to_admin(subject, message, admin_email)
