from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route("/")
def home():
	return render_template("index.html", content="Testing")

@app.route("/trade", methods=["POST", "GET"])
def trade():
	if request.method == "POST":
		user = request.form["nm"]
		return user
	else:
		return render_template("trade.html")

#@app.route("/rank", methods=["POST", "GET"])
#def rank():
#	if requeest.method == "POST":
#		user = request.form["nm"]
#		return redirect(url_for("user", usr=user))
#	else:
#		return render_template("rank.html")

if __name__ == "__main__":
	app.run(debug=True)
