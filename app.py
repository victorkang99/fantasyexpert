from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
	return "Hello! this is the main page"
	return "i like penis"

if __name__ == "__main__":
	app.run()
