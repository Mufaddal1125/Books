from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "userstable"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)    
    userreview = db.Column(db.String, db.ForeignKey("books.isbn"))

    def addUsers(name, password):
        user = Users(username=name, password=password)
        db.session.add(user)
        db.session.commit()

class Reviews(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer,primary_key = True)
    rating = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String, nullable = False)
    bookreview = db.Column(db.String, db.ForeignKey("books.isbn"))
    reviewer = db.Column(db.String, db.ForeignKey("userstable.id"))

    def addReview(self,rating,text):
        review = Reviews(rating = rating, text = text)
        db.session.add(review)
        db.session.commit()

class Books(db.Model):
    __tablename__ = "books"
    isbn = db.Column(db.String,primary_key=True, nullable = False)
    title = db.Column(db.String, nullable = False)
    author = db.Column(db.String, nullable = False)
    year = db.Column(db.Integer, nullable = False)
    # user_reviews = db.relationship("Reviews", backref="books", lazy=True)
    # users_who_review = db.relationship("Reviews", backref="books", lazy=True)

    def addBooks(isbn, title, author, year):
        book = Books(isbn=isbn,title=title,author=author,year=year)
        db.session.add(book)
        db.session.commit()