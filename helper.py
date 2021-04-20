#HELPER CLASSES AND FUNCTIONS
class Project:
	#Total project count submitted by community TODO count projects cached from previous runtimes via searching the db
	total = 0
	#ex Project("FicklePickle#4818", "TwilioSpam", "github.com/assets")
	def __init__(self, project_author, project_name, project_assets):
		Project.total += 1
		#STATIC VARIABLES
		self.project_author = project_author
		self.project_name = project_name
		self.project_assets = project_assets
		#LIVE VARIABLES
		self.upvotes = 0
		self.downvotes = 0
	
	#TODO make a check function to check each arguement entered to see if submission is valid @Mixed.Engineering
	
	#returns project information
	def retrieve_project_information(self):
		return self.project_author, self.project_name, self.project_assets
	def retrieve_project_information_all(self):
		return self.project_author, self.project_name, self.project_assets, self.upvotes, self.downvotes
	
	#setter instance methods
	def adjust_project_upvotes(self, upvotes):
		self.upvotes = upvotes
	def adjust_project_downvotes(self, downvotes):
		self.downvotes = downvotes
	def adjust_project_name(self, project_name):
		self.project_name = project_name
	def adjust_project_assets(self, project_assets):
		self.project_assets = project_assets


#Checks the string given from message.content as first arg, all other arguements is are required command names
#Keyword arguement to set a prefix if any is wanted and to set where you want to listen for a command and where the command actually comes in from

def is_calling_command(message_content,*command_names,current_channel=None,prefix=None,allowed_channel=None,usr_roles=None,role_requirements=None):
	command_names = [x for x in command_names]
	for x in range(len(command_names)):
		command_names[x] = command_names[x].lower()
	message_content = message_content.lower()
	if current_channel is None or allowed_channel is None:
		if prefix is None:
			for command_name in command_names:
				if not (command_name in message_content and ("neumann" in message_content or "von" in message_content)):
					return False
			return True
		else:
			for command_name in command_names:
				if not (prefix + command_name in message_content or (command_name in message_content and ("neumann" in message_content or "von" in message_content))):
					return False
			return True
	else:
		if current_channel == allowed_channel:
			if prefix is None:
				for command_name in command_names:
					if not (command_name in message_content and ("neumann" in message_content or "von" in message_content)):
						return False
				return True
			else:
				for command_name in command_names:
					if not (prefix + command_name in message_content or (command_name in message_content and ("neumann" in message_content or "von" in message_content))):
						return False
				return True
						
		else:
			return False

#SQLITE3 HELPER FUNCTIONS START

#As to not raise errors
import sqlite3
connection = sqlite3.connect(':memory:'); do = connection.cursor()
do.execute("""CREATE TABLE projects (author TEXT, name TEXT, assets TEXT)""")
connection.commit(); connection.close()


def addProject(table, author, name, assets, connection=':memory:'):
	connection = sqlite3.connect(connection)
	do = connection.cursor()

	do.execute(f"INSERT INTO {table} VALUES (?,?,?)", [author, name, assets])
	connection.commit()
	connection.close()


def changeAuthor(table, id, new_author, connection=':memory:'):
	connection = sqlite3.connect(connection)
	do = connection.cursor()

	do.execute(f"UPDATE {table} SET author = {new_author} WHERE rowid == {id}")
	connection.commit()
	connection.close()


def changeAssets(table, id, new_assets, connection=':memory:'):
	connection = sqlite3.connect(connection)
	do = connection.cursor()

	do.execute(f"UPDATE {table} SET assets = {new_assets} WHERE rowid == {id}")
	connection.commit()
	connection.close()


def changeName(table, id, new_name, connection=':memory:'):
	connection = sqlite3.connect(connection)
	do = connection.cursor()

	do.execute(f"UPDATE {table} SET name = {new_name} WHERE rowid == {id}")
	connection.commit()
	connection.close()


def removeProject(table, id, connection=':memory:'):
	connection = sqlite3.connect(connection)
	do = connection.cursor()

	do.execute(f"DELETE FROM {table} WHERE rowid == {id}")
	connection.commit()
	connection.close()


def getProjects(table, clause = None, connection=':memory:'):
	connection = sqlite3.connect(connection)
	do = connection.cursor()

	if clause is not None:
		do.execute(f"SELECT rowid, * FROM {table} {clause}")
		selections = do.fetchall()
		connection.close()
		return selections
	else:
		do.execute(f"SELECT rowid, * FROM {table}")
		selections = do.fetchall()
		connection.close()
		return selections
#END OF SQLITE3 HELPER FUNCTIONS



