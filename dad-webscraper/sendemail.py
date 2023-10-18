from email.message import EmailMessage
import smtplib

class email:
    def __init__(self, sender, password, receiver, subject, body):
        self.sender = sender
        self.password = password
        self.receiver = receiver
        self.subject = subject
        self.body = body
        
    def send(self):
        em = EmailMessage()

        em['Subject'] = self.subject
        em.set_content(self.body)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(self.sender, self.password)
            smtp.sendmail(self.sender, self.receiver, em.as_string())