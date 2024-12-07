import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(recipient, subject, message):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender = "dataanalysisformulaufmg2024@gmail.com"
    password = "skzv emrw adck mhny"

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(message,'plain'))

    try:
        server = smtplib.SMTP(smtp_server,smtp_port)
        server.starttls()
        server.login(sender, password)

        server.sendmail(sender, recipient, msg.as_string())
        print("email enviado")
    except Exception as e:
        print('erro ao enviar email:{}'.format(e))
    finally:
        server.quit()
