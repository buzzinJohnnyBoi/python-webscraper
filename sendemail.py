from email.message import EmailMessage
import smtplib

email_sender = "johncamp724@gmail.com"
email_password = "" #I deleted this part

def send(receiver, subject, body):

    em = EmailMessage()

    em['Subject'] = subject
    em.set_content(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, receiver, em.as_string())