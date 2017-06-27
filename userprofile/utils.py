class Send_email:
	def send_email(self, email_to, subject, message):
		import smtplib
		from email.mime.text import MIMEText

		msg = MIMEText(message)
		msg['Subject'] = subject

		mail = smtplib.SMTP('smtp.gmail.com', 587)  # or 465 (google said :Сервер исходящей почты), but not working thou :)

		mail.ehlo()

		mail.starttls()  # Transport Layer Security

		mail.login('buyandplay.team@gmail.com', '123zxcGmail+')  # !!!!!!

		mail.sendmail('buyandplay.team@gmail.com', email_to, msg.as_string())  # roman.olshansky123@gmail.com
		mail.close()
