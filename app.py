import os
from flask import Flask, render_template

app = Flask(__name__)

if os.environ.get("DEPLOYMENT_ENV") == "development":
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DEV_DATABASE_URI"]

if os.environ.get("DEPLOYMENT_ENV") == "heroku":
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)  # remove debug before final production deployment
