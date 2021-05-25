import bs4
import requests
from flask import Flask, render_template, url_for, request, redirect
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def home():
	return render_template("index.html", content="Testing")

@app.route("/trade", methods=["POST", "GET"])
def trade():
	if request.method == "POST":
		user = request.form["nm"]
		user2 = request.form["xm"]
		userEnv = [user, user2]
		statline_prod2 = {}
		index = 1;
		for x in userEnv:
			target_id = get_id(x)

			if target_id == "-1":
				error = { "developerMessage" : "No matching player ID was found",
				"userMessage" : "The player's name was not recognized. Make sure the player's name is spelled correctly."}
				return error

			target_url = "https://www.espn.com/nba/player/_/id/" + str(target_id)
			target_url = target_url.strip('\n')
			page = requests.get(str(target_url))
			soup = BeautifulSoup(page.text, 'html.parser')
			team_record = soup.find('div', class_ = 'Gamestrip__Record db n10 clr-gray-03').get_text()
			total_games_played = 0
			for num in team_record.split("-"):
				total_games_played += int(num)
			statline2 = soup.find('section', class_ = 'Card PlayerStats').find('div', class_ = 'Table__Scroller').find_all(class_ = "Table__TD")
			GP = statline2[0].get_text()
			total_games_played -= int(GP)
			statline_prod2[index] = [x, statline2[2].get_text(), statline2[4].get_text(), statline2[3].get_text(), statline2[11].get_text(), statline2[5].get_text(), statline2[6].get_text(), statline2[8].get_text(), statline2[7].get_text(), statline2[10].get_text(), total_games_played]
			index += 1
			#return redirect(url_for("tradecomp", tra=statline_prod))
			#return statline_prod
		input1 = statline_prod2[list(statline_prod2)[0]][1:]
		input2 = statline_prod2[list(statline_prod2)[1]][1:]
		output = [round_up(float(e1)-float(e2)) for (e1, e2) in zip(input1, input2)]
		statline_prod2["differential"] = ["+/-"]
		statline_prod2["differential"].extend(output)
		return render_template("tradetable.html", result=statline_prod2)
		#stat_table3 = stat_table2.find("tr", {"class": "Table__TR Table__TR--sm Table__even"})
	else:
		return render_template("trade.html")

@app.route("/ranking")
def ranking():
	stattable_url = "https://www.espn.com/nba/stats/player/_/table/general/sort/PER/dir/desc"
	page = requests.get(str(stattable_url))
	soup = BeautifulSoup(page.text, 'html.parser')
	return render_template("ranking.html")

#@app.route("/tradecomp")
#def tradecomp():
 #  tra = request.args.get("tra")
 #   return tra

def get_id(player_name):
	file = open("playerIDs.txt", "r", encoding='utf-8')
	for line in file:
		if player_name in line:
			return line.split(", ")[1]
	return str(-1)

def round_up(stat):
	return round(stat, 2)

	

#@app.route("/rank", methods=["POST", "GET"])
#def rank():
#   if requeest.method == "POST":
#       user = request.form["nm"]
#       return redirect(url_for("user", usr=user))
#   else:
#       return render_template("rank.html")

if __name__ == "__main__":
	app.run(debug=True)
