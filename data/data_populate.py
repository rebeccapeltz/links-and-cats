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

    user = User.query.filter_by(email="becky@becky.com").first()
    print (f"user {user.firstname} id: {user.id}")

    # first create category list
    category1 = Category(description="JavaScript")
    category2 = Category(description="CSS")
    db.session.add_all([category1, category2])
    print(f"Added JavaScript")
    db.session.commit()

    categories = Category.query.all()
    for cat in categories:
        print(f"{cat.description}")

    # create link and add categories
    link = Link(user_id=user.id,url="https://www.google.com", description="Google")
    db.session.add(link)
    link = Link(user_id=user.id,url="https://www.amazon.com", description="Amazon")
    db.session.add(link)
    db.session.commit()



    link1 = Link.query.filter_by(description="Google").first()
    link1.add_categories(categories)

    for cat in link1.categories:
        print(f"link 1 cats: {cat}")



if __name__ == "__main__":
    with app.app_context():
        main()

#https://gist.github.com/SuryaSankar/10091097