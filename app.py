from flask import Flask, render_template, redirect
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("find.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/local")
def local():
    return render_template("local.html")


if __name__ == "__main__":
    app.run(debug=True)
