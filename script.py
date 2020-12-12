from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from EmailUser import EmailUser
from Sqllite import Sqllite
from EmailData import EmailData
from datetime import datetime

import email
import smtplib
import imaplib
import socket   
import uuid 


def login(username, password, server):
	server.login(username, password)

def sendEmail(sender, recever, message, server):
	login(sender.get_username(), sender.get_password(), server)
	print(sender.get_username())
	print(recever.get_username())
	server.sendmail(sender.get_username(), recever.get_username(), message.as_string())
	log(sender, True)

def readEmail(u):
	EMAIL = u.get_username()
	PASSWORD = u.get_password()
	SERVER = u.get_server()
	mail = imaplib.IMAP4_SSL(SERVER)
	mail.login(EMAIL, PASSWORD)
	mail.select("inbox")
	_, search_data = mail.search(None, 'UNSEEN')
	my_message = []
	for num in search_data[0].split():
		email_data = {}
		_, data = mail.fetch(num, '(RFC822)')
		_, b = data[0]
		email_message = email.message_from_bytes(b)
		for header in ['subject', 'to', 'from', 'date']:
			#print("{}: {}".format(header, email_message[header]))
			email_data[header] = email_message[header]
		for part in email_message.walk():
			if part.get_content_type() == "text/plain":
				body = part.get_payload(decode=True)
				email_data['body'] = body.decode()
			elif part.get_content_type() == "text/html":
				html_body = part.get_payload(decode=True)
				email_data['body'] = html_body.decode()
		my_message.append(EmailData(email_data['from'], email_data['to'], email_data['subject'], email_data['date'],email_data['body']))
		saveEmail(email_message, email_data['subject'])
	log(u, False)
	return my_message

def log(email, isSend):
	hostname = socket.gethostname()    
	IPAddr = socket.gethostbyname(hostname)    
	f = open("log.txt", "a")
	if isSend:
		f.write( "[send] " + str(datetime.now()) + " " + email.get_username() + " " + str(IPAddr) + "\n")	
	else:
		f.write( "[receive] " + str(datetime.now()) + " " + email.get_username() + " " + str(IPAddr) + "\n")	

	f.close() 

def saveEmail(email, subject):
	f = open(subject + " " + str(uuid.uuid1()) + ".txt",  "w")
	f.write(str(email))
	f.close()

u = EmailUser("jjesuisla774@gmail.com", "P4t4t3_01", "imap.gmail.com")
sq = Sqllite()
conn = sq.create_connection(r"usertest.db")
#sq.createDataUser(conn)
#sq.createEmailData(conn)

#sq.insertUser(u, conn)
sq.selectUser(conn)
emails = readEmail(u)
for e in emails:
	sq.insertData(e, conn)

sq.selectData(conn)
print( "\n" + "Sort by Sender")
sq.selectDataOrderBySender(conn)
sq.close(conn)


message = MIMEMultipart('alternative')
message['Subject'] = 'Test'
message['From'] = 'jjesuisla774@gmail.com'
message['To'] = 'jjesuisla774@gmail.com'

message.attach(MIMEText('salut le monde', 'plain'))

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
#server.login('jjesuisla774@gmail.com', 'P4t4t3_01')
#server.sendmail('jjesuisla774@gmail.com', 'jjesuisla774@gmail.com', message.as_string())
sendEmail(u, u, message, server)
server.quit()




