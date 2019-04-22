from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Index, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func, Index


Base = declarative_base()

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.Integer, nullable=False)
Index('idx_user_email', func.lower(User.email))


# set up many to many relationship between categories and links

cat_link_table = Table('association', Base.metadata,
    Column('left_id', Integer, ForeignKey('left.id')),
    Column('right_id', Integer, ForeignKey('right.id'))
)

class Link(db.Model):
    __tablename__ = "left"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    categories = relationship(
        "Category",
        secondary=cat_link_table,
        back_populates="links")

class Category(db.Model):
  __tablename__ = "right"
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String, nullable=False)
  categories = relationship(
        "Link",
        secondary=cat_link_table,
        back_populates="categories")

Index('idx_cat_description', func.lower(Category.description))
