import urllib.request
from info import *
#Contains huge list of escape emoji's
from emoji import UNICODE_EMOJI

selective = unpackCustomCurses()
exceptions = unpackExceptions()
def isVulgar(message="hello"):
	boolean = bool
	message = message.split(" ")
	message = "+".join(message)
	connection = urllib.request.urlopen("http://www.wdylike.appspot.com/?q=" + message)
	output = connection.read(); connection.close
	output = str(output); output = output[2:-1]; output = output[0].upper() + output[1:]
	boolean = True if output == "True" else False
	return boolean
	
def censor(message="hello",author=None):
	message = message.split(" ")
	for word in message:
		if (isVulgar(word) or word in selective) and not word in exceptions:
			message[message.index(word)] = ("#")*len(word)		#    "||" + word + "||"
	message = " ".join(message)
	if author is None:
		return message
	else:
		return f"```ARM\n{str(author)[:-5]} said: {message}```"