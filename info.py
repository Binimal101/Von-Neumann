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

}
role_dictionary = {
	"@everyone" : 794843921501913108,
	"moderators" : 828880659811401731, 
	"head-moderators" : 829381821758046219,
	"creator" : 828881826927607819
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
		
	]
	return listOfCurses

def unpackExceptions():
	listOfExceptions = [
		"class",
		"grass",
		"lass",
		"brass",

	]
	return listOfExceptions