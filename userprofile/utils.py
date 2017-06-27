from django.conf import settings

class Send_email:

    def __init__(self, email_to, subject, message):
    	self.email_to = email_to
    	self.subject = subject
    	self.message = message

    def send_email(self):
        import smtplib
        from email.mime.text import MIMEText

        msg = MIMEText(self.message)
        msg['Subject'] = self.subject

        mail = smtplib.SMTP('smtp.gmail.com', 587)  # or 465 (google said :Сервер исходящей почты), but not working thou :)

        mail.ehlo()

        mail.starttls()  # Transport Layer Security

        mail.login(settings.GMAIL_MAIL, settings.GMAIL_PASS)

        mail.sendmail(settings.GMAIL_MAIL, self.email_to, msg.as_string())  # roman.olshansky123@gmail.com
        mail.close()
