import smtplib
from email.mime.text import MIMEText

def send_email_report(to_email, subject, content):

    sender_email = "your_email@gmail.com"
    app_password = "your_app_password"  # Gmail App Password

    msg = MIMEText(content)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, app_password)
    server.sendmail(sender_email, to_email, msg.as_string())
    server.quit()

    return "Email Sent Successfully"