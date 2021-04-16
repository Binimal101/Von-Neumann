import urllib.request
def isVulgar(string,message):
	copy = message
	for word in copy:
		connection = urllib.request.urlopen("http://www.wdylike.appspot.com/?q=" + string)
		if connection:
			ind = message.index(word)
			endInd = len(word) + ind
			output = True
			message = message[:ind] + ("*")*len(word) + message[endInd:]
		else:
			continue
		output = connection.read()
	connection.close
	return output, message