#WILL IMPACT RUN FOREVER FUNCTION
testing = False
#Main imports
from run_forever import run_forever #RUN_FOREVER VIA UPTIMEROBOTS
import discord, sqlite3, os, random, asyncio, urllib.request
import pyjokes as joke
from hashlib import sha256
from discord.ext import commands
from discord.ext.commands import *
import replit, getpass
#File Imports
from info import *
from helper import *
from profanity import *
#On Start Custom Info
link_chars = [".net","www.","https://",".com",".org","http",".co"] #gets rid of any links with at least one of these in the string, Expandable
prefix = "!"
logs_enabled = True
channel_creator = False
link_killer = False
profanity_filter = True
ban_kick = True
ratetimer = 0
rates = {}
ratelimited_users = {}

replit.clear()

#TO PREVENT VIEWERS FROM RUNNING THE BOT, PASSWORD WILL BE PINNED TO MOD-CHAT

usr_password = sha256(getpass("ENTER ACTIVATION PASSWORD\n>>> ").encode()).hexdigest()
if usr_password == os.environ['Password']:
	replit.clear()
	TOKEN = os.environ['TOKEN']
	print("**ONLINE**")

#DISCORD.PY

#bot creation

intents = discord.Intents.default()
intents = intents.all()

activity = discord.Activity(type=discord.ActivityType.listening, name="developer team") #Gives bot a custom status :pog:
permissions = discord.Permissions(administrator=True)
client = discord.Client(intents=intents,activity=activity,permissions=permissions)


#Global Scoped Helper Function
async def dm_user(message=None,embed=None,id=None):
		if id is not None:
			recipient = await client.fetch_user(id)
			if message is not None and embed is None:
				await recipient.send(message)

			elif message is None and embed is not None:
				await recipient.send(embed=embed)

			elif message is not None and embed is not None:
				await recipient.send(message, embed=embed)

async def ratecheck(ctx):
	global rates, ratelimited_users
	#If user has not taken any action in the psat 15 seconds
	if ctx.author.id not in rates:
		rates[ctx.author.id] = 1
	if rates[ctx.author.id] > 45:
		role_history = []
		#Get mute role
		muted_role = discord.utils.get(guild.roles, name="Muted")
		#Get member
		member = ctx.message.author
		role_history += member.roles

		#Remove all user roles and mute user
		for role in member.roles:
			if role.name != "@everyone":
				await member.remove_roles(role)
		await member.add_roles(muted_role)

		ratelimited_users[ctx.author.id] = "Blocked."
		await dm_user(message="You are being ratelimited and have been muted for 5 minutes as a consequence. Ratelimiting can occur when a user takes more than three actions per second.", id=ctx.author.id)
		#Mute for 5 minutes
		await asyncio.sleep(300)

		#Add roles and unmute after 10 minutes
		for role in role_history:
			if role.name != "@everyone":
				await member.add_roles(role)
		await member.remove_roles(muted_role)
		del ratelimited_users[ctx.author.id]

@Bot.before_invoke(ratecheck)

#events
@client.event
async def on_ready():
	global ratetimer, rates
	connection= client.get_channel(channel_dictionary["bot_commands"])
	await connection.send("What's up Mixed Engineers")
	await dm_aly()
	while True:
		await asyncio.sleep(1)
		if ratetimer == 15:
			ratetimer = 0
			rates = {}
		ratetimer += 1

@client.event
async def on_raw_reaction_add(payload):
	global ratelimited_users
	if payload.user_id in ratelimited_users:
		return
	Guild = client.get_guild(payload.guild_id) #gets guild object from the parameter, should work on multiple servers
	if Guild.id != 794843921501913108: #to just keep this while its in the works on this server
		return

	if payload.channel_id == 828876919936253952:
		Channel = discord.utils.get(Guild.channels, name="📝rules")
		Message = await Channel.fetch_message(payload.message_id)
		Emoji = payload.emoji
		Role = discord.utils.find(lambda x: x.name == Emoji.name, Guild.roles) #should work as long as role name and emoji name are the same
		reactor = discord.utils.find(lambda u: u.id == payload.user_id, Guild.members)
		#Will run if info above is viable
		if reactor is not None and not payload.user_id == client.user.id:
			if Role in reactor.roles:
				await reactor.remove_roles(Role)
				try: #Runs if the user already has the role
					await dm_user(id=reactor.id,message=f"Now why did you do that?")
				except:
					pass
			else: #Runs if the user does not already have the role
				await reactor.add_roles(Role)
				try:
					await dm_user(id=reactor.id,message=f"Welcome to the server!")
				except:
					pass

			#Removes reactors reaction
			snowflake = discord.Object(reactor.id)
			await Message.remove_reaction(Emoji, snowflake)

	#React Roles channel only react roles
	if payload.channel_id == 839854066922160138:
		Channel = discord.utils.get(Guild.channels, name="📝react_roles")
		Message = await Channel.fetch_message(payload.message_id)
		Emoji = payload.emoji
		Role = discord.utils.find(lambda x: x.name == Emoji.name, Guild.roles) #should work as long as role name and emoji name are the same
		reactor = discord.utils.find(lambda u: u.id == payload.user_id, Guild.members)
		#Will run if info above is viable
		if reactor is not None and not payload.user_id == client.user.id:
			if Role in reactor.roles:
				await reactor.remove_roles(Role)
				try:
					await dm_user(id=reactor.id,message=f"You have removed the role: {Role.name}")
				except:
					pass
			else:
				await reactor.add_roles(Role)
				try:
					await dm_user(id=reactor.id,message=f"You have gained the role: {Role.name}")
				except:
					pass
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


async def add_reactions_to_message(emoji_name,channel_name,message_id,guild=794843921501913108):
	Guild = client.get_guild(guild)
	Channel = discord.utils.get(Guild.channels, name=channel_name)
	Message = await Channel.fetch_message(message_id)
	Emoji = discord.utils.find(lambda x: x.name == emoji_name,Guild.emojis)
	await Message.add_reaction(Emoji)


@client.event
async def on_member_join(member):
	channel = client.get_channel(828876919936253952)
	message = await channel.fetch_message(840474974262919198)
	await message.clear_reactions()
	await add_reactions_to_message("MixedEngineers","📝rules",840474974262919198)

@client.event
async def on_message(message):
	#So bot will not respond inside a DMChannel
	if isinstance(message.channel, discord.channel.DMChannel):
		return

	connection = message.channel
	guild = client.get_guild(message.channel.guild.id)

	if logs_enabled and channel_creator:
		ban_logger = discord.utils.get(connection.guild.text_channels, name="⚠ban_logs")
		if ban_logger is None: #ADDS THESE CHANNELS TO SERVERS WITHOUT THEM
			await connection.guild.create_text_channel('⚠ban_logs')
			ban_logger = discord.utils.get(connection.guild.text_channels, name="⚠ban_logs")
			await ban_logger.set_permissions(connection.guild.default_role, send_messages=False)

		kick_logger = discord.utils.get(connection.guild.text_channels, name="⚠kick_logs")
		if kick_logger is None: #ADDS THESE CHANNELS TO SERVERS WITHOUT THEM
			await connection.guild.create_text_channel('⚠kick_logs')
			kick_logger = discord.utils.get(connection.guild.text_channels, name="⚠kick_logs")
			await kick_logger.set_permissions(connection.guild.default_role, send_messages=False)

		try:
			kick_log_id = discord.utils.get(connection.guild.text_channels, name="⚠kick_logs").id
			ban_log_id = discord.utils.get(connection.guild.text_channels, name="⚠ban_logs").id
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

	elif (isVulgar(message.content) or len([x for x in unpackCustomCurses() if x in message.content.lower()]) > 0) and profanity_filter:
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
		if new_project == None:
			await static_connection.send("INVALID ENTRY, TRY AGAIN")
		else:
			addProject(new_project)
			connection = message.channel
			await connection.send("Project Submitted Successfully!")

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

	elif is_calling_command(message.content,"server","ip",current_channel=message.channel.id,allowed_channel=838653416733409290):
		connection = message.channel
		await connection.send(f"The Minecraft Server's IP is: {ip}")

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
		if logs_enabled:
			connection = client.get_channel(837726869520252958)
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
		if logs_enabled:
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
			if logs_enabled:
				embed=discord.Embed(title="UNBAN_LOG", color=0x00ffee)
				embed.add_field(name=f"{message.author} has unbanned: ", value=f"{member.name}: {id_num}", inline=False)
				connection = client.get_channel(channel_dictionary["ban_logs"])
				await connection.send(embed=embed)


	elif is_calling_command(message.content,"slowmode",prefix=prefix) and (message.channel.permissions_for(message.author).administrator or message.author.id == 765972771418275841):
		channel = message.channel.id # Subclass of TextChannel ABC
		channel = discord.utils.find(lambda channel_: channel == channel_.id,guild.channels) #TextChannel ABC, has needed methods

		#Toggle
		delay = get_slowmode_timer(message.content)
		if channel.slowmode_delay == 0 and delay is None:
			delay = 5
		elif channel.slowmode_delay != 0 and delay is None:
			delay = 0
		else:
			delay = int(get_slowmode_timer(message.content))

		await channel.edit(slowmode_delay = delay)
		endis = "Disabled" if delay == 0 else "Enabled"
		await channel.send(f"Slowmode {endis}, set to {delay} seconds")




	elif is_calling_command(message.content,"timeout",prefix=prefix) and (message.channel.permissions_for(message.author).administrator or message.author.id == 765972771418275841) and not(str(client.user.id) in get_ids(message.content) or str(message.author.id) in get_ids(message.content)):
		#store previous roles in a list
		role_history = []
		muted_role = discord.utils.get(guild.roles, name="Muted")
		mute_time = int(get_mute_duration(message.content)) if get_mute_duration(message.content) is not None else 30
		users = get_ids(message.content)
		for userid in users:
			users[users.index(userid)] = int(userid) #using for discord.utils.find easy of use
		for user in users:
			member = discord.utils.find(lambda x: x.id == user, guild.members)
			role_history.append(member.roles)

		for user in users:
			member = discord.utils.find(lambda x: x.id == user, guild.members)
			for role in member.roles:
				if role.name != "@everyone":
					await member.remove_roles(role)
			await member.add_roles(muted_role)

		await asyncio.sleep(mute_time*60)

		for i in range(len(users)):
			member = discord.utils.find(lambda x: x.id == users[i], guild.members)
			for role in role_history[i]:
				if role.name != "@everyone":
					await member.add_roles(role)
			await member.remove_roles(muted_role)

	#Funny
	elif is_calling_command(message.content,'wake','channels') and (message.channel.permissions_for(message.author).administrator or message.author.id == 765972771418275841):
		await message.delete()
		for channel in channel_dictionary:
			connection= client.get_channel(channel_dictionary[channel])
			await connection.send(".")
			await connection.purge(limit=1)


	elif is_calling_command(message.content,"reactions","add","to","message") and (message.channel.permissions_for(message.author).administrator or message.author.id == 765972771418275841):
		skills = [["None", "Beginner", "Advanced", "Expert"],839915873417953330]
		languages = [["Python","RaspberryPi","Javascript","Java","Arduino","PHP","HTML_CSS"],839855261623517234]
		terms = languages
		#for item in terms[0]:
		await add_reactions_to_message("MixedEngineers","📝rules",839849973411086386)

	# elif is_calling_command(message.content,"test") and (message.channel.permissions_for(message.author).administrator or message.author.id == 765972771418275841):
	# 	from pprint import pprint
	# 	member = discord.utils.find(lambda x: x.id == , guild.members)
	# 	print(member.name, member.id)
	# 	pprint(member.roles)


	else:
		return
run_forever() if not testing else None
client.run(TOKEN)
