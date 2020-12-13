class EmailData:
	def __init__(self, sender, recever, subject, date, content):
		self.sender = sender
		self.recever = recever
		self.subject = subject
		self.date = date
		self.content = content

	def get_sender(self):
		return self.sender

	def get_recever(self):
		return self.recever

	def get_subject(self):
		return self.subject

	def get_date(self):
		return self.date

	def get_content(self):
		return self.content

	def get_resume(self):
		return "sender " + self.sender + ", recever " + self.recever + ", subject " + self.subject

	def __str__(self):
		return "sender " + self.sender + ", recever " + self.recever + ", subject " + self.subject + ", date " + self.date + ", \n content " + self.content
