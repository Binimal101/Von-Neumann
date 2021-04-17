#importing modules

#Main imports
import discord
from Channels import *
from Roles import *
from helper import *
import sqlite3
import urllib.request
import os


#Message logic imports
from message_funcs import *
import pyjokes as joke
from profanity import *


#DISCORD.PY
#initialising static variables
TOKEN = os.environ['TOKEN']
GUILD = os.environ['GUILD']

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
	elif isVulgar(message.content):
		bot_com = client.get_channel(message.channel.id)
		await message.delete()
		await bot_com.send(censor(message.content,message.author))
		
	elif is_calling_command(message.content, 'joke', 'tell', current_channel=message.channel.id, allowed_channel=channel_dictionary["bot_commands"]):
		bot_com = client.get_channel(channel_dictionary["bot_commands"])
		await bot_com.send(f'I got one for ya,\n"{joke.get_joke()}"')

	elif is_calling_command(message.content, 'help', current_channel=message.channel.id, allowed_channel=channel_dictionary["bot_commands"]):
		bot_com = client.get_channel(channel_dictionary["bot_commands"])
		#initialising command embed
		embed=discord.Embed(title="Commands", description="Type help <command> for more information on a command", color=0xd50101)
		embed.add_field(name="Von+Joke+Tell", value="Von will tell you a joke", inline=False)
		embed.add_field(name="Von+Eval", value="Von will solve basic math problems", inline=False)
		embed.add_field(name="Von+Time", value="Von will tell you the time", inline=False)
		embed.add_field(name="Von+Help", value="Von will show you all commands", inline=False)
		embed.add_field(name="Von+Submit+Project", value="Von will walk you through how to submit a user project", inline=False)
		
		await bot_com.send(embed=embed)
		

	elif is_calling_command(message.content, 'time', current_channel=message.channel.id, allowed_channel=channel_dictionary["bot_commands"]):
		hour, minute, ampm = unpack_time()
		bot_com = client.get_channel(channel_dictionary["bot_commands"])
		await bot_com.send(f'The time is {hour}:{minute} {ampm}')
	
	#TODO this is the main purpose of this bot, to help with event submission, this where the code will come together to use the database
	elif is_calling_command(message.content, 'submit','project',current_channel=message.channel.id, allowed_channel=channel_dictionary["mods-chat"]):
		#TODO, make lines in this command for uploading submission links, checking a submission for validity, and then creating project objects to plug into the database
		
		"""ALL DATA WILL BE MANIPULATED VIA HELPER FUNCTIONS IN HELPER.py"""
		#TODO implement this line with helper functions
		#do.execute("INSERT INTO projects VALUES (?, ?, ?)", (object.retrieve_project_information())); connection.commit(); connection.close() #USE AS A TEMPLATE
		

		connection.close()

		bot_com = client.get_channel(channel_dictionary["mods-chat"])
		await bot_com.send("WORKING")

	elif is_calling_command(message.content,'eval',current_channel=message.channel.id,allowed_channel=channel_dictionary['bot_commands']):
		bot_com = client.get_channel(channel_dictionary["bot_commands"])	
		equation = unpack_math(message.content)
		await bot_com.send(f"{equation} = {eval(equation)}")
	
	elif is_calling_command(message.content,'purge',current_channel=message.channel,allowed_channel=message.channel):
		bot_com = client.get_channel(message.channel.id)
		
		id = [None,]
		for x in message.author.roles:
			id.append(x.id)

		if is_admin(id):
			limit = 0
			for word in message.content:
				if word.isdigit():
					count = 0
					#for word in message.content parses 12 as 1 then 2
					#cycles thru and concatatnates 1 and 2 to make "12" then converts to int
					if count != 0:
						limit = limit + word
					else:
						limit = word
					count += 1
			
			limit = int(limit)
			await bot_com.purge(limit=(limit+1 if limit != 0 else 1000))
		else:
			await bot_com.send("Ha, nice try nerd\nTry getting some perms first")
	
	else:
		pass

for key in channel_dictionary:
	print(key, channel_dictionary[key])

client.run(TOKEN)
