#importing modules

#Main imports
import discord
from Channels import channel_dictionary
from helper import *
import sqlite3


#Message logic imports
from message_funcs import *
import pyjokes as joke


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
		hour, minute, ampm = unpack_time()
		bot_com = client.get_channel(channel_dictionary["bot_commands"])
		await bot_com.send(f'The time is {hour}:{minute} {ampm}')
	
	#TODO this is the main purpose of this bot, to help with event submission, this where the code will come together to use the database
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

	elif is_calling_command(message.content,'eval',current_channel=message.channel.id,allowed_channel=channel_dictionary['bot_commands']):
		bot_com = client.get_channel(channel_dictionary["bot_commands"])	
		equation = unpack_math(message.content)
		await bot_com.send(f"{equation} = {eval(equation)}")
	
	else:
		pass

for key in channel_dictionary:
	print(key, channel_dictionary[key])

client.run(TOKEN)





