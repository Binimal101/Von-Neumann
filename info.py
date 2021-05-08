channel_dictionary = {
	"general" : 828893565404184606,
	"bot_commands" : 828898842866221137,
	"events" : 829910548669399050,
	"mods-chat" : 828902637679411230,
	"events" : 829910548669399050,
	"partnerships" : 829736299577475083,
	"group-projects" : 828891677996613662,
	"memes" : 833701727172952127,
	"PYTHON" : 828892242604851200,
	"C" : 828892272787587103,
	"JS" : 828892315593605180,
	"JAVA" : 828892335484043275,
	"ARDUINO" : 828892397441777684,
	"RASPBERRY" : 828892428323913749,
	"hardware" : 828892882085085184,
	"general_support" : 828919736032165898,
	"tau" : 828974659286073354,
	"radar" : 828979948584697957,
	"discord_bot" : 828986793436250132,
	"database" : 829889952283623475,
	"gaming" : 828918183645282354,
	"ban_logs" : 837726869520252958,
	"kick_logs" : 837729254803243078,
	"guild_logs" : 837726761005482034,
	
}
role_dictionary = {
	"@everyone" : 794843921501913108,
	"moderators" : 828880659811401731, 
	"head-moderators" : 829381821758046219,
	"creator" : 828881826927607819,
	"mixed-engineers" : 838658069771583518,
}

ADMIN = [role_dictionary["creator"],role_dictionary["head-moderators"],role_dictionary["moderators"]]
def is_admin(ids):
	admin_bool = False
	for id in ids:
		if id in ADMIN:
			admin_bool = True
	return admin_bool

def unpackCustomCurses():
	listOfCurses = [
		"penis",
		"sex",
		"semen",
		"faggot",
		"bitch",
		"F̷U̶C̸K̸ ̵Y̴O̵U̸",
		"F̷U̶C̸K̸",
		"F̵U̶C̵K̴",
		"F̷̐̂Ù̷̾C̸͌̑K̷͂͆",
		"F̵̍͐U̶̍͗C̸̓͝K̶̀̉",
		"slut",
		"whore",
		"fûck",
		"peenis",

		
	]
	return listOfCurses

def unpackExceptions():
	listOfExceptions = [
		"class",
		"grass",
		"lass",
		"brass",
		"classroom",
		"assume",
		"assuming",
		"passwords",
		"password",
		"pass",
		"passes",
		"passed",
		"chassis",
		
	]
	return listOfExceptions
	
def unpackVonQuotes():
	von_quotes = [
		"If people do not believe that mathematics is simple, it is only because they do not realize how complicated life is.",
		"Anyone who attempts to generate random numbers by deterministic means is, of course, living in a state of sin.",
		"There's no sense in being precise when you don't even know what you're talking about.",
		"It would appear that we have reached the limits of what it is possible to achieve with computer technology, although one should be careful with such statements, as they tend to sound pretty silly in 5 years.",
		"You insist that there is something a machine cannot do. If you tell me precisely what it is a machine cannot do, then I can always make a machine which will do just that.",
		"If you tell me precisely what it is a machine cannot do, then I can always make a machine which will do just that.",
		"Computers are like humans - they do everything except think.",
		"The sciences do not try to explain, they hardly even try to interpret, they mainly make models. By a model is meant a mathematical construct which, with the addition of certain verbal interpretations, describes observed phenomena. The justification of such a mathematical construct is solely and precisely that it is expected to work-that is, correctly to describe phenomena from a reasonably wide area.",
		"Truth is much too complicated to allow anything but approximations.",
		"Science, as well as technology, will in the near and in the farther future increasingly turn from problems of intensity, substance, and energy, to problems of structure, organization, information, and control.",
		"The total subject of mathematics is clearly too broad for any of us. I do not think that any mathematician since Gauss has covered it uniformly and fully; even Hilbert did not and all of us are of considerably lesser width quite apart from the question of depth than Hilbert.",
		"With four parameters I can fit an elephant, and with five I can make him wiggle his trunk.",
		"All stable processes we shall predict. All unstable processes we shall control.",
		"There probably is a God. Many things are easier to explain if there is than if there isn't.",
		"Technological possibilities are irresistible to man. If man can go to the moon, he will. If he can control the climate, he will.",
		"I am thinking about something much more important than bombs. I am thinking about computers.",
		"There is no point in being precise if you do not even know what you are talking about.",
		"Young man, in mathematics you don't understand things. You just get used to them.",
		"I would like to make a confession which may seem immoral: I do not believe in Hilbert space anymore.",
		"The calculus was the first achievement of modern mathematics and it is difficult to overestimate its importance. I think it defines more unequivocally than anything else the inception of modern mathematics; and the system of mathematical analysis, which is its logical development, still constitutes the greatest technical advance in exact thinking.",
		"When we talk mathematics, we may be discussing a secondary language built on the primary language of the nervous system.",
		"You don't have to be responsible for the world that you're in.",
		"Problems are often stated in vague terms... because it is quite uncertain what the problems really are.",
		"By and large it is uniformly true that in mathematics there is a time lapse between a mathematical discovery and the moment it becomes useful; and that this lapse can be anything from 30 to 100 years, in some cases even more; and that the whole system seems to function without any direction, without any reference to usefulness, and without any desire to do things which are useful.",
		"It is exceptional that one should be able to acquire the understanding of a process without having previously acquired a deep familiarity with running it, with using it, before one has assimilated it in an instinctive and empirical way... Thus any discussion of the nature of intellectual effort in any field is difficult, unless it presupposes an easy, routine familiarity with that field. In mathematics this limitation becomes very severe.",
		"Life is a process which may be abstracted from other media.",
		"You wake me up early in the morning to tell me I am right? Please wait until I am wrong.",
		"Any one who considers arithmetical methods of producing random digits is, of course, in a state of sin. For, as has been pointed out several times, there is no such thing as a random number– there are only methods to produce random numbers, and a strict arithmetic procedure of course is not such a method.",
		"The emphasis on mathematical methods seems to be shifted more towards combinatorics and set theory - and away from the algorithm of differential equations which dominates mathematical physics.",
		"There's no sense in being precise when you don't even know what you're talking about"
		"It is just as foolish to complain that people are selfish and treacherous as it is to complain that the magnetic field does not increase unless the electric field has a curl. Both are laws of nature.",
		"The most vitally characteristic fact about mathematics is, in my opinion, its quite peculiar relationship to the natural sciences, or more generally, to any science which interprets experience on a higher than purely descriptive level.",
		"If one has really technically penetrated a subject, things that previously seemed in complete contrast, might be purely mathematical transformations of each other.",
		"Kurt Godel's achievement in modern logic is singular and monumental - indeed it is more than a monument, it is a landmark which will remain visible far in space and time. ... The subject of logic has certainly completely changed its nature and possibilities with Godel's achievement.",
		"I am a little troubled about the tea service in the electronic computer building. Apparently the members of your staff consume several times as much supplies as the same number of people do in Fuld Hall and they have been especially unfair in the matter of sugar.... I should like to raise the question whether it would not be better for the computer people to come up to Fuld Hall at the end of the day at 5 o'clock and have their tea here under proper supervision.",

		]
	return von_quotes