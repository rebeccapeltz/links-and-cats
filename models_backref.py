from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Index, Column, Integer, ForeignKey, engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func, Index


Base = declarative_base()

db = SQLAlchemy()

# drop table public.users cascade;
# drop table public.links cascade;
# drop table public.categories cascade;


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.Integer, nullable=False)
Index('idx_user_email', func.lower(User.email))


# set up many to many relationship between categories and links

class Link(db.Model):
    __tablename__ = "links"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)

    #category.links
    categories = db.relationship("Category", backref="links", cascade="all, delete-orphan", lazy=True)



class Category(db.Model):
  __tablename__ = "categories"
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String, nullable=False)
  links = db.relationship("Link", backref="category", lazy=True)
  link_id = db.Column(db.Integer, db.ForeignKey("links.id"))
  #link.categories
  categories = db.relationship("Link", backref="categories", cascade="all, delete-orphan", lazy=True)


Index('idx_cat_description', func.lower(Category.description))
