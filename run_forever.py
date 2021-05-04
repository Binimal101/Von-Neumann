import flask, threading
app = flask.Flask('')
@app.route('/')
def home():
	while True:
		return "Von is up and running!"
def running():
	app.run(host="0.0.0.0",port=8080)
def run_forever():
	socket = threading.Thread(target=running)
	socket.start()
	return 