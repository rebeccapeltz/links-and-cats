import os

from flask import Flask, request, render_template, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=["POST", "GET"])
# current_user is session variable for a logged in user
def index():
    current_user = None
    if (session.get("current_user") != None):
        current_user = session["current_user"]
    # logged in or not, return all public links

    # if user is logged in return the private links
    if request.method == "POST":
        #
        return render_template("index.html", current_user=current_user, title="Home")
    elif request.method == "GET":
        return render_template("index.html", current_user=current_user, title="Home")
    else:
        return render_template("index.html", current_user=current_user, title="Home")

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
        session["current_user"] = user
        # send to index
        return redirect(url_for('index'))
    else:
        return render_template("index.html", title="Home", error_msg="Passwords don't match")


@app.route("/login", methods=["POST"])
def login():
    # get data from form
    # validate
    # lookup in db
    # send to index
    return redirect(url_for('index'))
