import csv
import os

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
   

    user = User.query.filter_by(email="becky@becky.com").first()
    print (f"user {user.firstname} id: {user.id}")


    categories = Category.query.all()
    for cat in categories:
        print(f"{cat.description}")


    category1 = Category.query.filter_by(description="JavaScript").first()
    for link in category1.links:
      print(f"category 1 links: {link}")


    link1 = Link.query.filter_by(description="Google").first()
    for cat in link1.categories:
        print(f"link 1 cats: {cat}")



if __name__ == "__main__":
    with app.app_context():
        main()

#https://gist.github.com/SuryaSankar/10091097