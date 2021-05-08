import datetime
import sqlite3
import pprint
from pytz import timezone
from profanity import *
allowed_link_chars = ["github",".com","youtube","www."]
#HELPER CLASSES AND FUNCTIONS
class Project:
	#Total project count submitted by community TODO count projects cached from previous runtimes via searching the db
	total = 0
	#ex Project("FicklePickle#4818", "TwilioSpam", "github.com/assets")
	def __init__(self, project_author, project_name, project_assets):
		Project.total += 1
		#STATIC VARIABLES
		if not isVulgar(project_author) and not isVulgar(project_name) and len([x for x in allowed_link_chars if x in project_assets]) < 1:
			self.project_author = project_author
			self.project_name = project_name
			self.project_assets = project_assets
		else:
			return None
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

def is_calling_command(message_content,*command_names,current_channel=None,prefix=None,allowed_channel=None):
	command_names = [x for x in command_names]
	for x in range(len(command_names)):
		command_names[x] = command_names[x].lower()
	message_content = message_content.lower()
	if current_channel is None or allowed_channel is None:
		if prefix is None:
			for command_name in command_names:
				if not (command_name in message_content and ("neumann" in message_content or "von" in message_content or '829358670042365992' in message_content)):
					return False
			return True
		else:
			for command_name in command_names:
				if message_content.startswith(prefix + command_name):
					continue
				else:
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
					if not (prefix + command_name in message_content):
						return False
				return True
						
		else:
			return False

#SQLITE3 HELPER FUNCTIONS START\
connection = sqlite3.connect('USER_PROJECTS.db')
def create_projects_db():
	connection = sqlite3.connect('USER_PROJECTS.db'); do = connection.cursor()
	do.execute("""CREATE TABLE projects (author TEXT, name TEXT, assets TEXT)""")
	connection.commit(); connection.close()


def addProject(project):
	connection = sqlite3.connect('USER_PROJECTS.db')
	do = connection.cursor()

	do.execute("INSERT INTO Projects VALUES (?,?,?)", [project.project_author, project.project_name, project.project_assets])
	connection.commit()
	connection.close()


def changeAuthor(table, id, new_author, connection='USER_PROJECTS.db'):
	connection = sqlite3.connect(connection)
	do = connection.cursor()

	do.execute(f"UPDATE {table} SET author = {new_author} WHERE rowid == {id}")
	connection.commit()
	connection.close()


def changeAssets(table, id, new_assets, connection='USER_PROJECTS.db'):
	connection = sqlite3.connect(connection)
	do = connection.cursor()

	do.execute(f"UPDATE {table} SET assets = {new_assets} WHERE rowid == {id}")
	connection.commit()
	connection.close()


def changeName(table, id, new_name, connection='USER_PROJECTS.db'):
	connection = sqlite3.connect(connection)
	do = connection.cursor()

	do.execute(f"UPDATE {table} SET name = {new_name} WHERE rowid == {id}")
	connection.commit()
	connection.close()


def removeProject(table, id, connection='USER_PROJECTS.db'):
	connection = sqlite3.connect(connection)
	do = connection.cursor()

	do.execute(f"DELETE FROM {table} WHERE rowid == {id}")
	connection.commit()
	connection.close()


def getProjects(table, clause = None, connection='USER_PROJECTS.db'):
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
		pprint.pprint(selections)

#END OF SQLITE3 HELPER FUNCTIONS

def unpack_math(message):
	equation = ""
	look_for = "1234567890+-/*^.()"
	for char in message:
		equation = equation + (char if char in look_for else "")
	return equation

def get_ids(message):
	message = message.replace("<","");message = message.replace(">","");message = message.replace("@","");message = message.replace("!","")
	message = message.split()
	for thing in message:
		if thing.isdigit():
			message[message.index(thing)] = message[message.index(thing)] + " "
			continue
		else:
			del message[message.index(thing)]
	message[0] = message[0] + " "
	message = "".join(message)
	message = message.split(" ")
	count = 0
	for _ in range(2): #to fully cleanse all elements
		for id in message:
			if len(str(id)) != 18:
				del message[message.index(id)]
	return message

def get_reason(message):
	if "= " in message.lower() and "r" in message.lower():
		reason = message[message.index("= ")+2:]
		return reason
	elif "=" in message.lower() and "r" in message.lower():
		reason = message[message.index("=")+1:]
		return reason
	else:
		return None

def get_mute_duration(message):
	if "= " in message.lower() and "d" in message.lower():
		reason = message[message.index("= ")+2:]
		return reason
	elif "=" in message.lower() and "d" in message.lower():
		reason = message[message.index("=")+1:]
		return reason
	else:
		return None

def get_slowmode_timer(message):
	if "= " in message.lower() and "s" in message.lower():
		reason = message[message.index("= ")+2:]
		return reason
	elif "=" in message.lower() and "s" in message.lower():
		reason = message[message.index("=")+1:]
		return reason
	else:
		return None

def convert_est():
	tz = timezone("GMT")
	now = datetime.datetime.now(tz)
	hour, minute = now.hour, now.minute
	return hour % 6 == 0 and now.month == 6 and now.day <= 4

def get_timestamp():
	obj = datetime.datetime.now()
	year, month, day = str(obj.year), str(obj.month), str(obj.day)
	timestamp = f"{year}-{month}-{day}"
	return timestamp

