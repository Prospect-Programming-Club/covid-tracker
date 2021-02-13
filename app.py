from flask import Flask, render_template, redirect, url_for, request, flash
import requests
import json
import pycountry

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        country_input = request.form["country"]
        country_covid_api = requests.get(
            "https://api.covid19api.com/summary").json()

        covidInformation = None
        # exceptions
        if(country_input == "United States"):
            country_input = "United States of America"

        for i in country_covid_api["Countries"]:
            if(i['Country'] == country_input):
                covidInformation = i
        if(covidInformation):
            return render_template('find.html', apiConnection=True, covidInformation=covidInformation)
        else:
            return render_template('find.html', apiConnectionFailed=True)
    return render_template("find.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/local")
def local():
    return render_template("local.html")


if __name__ == "__main__":
    app.run(debug=True)
