import smtplib
import email.utils
from email.mime.text import MIMEText
import getpass

# Prompt the user for connection info
to_email = 'ovodrake066@gmail.com'
servername = 'smtp.gmail.com'
username = 'SMTPemail24'
password = 'SMTPCs3800'

# Create the message
msg = MIMEText('This is a test message.')

msg.set_unixfrom('author')
msg['To'] = email.utils.formataddr(('Recipient', to_email))
msg['From'] = email.utils.formataddr(('Author', 'SMTPemail24@gmail.com'))
msg['Subject'] = 'Testing'

server = smtplib.SMTP(servername,587) # using TLS protocols
try:
    server.set_debuglevel(True)

    # identify ourselves, prompting server for supported features
    server.ehlo()

    # encrypted session
    if server.has_extn('STARTTLS'):
        server.starttls()
        server.ehlo() # re-identify ourselves over TLS connection

    server.login(username, password)
    server.sendmail('SMTPemail24@gmail.com', [to_email], msg.as_string())
finally:
    server.quit()