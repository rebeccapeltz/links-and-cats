from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Index, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func, Index
import uuid


Base = declarative_base()

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, nullable=False)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)

    def __init__(self, email, firstname, lastname):
        self.id = uuid.uuid4().hex
        self.email = email
        self.firstname = firstname
        self.lastname = lastname


Index('idx_user_email', func.lower(User.email))


# set up many to many relationship between categories and links


class Link_Category(db.Model):
    __tablename__ = "link_category"
    id = Column(db.String, primary_key=True, unique=True)
    link_id = Column(db.String, ForeignKey('links.id'), primary_key=True)
    category_id = Column(db.String, ForeignKey('categories.id'), primary_key=True)

    link = relationship("Link", backref=backref("link_category", cascade="all, delete-orphan" ))
    category = relationship("Category", backref=backref("link_category", cascade="all, delete-orphan" ))

    def __init__(self, link, category):
        self.id = uuid.uuid4().hex
        self.link_id = link.id
        self.category_id =  category.id

    def __repr__(self):
        return '<Link Category {}>'.format(self.link.url+" "+self.category.description)

class Link(db.Model):
    __tablename__ = "links"
    id = db.Column(db.String, primary_key=True)
    url = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    user_id = db.Column(db.String, db.ForeignKey("users.id"), nullable=False)
    categories = relationship("Category", secondary="link_category")

    def __init__(self, url, description, user_id):
        self.id = uuid.uuid4().hex
        self.user_id = user_id
        self.url = url
        self.description = description
        self.categories=[]
    
    # param is a list of categories
    def add_categories(self, category_list):
        for category in category_list:
            self.link_category.append(Link_Category(link=self, category=category))
      
    def __repr__(self):
        return f"Link: id {self.id} url: {self.url}"


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.String, primary_key=True)
    description = db.Column(db.String, nullable=False)
    links = relationship("Link", secondary="link_category")

    def __init__(self,description):
        self.id = uuid.uuid4().hex
        self.description = description
        self.links=[]

    def __repr__(self):
        return f"Category: id {self.id} desc: {self.description}"



Index('idx_cat_description', func.lower(Category.description))
