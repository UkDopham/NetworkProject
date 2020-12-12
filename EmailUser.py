class EmailUser:

	def __init__(self, username, password, server):
		self.username = username
		self.password = password
		self.server = server

	def get_username(self):
		return self.username

	def get_password(self):
		return self.password

	def get_server(self):
		return self.server