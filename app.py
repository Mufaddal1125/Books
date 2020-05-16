import os, requests
from models import *
from flask import Flask, session, render_template, request, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
dbname = "postgres://postgres:mufaddal2460@localhost/users"
app.config["SQLALCHEMY_DATABASE_URI"] = dbname
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'
db.init_app(app)


@app.route("/")
def index():
    return render_template("index.html", title="Register")

@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    password = request.form.get("password")
    #check if user already exists
    users = Users.query.filter(Users.username == name).first()
    if  not users is None:
        return render_template("index.html", msg="User Already Registered", alert_type="alert-danger")
    Users.addUsers(name = name,password = password)
    return render_template("index.html", msg="Successfully Created User", alert_type="alert-success")

@app.route("/redirlogin")
def redirlogin():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():

    name = request.form.get("name")
    password = request.form.get("password")

    if session.get("user") is None:
        session["user"] = []
    
    users = Users.query.filter(Users.username == name, Users.password == password).first()
    if users:
        session["user"].append(users.id)

    if users is None:
        return render_template("index.html", msg = "Error User Not Found")
    else: 
        return render_template('dashboard.html')

@app.route("/dashboard", methods=["POST"])
def books():
    if session.get("user"):
        start = int(request.form.get('start') or 0)
        end = int(request.form.get('end') or (start + 9))

        book = {}
        for i in range(start, end + 1):
            book.append(Books.query.filter().limit(i).all())
        return jsonify(book)

@app.route("/logout")
def logout():
    session.clear()
    return render_template("index.html", title='Register')

@app.route("/search", methods=["GET"])
def search():
    isbn = request.args.get("isbn")
    title = request.args.get("title")
    author = request.args.get("author")
    year = str(request.args.get("year"))
    books = Books.query.filter(Books.isbn.like('%' + isbn + '%')|Books.title.like('%' + title+ '%')|Books.author.like('%' + author+ '%') | Books.year.like('%' + year + '%')).all()
    return render_template("dashboard.html", books = books)

@app.route("/bookreview", methods=["GET"])
def bookreview():
    isbns = request.args.get("isbns")
    if session.get('isbn') is None:
        session["isbn"] = []
    session['isbn'].append(isbns)
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key":"dASrcpv1JcJfNjXULI2QZg","isbns":isbns})
    view = res.json()
    review = Reviews.query.filter_by(bookreview=session['isbn'][0]).all()
    book = Books.query.filter(Books.isbn == isbns).first()
    return render_template("bookview.html",title = "Book Details", view = view, book = book,review=review)
@app.route("/bookreview", methods=["POST"])
def submitReview():
    
    user = session['user']
    isbns = session['isbn']
    # check if user has submitted a review for the same book
    check_user = Reviews.query.filter_by(reviewer = user[0]).first()
    check_book = Reviews.query.filter_by(bookreview = isbns[0]).first()
    if check_user and check_book:
        #dont submit review if user has already submitted the review
        return render_template("success.html",title = "Success",heading = "You can Only Submit Your Review Once",para = "You can Review another Books" ,msg = "Error Submitting Review")
    rating = request.form.get('rating')
    text = request.form.get('text')

    data = Reviews(rating=rating,text=text,bookreview=isbns[0],reviewer=user[0])
    db.session.add(data)
    db.session.commit()
    return render_template("success.html",title = "Success",heading = "Successfully Submitted Your Review",para = "Thanks For your Review",msg = "Successfully Submitted Review")