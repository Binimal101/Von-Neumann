import urllib.request
from info import *

selective = unpackCustomCurses()
exceptions = unpackExceptions()

def isVulgar(message="hello"):
	boolean = False
	message = message.split(" ") #message = "+".join(message)
	for word in message:
		try:
			connection = urllib.request.urlopen("http://www.wdylike.appspot.com/?q=" + word)
			output = connection.read(); connection.close
			output = str(output); output = output[2:-1]; output = output[0].upper() + output[1:]
			boolean = True if output == "True" or boolean else False
		except UnicodeEncodeError or InvalidURL:
			continue
	return boolean
	
def censor(message="hello",author=None):
	message = message.split(" ")
	for word in message:
		if (isVulgar(word) or word in selective) and not word.lower() in exceptions:
			message[message.index(word)] = ("#")*len(word)		#    "||" + word + "||"
	message = " ".join(message)
	if author is None:
		return message
	else:
		return f"```ARM\n{str(author)[:-5]} said: {message}```"
