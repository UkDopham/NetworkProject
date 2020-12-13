from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from EmailUser import EmailUser
from Sqllite import Sqllite
from EmailData import EmailData
from datetime import datetime
from datetime import date

import email
import smtplib
import imaplib
import socket   
import uuid 
import os


def login(username, password, server):
	server.login(username, password)

def sendEmail(sender, recever, message, server):
	login(sender.get_username(), sender.get_password(), server)
	print(sender.get_username())
	print(recever)
	server.sendmail(sender.get_username(), recever, message.as_string())
	log(sender.get_username(), "[send]")

def readEmail(u):
	EMAIL = u.get_username()
	PASSWORD = u.get_password()
	SERVER = u.get_server()
	mail = imaplib.IMAP4_SSL("imap." + SERVER)
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
	log(u.get_username(), "[read]")
	return my_message

def log(username, title):
	hostname = socket.gethostname()    
	IPAddr = socket.gethostbyname(hostname)    
	f = open("log.txt", "a")
	f.write(title + " " + str(datetime.now()) + " " + username + " " + str(IPAddr) + "\n")

	f.close() 

def saveEmail(email, subject):
	f = open("saves/" + str(date.today()) + str(uuid.uuid1()) + ".txt",  "w")
	f.write(str(email))
	f.close()

def interface():	
	print("Bienvenue dans la meilleur boite mail au monde !")
	print("Ajouter un nouvel utilisateur ? Oui/Non (0/1)")
	ip = input()
	if ip == "0":
		interfaceNewUser()

	print("Quelle boîte mail voulez vous utilisez ?")
	users = getEmailUsers()	
	for i in range(0, len(users)):
		print(str(i) + " " + str(users[i]))
	ip = input()
	u = users[int(ip)]
	user = EmailUser(u[0], u[1], u[2])
	log(user.get_username(), "[login]")
	print("vous avez selectionné la boîte mail " + str(user.get_username()))

	print("Que voulez vous faire ? (1 Send , 2 Read, 3 Sort, 4 Log, 5 LogOut)")
	ip = input()
	if ip == "1":
		interfaceSend(user)
		return True
	elif ip == "2":
		interfaceReadNew(user)
		interfaceRead(user)
		return True
	elif ip == "3":
		sortEmailData(user)
		return True
	elif ip == "4":
		readLog()
		return True
	elif ip == "5":
		log(user.get_username(), "[logout]")
		return False


def interfaceNewUser():
	print("Username :")
	ipUser = input()
	print("Password :")
	ipPass= input()
	print("Server :")
	ipServ = input()
	eu = EmailUser(ipUser, ipPass, ipServ)
	saveEmailUser(eu)


def getEmailUsers():
	sq = Sqllite()
	conn = sq.create_connection(r"usertest.db")
	emailUser = sq.selectUser(conn)
	sq.close(conn)
	return emailUser

def getMessage(user, subject, recever, msg):
	message = MIMEMultipart('alternative')
	message['Subject'] = subject
	message['From'] = user.get_username()
	message['To'] = recever
	message.attach(MIMEText(msg, 'plain'))
	return message

def getServer(user):
	value = "smtp." + user.get_server()
	server = smtplib.SMTP(value, 587)
	server.starttls()
	return server

def interfaceSend(user):
	print("Send")
	print("Destinataire :")
	ipDes = input()
	print("Sujet :")
	ipSuj = input()
	print("Message :")
	ipMsg = input()
	message = getMessage(user, ipSuj, ipDes, ipMsg)
	server = getServer(user)
	sendEmail(user, ipDes, message, server)

def interfaceReadNew(user):
	emails = readEmail(user)	
	for e in emails:
		saveEmailData(e)

def interfaceRead(user):
	a = getEmailData(user)
	for i in range(0, len(a)):
		ed = EmailData(a[i][0], a[i][1], a[i][2], a[i][3], a[i][4])
		print("[" +str(i) + "] " + ed.get_resume())
	print("Quelle mail voulez vous lire ?")
	ip = input()
	ed = EmailData(a[int(ip)][0], a[int(ip)][1], a[int(ip)][2],a[int(ip)][3], a[int(ip)][4])
	print(a[int(ip)][4])
	print("Sauvegarder le mail dans un fichier lisible, reply ou rien ? (0/1/2)")
	ip = input()
	if ip == "0":
		saveEmail(ed, ed.get_subject())
	elif ip == "1":
		print("Message :")
		ipMsg = input()
		message = getMessage(user, "RE :" + ed.get_subject(), ed.get_sender(), ipMsg)
		server = getServer(user)		
		sendEmail(user, ed.get_sender(), message, server)

def saveEmailData(emailData):
	sq = Sqllite()
	conn = sq.create_connection(r"usertest.db")
	sq.insertData(emailData, conn)
	sq.close(conn)

def saveEmailUser(emailUser):
	sq = Sqllite()
	conn = sq.create_connection(r"usertest.db")
	sq.insertUser(emailUser, conn)
	sq.close(conn)

def getEmailData(user):
	sq = Sqllite()
	conn = sq.create_connection(r"usertest.db")
	emailData = sq.selectData(conn, user)
	sq.close(conn)
	return emailData

def sortEmailData(user):
	sq = Sqllite()
	conn = sq.create_connection(r"usertest.db")
	sq.selectData(conn, user)
	print( "\n" + "Sort by Sender")
	sq.selectDataOrderBySender(conn, user)
	sq.close(conn)

def readLog():
	f = open("log.txt", "r")
	print(f.read())
	f.close()

def initi():
	f = open("init.txt", "r")
	if f.read() == "":
		sq = Sqllite()
		conn = sq.create_connection(r"usertest.db")
		sq.createDataUser(conn)
		sq.createEmailData(conn)
		sq.insertUser(EmailUser("jjesuisla774@gmail.com", "P4t4t3_01", "gmail.com"), conn)
		sq.close(conn)
		f.close()
		f = open("init.txt", "w")
		f.write("0")
	f.close()

initi()
stillContinue = True
while stillContinue == True:
	stillContinue = interface()




