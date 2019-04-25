import csv
import os

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def add_link_and_categories(user_id,url, description, cat_list, public=True):
    link = Link(user_id=user_id,url=url, description=description, public=public)
    link.add_categories(cat_list)
    db.session.add(link)
    db.session.commit()

def main():
    # get user
    user = User.query.filter_by(email="becky@becky.com").first()
    # link = Link(user_id=user.id,url="https://www.google.com", description="Google", public=True)
    # cat1 = Category.query.filter_by(description="Work").first()
    # cat2 = Category.query.filter_by(description="Shopping").first()
    # link.add_categories([cat1, cat2])
    # db.session.add(link)
    # db.session.commit()

    work_cat = Category.query.filter_by(description="Work").first()
    shopping_cat = Category.query.filter_by(description="Shopping").first()
    bills_cat = Category.query.filter_by(description="Bills").first()
    education_cat = Category.query.filter_by(description="Education").first()

    # add_link_and_categories(user.id,"https://www.google.com","Google",[work_cat,shopping_cat],public=True)
    # add_link_and_categories(user.id,"https://www.amazon.com","Amazon",[shopping_cat],public=True)
    add_link_and_categories(user.id,"https://www.amazon.com","Amazon",[shopping_cat],public=True)
    add_link_and_categories(user.id,"https://cs50.harvard.edu/web/2019/spring/","Harvard python class",[education_cat],public=False)
    add_link_and_categories(user.id,"https://becu.com","Credit Union",[bills_cat],public=False)


   

    links = Link.query.all()
    for link in links:
        print(link.url)
        for cat in link.categories:
            print(cat.description)

if __name__ == "__main__":
    with app.app_context():
        main()
