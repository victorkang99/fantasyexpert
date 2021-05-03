import bs4
import requests
from flask import Flask, render_template, url_for, request
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", content="Testing")

@app.route("/trade", methods=["POST", "GET"])
def trade():
    if request.method == "POST":
        user = request.form["nm"]
        target_id = get_id(user)

        if target_id == "-1":
            error = { "developerMessage" : "No matching player ID was found",
            "userMessage" : "The player's name was not recognized. Make sure the player's name is spelled correctly."}
            return error

        target_url = "https://www.espn.com/nba/player/gamelog/_/id/" + str(target_id)
        target_url = target_url.strip('\n')
        page = requests.get(str(target_url))
        soup = BeautifulSoup(page.text, 'html.parser')
        stat_table = soup.find('div', class_= 'summary_table')

        if stat_table is not None:
            statline = stat_table.find_all(class_="Table__TD")
            statline_prod = { "FG%": statline[3].get_text(),
                              "FT%": statline[7].get_text(),
                              "3P%" : statline[5].get_text(), 
                              "PTS": statline[14].get_text(), 
                              "REB": statline[8].get_text(),
                              "AST": statline[9].get_text(),
                              "STL": statline[11].get_text(),
                              "BLK": statline[10].get_text(),
                              "TO": statline[13].get_text() }
            return statline_prod

        else:
            return user
        #stat_table3 = stat_table2.find("tr", {"class": "Table__TR Table__TR--sm Table__even"})
    else:
        return render_template("trade.html")

def get_id(player_name):
    file = open("playerIDs.txt", "r", encoding='utf-8')
    for line in file:
        if player_name in line:
            return line.split(", ")[1]
    return str(-1)

#@app.route("/rank", methods=["POST", "GET"])
#def rank():
#   if requeest.method == "POST":
#       user = request.form["nm"]
#       return redirect(url_for("user", usr=user))
#   else:
#       return render_template("rank.html")

if __name__ == "__main__":
    app.run(debug=True)
