import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailUtils:
    @staticmethod
    def send_email(subject, body, recipient_email):
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        sender_email = 'tempftempl012001@gmail.com'
        password = 'ecvb lypr ahwt zlyi'

        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_email, message.as_string())
