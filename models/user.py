class User:
	def __init__(self, user_id, username, first_name, last_name):
		self.user_id = user_id
		self.username = username
		self.first_name = first_name
		self.last_name = last_name

	def __str__(self):
		return f"User ID: {self.user_id}\nUsername: {self.username}\nFirst Name: {self.first_name}\nLast Name: {self.last_name}"