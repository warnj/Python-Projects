import smtplib, json
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

data = json.loads(open('../personal_data.json').read())

fromaddr = data["gmail"]
toaddr = data["email"]
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Automated Email"

body = "Remember: X"
msg.attach(MIMEText(body, 'plain'))

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, data["gmail_password"])
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
