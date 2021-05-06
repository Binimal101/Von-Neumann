#WILL IMPACT RUN FOREVER FUNCTION
testing = False
#Main imports
from run_forever import run_forever #RUN_FOREVER VIA UPTIMEROBOTS
import discord, sqlite3, os, random, urllib.request
import pyjokes as joke
from hashlib import sha256
from discord.ext import commands
from discord.ext.commands import *
#File Imports
from info import *
from helper import *
from profanity import *
#On Start Custom Info
link_chars = [".net","www.","https://",".com",".org","http",".co"] #gets rid of any links with at least one of these in the string, Expandable
prefix = "!"

logs_enabled = True
channel_creator = True
link_killer = False
profanity_filter = True
ban_kick = True

os.system('cls' if os.name=='nt' else 'clear')

#TO PREVENT VIEWERS FROM RUNNING THE BOT, PASSWORD WILL BE PINNED TO MOD-CHAT

#usr_password = sha256(input("ENTER ACTIVATION PASSWORD\n>>> ").encode()).hexdigest()
#if usr_password == os.environ['Password']:
os.system('cls' if os.name=='nt' else 'clear')
TOKEN = os.environ['TOKEN']
print("**ONLINE**")

#DISCORD.PY

#bot creation

intents = discord.Intents.default()
intents = intents.all()

activity = discord.Activity(type=discord.ActivityType.listening, name="developer team") #Gives bot a custom status :pog:
permissions = discord.Permissions(administrator=True)
client = discord.Client(intents=intents,activity=activity,permissions=permissions)

#events

@client.event
async def on_ready():
    connection= client.get_channel(channel_dictionary["bot_commands"])
    await connection.send("What's up Mixed Engineers")

@client.event
async def on_raw_reaction_add(payload):
	#payload.emoji returns the literal emoji, cannot compare with == operator, so hash it and compare it then
	Guild = client.get_guild(payload.guild_id) #gets guild object from the parameter, should work on multiple servers
	if Guild.id != 794843921501913108: #to just keep this while its in the works on this server
		return
	
	#Rules channel Only react roles
	if payload.message_id == 839849973411086386:
		Channel = discord.utils.get(Guild.channels, name="📝rules")
		Message = await Channel.fetch_message(839849973411086386)
		#Unlock Emote
		if sha256(payload.emoji.name.encode()).hexdigest() == '4eec930975e4c54d690a82bd3be37c58a7c35e7021b367474f13eebdc7fd211d':
			role = discord.utils.get(Guild.roles, name="mixed engineers") #gets the role obj for the role we are going to give to the reactor
			reactor = discord.utils.find(lambda u: u.id == payload.user_id, Guild.members) #searches through guild.memberes for the member object with the id of the reactor
			#Will run if info above is viable
			if reactor is not None and not payload.user_id == client.user.id: #makes sure the bot doesn't get the role when he adds the roles back for other users to react to
				await reactor.add_roles(role)
				snowflake = discord.Object(reactor.id)
				await Message.remove_reaction(payload.emoji, snowflake)

	#React Roles channel only react roles
	elif payload.message_id == 839855261623517234:
		Channel = discord.utils.get(Guild.channels, name="react_roles")
		Message = await Channel.fetch_message(839855261623517234)
		Emoji = payload.emoji
		Role = discord.utils.find(lambda x: x.name == Emoji.name, Guild.roles) #should work as long as role name and emoji name are the same
		reactor = discord.utils.find(lambda u: u.id == payload.user_id, Guild.members)
		#Will run if info above is viable
		if reactor is not None and not payload.user_id == client.user.id:
			if Role in reactor.roles:
				await reactor.remove_roles(Role)
			else:
				await reactor.add_roles(Role)
			#Removes reactors reaction
			snowflake = discord.Object(reactor.id)
			await Message.remove_reaction(Emoji, snowflake)
	
		

	
	else:
		return
		
	
@client.event
async def on_guild_join(guild):
	timestamp = get_timestamp()
	#Guild Info
	guild_name, guild_id = guild.name, guild.id
	guild_channels, guild_members = len(guild.channels), len(guild.members)
	#Owner Info
	owner_name = f"{guild.owner.name}#{guild.owner.discriminator}"
	owner_id = guild.owner.id
	#Send Info Home
	home_server = client.get_channel(837726761005482034)
	embed=discord.Embed(title="Von Neumann has joined a server!", color=0x00ffbf)
	embed.add_field(name=f"\nGuild:\n\tName: {guild_name}\n\tId: {guild_id}\n\tMembers: {guild_members}\n\tChannels: {guild_channels}\nOwner:\n\tTag: {owner_name}\n\tId: {owner_id}\n", value=f"{timestamp}", inline=False)
	await home_server.send(embed=embed)

@client.event
async def on_message(message):
	#So bot will not respond inside a DMChannel
	if isinstance(message.channel, discord.channel.DMChannel):
		return

	connection = message.channel
	guild = client.get_guild(message.channel.guild.id)
	
	if logs_enabled and channel_creator:

		ban_logger = discord.utils.get(connection.guild.text_channels, name="ban_logs")
		if ban_logger is None: #ADDS THESE CHANNELS TO SERVERS WITHOUT THEM
			await connection.guild.create_text_channel('ban_logs')
			ban_logger = discord.utils.get(connection.guild.text_channels, name="ban_logs")
			await ban_logger.set_permissions(connection.guild.default_role, send_messages=False)

		kick_logger = discord.utils.get(connection.guild.text_channels, name="kick_logs")
		if kick_logger is None: #ADDS THESE CHANNELS TO SERVERS WITHOUT THEM
			await connection.guild.create_text_channel('kick_logs')
			kick_logger = discord.utils.get(connection.guild.text_channels, name="kick_logs")
			await kick_logger.set_permissions(connection.guild.default_role, send_messages=False)
		
		try:
			kick_log_id = discord.utils.get(connection.guild.text_channels, name="kick_logs").id
			ban_log_id = discord.utils.get(connection.guild.text_channels, name="ban_logs").id
		except:
			pass
	
	#Creates Objects From ids
	def get_member_objects(message):
		objects = []
		ids = get_ids(message)
		for id in ids:
			if id is not None:
				objects.append(discord.Object(id))
		return objects
	
	async def add_reactions_to_message(emoji_name,channel_name,message_id):
		Guild = client.get_guild(794843921501913108)
		Channel = discord.utils.get(Guild.channels, name=channel_name)
		Message = await Channel.fetch_message(message_id)
		Emoji = discord.utils.find(lambda x: x.name == emoji_name,Guild.emojis)
		await Message.add_reaction(Emoji)

	async def dm_user(message=None,embed=None,id=None):
		if id is not None:
			if message is not None and embed is None:
				recipient = await client.fetch_user(id)
				await recipient.send(message)

			elif message is None and embed is not None:
				recipient = await client.fetch_user(id)
				await recipient.send(embed=embed)

			elif message is not None and embed is not None:
				recipient = await client.fetch_user(id)
				await recipient.send(message, embed=embed)
			else:
				return
		else:
			return
	
	if logs_enabled:
		if not message.author == client.user or not message.author.bot and ("von" in message.content.lower() or isVulgar(message)) or message.content.startswith('!') or "neumann" in message.content.lower():
			logs = open("logs.txt","a")
			logs.write(f"{message.author}: {message.content}\n")

	if link_killer:
		if not (message.channel.permissions_for(message.author).administrator) and not message.author.bot:
			for look_for in link_chars:
				if look_for in message.content:
					await message.delete()

	if message.author.bot:
		return

	elif isVulgar(message.content) and profanity_filter:
		try:
			connection = client.get_channel(message.channel.id)
			if not(message.content in censor(message.content, message.author)):
				await message.delete()
				await connection.send(censor(message.content,message.author))
		except:
			pass

	elif is_calling_command(message.content, 'joke', 'tell',allowed_channel=channel_dictionary["bot_commands"],current_channel=channel_dictionary["bot_commands"]):
		connection= client.get_channel(channel_dictionary["bot_commands"])
		await connection.send(f'I got one for ya,\n"{joke.get_joke()}"')

	elif is_calling_command(message.content, "quote"):
		connectiion = message.channel
		quote=f"```\n{random.choice(unpackVonQuotes())}\n\n~John Von Neumann\n```"
		await connection.send(quote)

	elif is_calling_command(message.content, 'help'):
		connection= client.get_channel(channel_dictionary["bot_commands"])
		#initialising command embed
		embed=discord.Embed(title="Commands", description="Type help <command> for more information on a command", color=0xd50101)
		embed.add_field(name="Von+Joke+Tell", value="Von will tell you a joke", inline=False)
		embed.add_field(name="Von+Eval", value="Von will solve basic math problems", inline=False)
		embed.add_field(name="Von+Invite", value="Von will give you the link to invite him to your server", inline=False)
		embed.add_field(name="Von+Help", value="Von will show you all commands", inline=False)
		embed.add_field(name="Von+Quote", value="Von will recite a quote from the real Von Neumann", inline=False)
		embed.add_field(name="Von+Submit+Project", value="Von will walk you through how to submit a user project", inline=False)
		embed.set_thumbnail(url=client.user.avatar_url)
		await dm_user(id=message.author.id,embed=embed)
	
	#TODO this is the main purpose of this bot, to help with event submission, this where the code will come together to use the database

	elif is_calling_command(message.content, 'submit','project'):
		def check(mess):
			return mess.author == mess.author and mess.channel == mess.channel
		
		#PROJECT INFO COLLECTION

		static_connection = message.channel
		await static_connection.send("Enter Your Projects Signature:")
		signature = await client.wait_for('message',check=check)

		static_connection = signature.channel
		await static_connection.send("Enter the Name of Your Project: ")
		name = await client.wait_for('message',check=check)

		static_connection = name.channel
		await static_connection.send("Enter the Link of Your Project(one only): ")
		asset = await client.wait_for('message',check=check)

		#INITIALISING NEW INSTANCE OF PROJECT CLASS
		new_project = Project(signature.content,name.content,asset.content)

		#TODO, MAKE A VALIDITY CHECKER INSTANCE FUNCTION FOR EACH new_project OBJECT

		addProject(new_project)

		connection = message.channel
		await connection.send("In Dev")

	elif is_calling_command(message.content,'eval',current_channel=message.channel.id,allowed_channel=channel_dictionary['bot_commands']):
		connection= client.get_channel(channel_dictionary["bot_commands"])	
		equation = unpack_math(message.content)
		await connection.send(f"{equation} = {eval(equation)}")
	
	elif is_calling_command(message.content,'purge') and (message.channel.permissions_for(message.author).administrator or message.author.id == 765972771418275841):
		connection= client.get_channel(message.channel.id)
		limit = -1
		count = 0
		for word in message.content:
			if word.isdigit():
				#for word in message.content parses 12 as 1 then 2
				#cycles thru and concatatnates 1 and 2 to make "12" then converts to int
				if count != 0:
					limit = limit + word
				else:
					limit = word
					count += 1
		limit = int(limit)
		await connection.purge(limit=(limit+1 if limit != -1 else 1000))


	elif is_calling_command(message.content,"hi"):
		connection = message.channel
		await connection.send(f"hi {message.author.name}!")


	#@BAN COMMAND
	elif is_calling_command(message.content,"ban",prefix=prefix) and (message.channel.permissions_for(message.author).administrator or message.author.id == 765972771418275841) and not(str(client.user.id) in get_ids(message.content) or str(message.author.id) in get_ids(message.content)) and ban_kick == True:
		connection = client.get_channel(message.channel.id)
		reason = get_reason(message.content);reason = "Cause we said so" if reason is None else f"Reason: \"{get_reason(message.content)}\""
		for obj in get_member_objects(message.content):
			embed=discord.Embed(title=f"You have been banned from {message.channel.guild.name}!", description=reason, color=0xff0000); embed.set_thumbnail(url="https://i.redd.it/e77eetckule11.png")
			try:
				await dm_user(id=obj.id,embed=embed)
			except:
				pass
			await connection.guild.ban(obj, reason=reason)
		await connection.send("Banned!")
		#@BAN_LOGS
		if logs_enabled and channel_creator:
			connection = client.get_channel(ban_log_id)
			embed=discord.Embed(title="BAN_LOG", color=0x00ffee)
			for id_num in get_ids(message.content):
				member = await client.fetch_user(int(id_num))
				embed.add_field(name=f"{message.author} has banned: ", value=f"{member.name}: {id_num}", inline=False)
			embed.set_footer(text=reason)
			await connection.send(embed=embed)


	#@KICK COMMAND	
	elif is_calling_command(message.content,"kick",prefix=prefix) and (message.channel.permissions_for(message.author).administrator or message.author.id == 765972771418275841) and not(str(client.user.id) in get_ids(message.content) or str(message.author.id) in get_ids(message.content)) and ban_kick == True:
		connection = client.get_channel(message.channel.id)
		reason = get_reason(message.content);reason = "Cause we said so" if reason is None else f"Reason: {get_reason(message.content)}"
		connection = client.get_channel(message.channel.id)
		for obj in get_member_objects(message.content):
			embed=discord.Embed(title=f"You have been kicked from {message.channel.guild.name}!", description=reason, color=0xff0000); embed.set_thumbnail(url="https://irp-cdn.multiscreensite.com/87e31e8f/dms3rep/multi/blog-post-111-1.jpg")
			try:
				await dm_user(id=obj.id,embed=embed)
			except:
				pass
			await connection.guild.kick(obj, reason=reason)
		await connection.send("Kicked!")
		#@KICK_LOGS
		if logs_enabled and channel_creator:
			connection = client.get_channel(kick_log_id)
			embed=discord.Embed(title="KICK_LOG", color=0x00ffee)
			for id_num in get_ids(message.content):
				member = await client.fetch_user(int(id_num))
				embed.add_field(name=f"{message.author} has kicked: ", value=f"{member.name}: {id_num}", inline=False)
			embed.set_footer(text=reason)
			await connection.send(embed=embed)


	elif is_calling_command(message.content,"unban",prefix=prefix) and (message.channel.permissions_for(message.author).administrator or message.author.id == 765972771418275841) and not(str(client.user.id) in get_ids(message.content) or str(message.author.id) in get_ids(message.content)) and ban_kick == True:
		for id_num in get_ids(message.content):
			member = await client.fetch_user(int(id_num))
			await guild.unban(discord.Object(member.id))

			#Creates the embed for the dm and attemps to dm the user
			embedd=discord.Embed(title=f"You have been unbanned from {message.channel.guild.name}!", description="dw about it", color=0xff0000)
			try:
				await dm_user(id=id_num,embed=embedd)
			except:
				pass
			#Logs the unban in ban_logs
			embed=discord.Embed(title="UNBAN_LOG", color=0x00ffee)
			embed.add_field(name=f"{message.author} has unbanned: ", value=f"{member.name}: {id_num}", inline=False)
			connection = client.get_channel(channel_dictionary["ban_logs"])
			await connection.send(embed=embed)


	#Funny	
	elif is_calling_command(message.content,'wake','channels') and (message.channel.permissions_for(message.author).administrator or message.author.id == 765972771418275841):
		await message.delete()
		for channel in channel_dictionary:
			connection= client.get_channel(channel_dictionary[channel])
			await connection.send(".")
			await connection.purge(limit=1)


	elif is_calling_command(message.content,"test") and (message.channel.permissions_for(message.author).administrator or message.author.id == 765972771418275841):
		pass

	else:
		return

run_forever() if not testing else None
client.run(TOKEN)