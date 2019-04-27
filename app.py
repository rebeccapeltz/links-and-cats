import os

from flask import Flask, request, render_template, session, redirect, url_for
# from flask_session import Session
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
from models import *
from flask_session import Session

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
sess = Session()
sess.init_app(app)

# HOME login/logout/show public links by defaul
# if logged in show private links if any
@app.route("/", methods=["POST", "GET"])
# current_user is session variable for a logged in user
def index():
    current_user = None
    # logged in or not, return all public links
    public_links = Link.query.filter_by(public=True).all()
    private_links = None
    
    if 'current_user' in session:
        current_user = session["current_user"]
        private_links = Link.query.filter_by(public=False, user_id=current_user.id).all()
    return render_template("index.html", private_links=private_links, public_links=public_links,title="Home")
    

# returns empty array if input is valid
def validate_user(email, firstname, lastname, password, confirm_password):
    invalid = []
    if len(email) == 0:
        invalid.append("Email is required.")
    if (len(firstname) == 0):
        invalid.append("Firstname is required.")
    if (len(lastname) == 0):
        invalid.append("Lastname is required.")
    if (len(password) == 0):
        invalid.append("Password is required.")
    if (password != confirm_password):
        invalid.append("Password must match Password confirm.")
    return invalid

# REGISTER register a user but don't automatically login
@app.route("/register", methods=["POST"])
def register():
    # get data from form
    email_input = request.form.get("email-input")
    firstname_input = request.form.get("firstname-input")
    lastname_input = request.form.get("lastname-input")
    password_input = request.form.get("password-input")
    confirm_password_input = request.form.get("confirm-password-input")
    # validate
    if len(validate_user(email_input, firstname_input, lastname_input, password_input, confirm_password_input)) == 0:
        # add to database
        user = User(email=email_input, firstname=firstname_input,
                    lastname=lastname_input, password=password_input)
        db.session.add(user)
        db.session.commit()
        # write email to session
        # session.pop("current_user", None) // this breaks the session and produces
        # disconnected session error
        # session["current_user"] = user
        # send to index with success message
        return render_template("index.html", title="Home", success_msg="Successful user registration.")
    else:
        return render_template("index.html", title="Home", error_msg="Key in both email and password to login.")

# LOGOUT: logout user
@app.route("/logout", methods=["POST"])
def logout():
    session.pop("current_user", None)
    # session["current_user"] = None
    return redirect(url_for('index'))

# LOGIN: login user
@app.route("/login", methods=["POST"])
def login():
    # get data from form
    email_input = request.form.get("email-input")
    print(email_input)
    password_input = request.form.get("password-input")
    print(password_input)
    # validate
    if len(email_input) == 0 or len(password_input) == 0:
        return render_template("index.html", error_msg="Key in both email and password to login.", title="Home")
    # lookup in db
    try:
        user = User.query.filter_by(email=email_input).first()
        # add to session cache
        session["current_user"] = user
        # send to index
        return redirect(url_for('index'))
    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)
        return render_template("index.html", error_msg="Problem finding registered user during login.", title="Home")

@app.route("/form", methods=["GET"])
def form():
    categories = Category.query.all()
    default_entry = {"public": True, "url": "http://www.example.com", "title":"Example","description":"Description","categories":"JavaScript"}
    # print(default_entry)
    return render_template("form.html",categories=categories, default_entry=default_entry)

def add_link_and_categories(user_id,url,title, description, cat_list, public):
    link = Link(user_id=user_id,url=url,title=title, description=description, public=public)
    link.add_categories(cat_list)
    db.session.add(link)
    db.session.commit()

# ADD LINK: add a new link
@app.route("/add_link", methods=["GET", "POST"])
def add_link():
    categories = Category.query.all()
    # default_entry = {}
    default_entry = {"public": True, "url": "http://www.example.com", "title":"Example","description":"Description","categories":"JavaScript"}
    # if GET
    if request.method == "GET":
        # get a list of categories
        categories = Category.query.all()
        # print(categories)
        # call form with categories
        return render_template("form.html",categories=categories, default_entry=default_entry)
    elif request.method == "POST":
        public = True #default
        # get data from form 
        user_id = session["current_user"].id
        pubpriv_input = request.form.get("pubpriv-input")
        if pubpriv_input == "private":
            public = False
        url_input = request.form.get("url-input")
        title_input = request.form.get("title-input")
        description_input = request.form.get("description-input")
        category_input = request.form.getlist("category-input")
        print("cat input", category_input)
        print(user_id, url_input, title_input, description_input, category_input,public)
        # add link and categories
        # add_link_and_categories(user_id,url_input,title_input, description_input, cat_list, public)
        # go back to index with success message
    return redirect(url_for('index',success_msg="Link successfully added."))

# UPDATE LINK: update an existing link
@app.route("/update_link/<int:link_id>", methods=["GET","POST"])
def update_link(link_id):
    # if GET
    # get current data using link_id
    # prepare to update checked categories

    # if POST
    # get data from form
    # update link
    # remove all categories
    # add categories to link
    # rerun update to stay on form
    return render_template("form.html")

# DELETE LINK delete an existing link
@app.route("/delete_link/<int:link_id>", methods=["POST"])
def delete_link(link_id):
    # delete link category
    # delete link
    # go to home with success message
    print(link_id)
