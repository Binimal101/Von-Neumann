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