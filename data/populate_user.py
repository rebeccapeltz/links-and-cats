
import csv
import os

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    #create user
    user = User(email="becky@becky.com", firstname="beckyf", lastname="beckyl", password="password")
    db.session.add(user)
    db.session.commit()

    users = User.query.all()
    for user in users:
      print(user.email)

if __name__ == "__main__":
    with app.app_context():
        main()
