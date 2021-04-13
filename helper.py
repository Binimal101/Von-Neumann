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

# def get_instances
