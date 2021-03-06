from flask import Flask, render_template, redirect, url_for, request, flash, session
import requests
import json

app = Flask(__name__)
app.secret_key = '|\x93\xf2A\t\xa6-\xd1\x11\xe2}\x19M\x8ad\xb2\x80q\xa3\x7f\xbb4\xe7n'


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        country_input = request.form["country"]
        country_input_modified = request.form["country"].lower().replace(
            " ", "-")
        state_input = request.form["state"]
        graph_data = {}
        graph_data["Cases"] = []

        growth_over_time_api = requests.get(
            "https://api.covid19api.com/total/dayone/country/%s" % (country_input_modified)).json()
        country_covid_api = requests.get(
            "https://api.covid19api.com/summary").json()

        state_covid_api = requests.get(
            "https://api.covid19api.com/live/country/%s" % (country_input_modified)).json()

        countryCovidInformation = None
        stateCovidInformation = None
        # exceptions

        if(country_input == "United States"):
            country_input = "United States of America"

        for i in country_covid_api["Countries"]:
            if(i['Country'] == country_input):
                countryCovidInformation = i

        for i in state_covid_api:
            if(i['Province'] == state_input):
                stateCovidInformation = i

        if(countryCovidInformation):
            for i in growth_over_time_api:
                graph_data["Cases"].append({
                    'confirmed': i['Confirmed'],
                    'date': i['Date']
                })

        if(countryCovidInformation and stateCovidInformation):
            return render_template("find.html", apiConnection=True, countrySearch=True, stateSearch=True, countryCovidInformation=countryCovidInformation, stateCovidInformation=stateCovidInformation, graph_data=graph_data)
        elif(countryCovidInformation):
            return render_template("find.html", apiConnection=True, countrySearch=True, countryCovidInformation=countryCovidInformation, graph_data=graph_data)
        else:
            return render_template('find.html', apiConnectionFailed=True)
    return render_template("find.html")


@app.route("/about")
def about():
    world_covid_api = requests.get(
        "https://api.covid19api.com/world/total").json()
    return render_template("about.html", worldCovidInformation=world_covid_api)


@app.route("/local", methods=["POST", "GET"])
def local():
    if request.method == "POST":
        country_input = request.form["country"]
        country_input_modified = request.form["country"].lower().replace(
            " ", "-")
        state_input = request.form["state"]
        graph_data = {}
        graph_data["Cases"] = []

        growth_over_time_api = requests.get(
            "https://api.covid19api.com/total/dayone/country/%s" % (country_input_modified)).json()
        country_covid_api = requests.get(
            "https://api.covid19api.com/summary").json()

        state_covid_api = requests.get(
            "https://api.covid19api.com/live/country/%s" % (country_input_modified)).json()

        countryCovidInformation = None
        stateCovidInformation = None
        # exceptions

        if(country_input == "United States"):
            country_input = "United States of America"

        for i in country_covid_api["Countries"]:
            if(i['Country'] == country_input):
                countryCovidInformation = i

        for i in state_covid_api:
            if(i['Province'] == state_input):
                stateCovidInformation = i

        if(countryCovidInformation):
            for i in growth_over_time_api:
                graph_data["Cases"].append({
                    'confirmed': i['Confirmed'],
                    'date': i['Date']
                })

        session["countryCovidInformation"] = countryCovidInformation
        session["stateCovidInformation"] = stateCovidInformation
        if(countryCovidInformation and stateCovidInformation):
            return render_template("local.html", graph_data=graph_data)
        elif(countryCovidInformation):
            return render_template("local.html", graph_data=graph_data)
        else:
            return render_template('local.html')
    return render_template("local.html")


@app.route("/change_location")
def change_location():
    session.clear()
    return redirect(url_for("local"))


if __name__ == "__main__":
    app.run(debug=True)
