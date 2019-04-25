import csv
import os

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'categories.csv')
    f = open(filename)
    reader = csv.reader(f)
    for description in reader:
        cat = Category(description=description[0])
        db.session.add(cat)
    db.session.commit()

    categories = Category.query.all()
    for cat in categories:
        print(cat.description)

if __name__ == "__main__":
    with app.app_context():
        main()
