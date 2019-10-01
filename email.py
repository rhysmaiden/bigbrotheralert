import smtplib

import config
import sys
import string

subject = sys.argv[1]
msg = sys.argv[2]


printable = set(string.printable)
filter(lambda x: x in printable, msg)

#msg = msg.encode('ascii')

server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(config.email, config.email_password)

message = 'Subject: {}\n\n{}'.format(subject, msg)
server.sendmail(config.email, config.email, message)
server.quit()
