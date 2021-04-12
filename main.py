#importing modules

#Main imports
import discord
from Channels import channel_dictionary
import sqlite3


#Message logic imports
import datetime
import pyjokes as joke


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



#DISCORD.PY
#initialising static variables
TOKEN = ('ODI5MzU4NjcwMDQyMzY1OTky.YG2-cw.Ak6kITYzT05sTkxj8ZcbT5bd6dg')
GUILD = ('794843921501913108')

#bot creation
client = discord.Client()

#events
@client.event
async def on_ready():
    bot_com = client.get_channel(channel_dictionary["bot_commands"])
    await bot_com.send("What's up? I'm back!")

@client.event
async def on_message(message):

	#so the bot will not reply to itself or other bots
	if message.author == client.user or message.author.bot: 
		return
	elif is_calling_command(message.content, 'joke', 'tell', current_channel=message.channel.id, allowed_channel=channel_dictionary["bot_commands"]):
		bot_com = client.get_channel(channel_dictionary["bot_commands"])
		await bot_com.send(f'I got one for ya,\n"{joke.get_joke()}"')

	elif is_calling_command(message.content, 'help', current_channel=message.channel.id, allowed_channel=channel_dictionary["bot_commands"]):
		bot_com = client.get_channel(channel_dictionary["bot_commands"])
		await bot_com.send('help')

	elif is_calling_command(message.content, 'time', current_channel=message.channel.id, allowed_channel=channel_dictionary["bot_commands"]):
		now = datetime.datetime.now(); hour, minute = now.hour, str(now.minute)
		ampm = "AM"
		#changes the time from military to standard
		if len(minute) == 1:
			minute = "0" + minute
		if hour > 12:
			ampm = "PM"
			hour -= 12
		elif hour == 12:
			ampm = "PM"
		elif hour == 0:
			hour = 12
			ampm = "AM"
		else:
			ampm = "AM"
		bot_com = client.get_channel(channel_dictionary["bot_commands"])
		await bot_com.send(f'The time is {hour}:{minute} {ampm}')

	elif is_calling_command(message.content, 'submit','project',current_channel=message.channel.id, allowed_channel=channel_dictionary["mods-chat"]):
		#TODO, make lines in this command for uploading submission links, checking a submission for validity, and then creating project objects to plug into the database
		#connection = sqlite3.connect('USER_PROJECTS.db')
		
		connection = sqlite3.connect(':memory:')
		do = connection.cursor()
		#do.execute("""CREATE TABLE projects (user text, title text, assets text)""") #ALREADY INITIATED A TABLE
		#do.execute("INSERT INTO projects VALUES (?, ?, ?)", (object.retrieve_project_information())); connection.commit(); connection.close() #USE AS A TEMPLATE
		connection.close()

		bot_com = client.get_channel(channel_dictionary["mods-chat"])
		await bot_com.send("WORKING")

	elif is_calling_command(message.content, 'evaluate',current_channel=message.channel.id,allowed_channel=channel_dictionary['bot_commands']):
		bot_com = client.get_channel(channel_dictionary["bot_commands"])
		full = message.content
		equation = ""
		answer = ""
		look_for = "1234567890+-/*^.()"
		for char in full:
			if char == "^":
				await bot_com.send("Try again, use '**' for exponents instead of ^. Otherwise functions will have trouble evaluating")
				return ""
			
			equation = str(equation + char if char in look_for else "")
		
		#TODO get equation to solve itself, kinda like how when you print(5+7) it will print 12 instead of 5+7
		await bot_com.send(f'{equation} = {eval(equation)}')
	else:
		pass

for key in channel_dictionary:
	print(key, channel_dictionary[key])

client.run(TOKEN)






