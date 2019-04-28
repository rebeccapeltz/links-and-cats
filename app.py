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
    error_msg = request.args.get("error_msg")
    success_msg = request.args.get("success_msg")
    current_user = None
    # logged in or not, return all public links
    public_links = Link.query.filter_by(public=True).all()
    private_links = None

    if 'current_user' in session:
        current_user = session["current_user"]
        private_links = Link.query.filter_by(
            public=False, user_id=current_user.id).all()

    if error_msg:
        return render_template("index.html", private_links=private_links, public_links=public_links, title="Home", error_msg=error_msg)
    elif success_msg:
        return render_template("index.html", private_links=private_links, public_links=public_links, title="Home", success_msg=success_msg)
    else:
        return render_template("index.html", private_links=private_links, public_links=public_links, title="Home")


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
    validation_result = validate_user(email_input, firstname_input, lastname_input, password_input, confirm_password_input)
    if len(validation_result) == 0:
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
        return redirect(url_for('index', success_msg="Successful user registration."))
    else:
        return redirect(url_for('index', error_msg=validation_result))

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
    default_entry = {"public": True, "url": "http://www.example.com",
                     "title": "Example", "description": "Description", "categories": "JavaScript"}
    # print(default_entry)
    return render_template("form.html", categories=categories, default_entry=default_entry)


def add_link_and_categories(user_id, url, title, description, categories, public):
    link = Link(user_id=user_id, url=url, title=title,
                description=description, public=public)
    # create a list of cat objects from categories
    cat_list = []
    for cat in categories:
        cat_obj = Category.query.filter_by(description=cat).first()
        cat_list.append(cat_obj)
    link.add_categories(cat_list)
    db.session.add(link)
    db.session.commit()


def update_link_and_categories(link_id, user_id, url, title, description, categories, public):
    link = Link.query.filter_by(id=link_id).first()
    link.title = title
    link.description = description
    link.url = url

    # create a list of cat objects from categories
    cat_list = []
    for cat in categories:
        cat_obj = Category.query.filter_by(description=cat).first()
        cat_list.append(cat_obj)
    link.update_categories(cat_list)
    db.session.add(link)
    db.session.commit()

# ADD LINK: add a new link
@app.route("/add_link", methods=["GET", "POST"])
def add_link():
    user_id = None
    if 'current_user' in session:
        current_user = session["current_user"]
        user_id = current_user.id
    # get out if not logged in
    if user_id is None:
        return redirect(url_for('index', error_msg="Error: Can't add link unless logged in."))

    categories = Category.query.all()
    # default_entry = {}
    default_entry = {"public": True, "url": "http://www.example.com",
                     "title": "Example", "description": "Description", "categories": "JavaScript"}
    # if GET
    if request.method == "GET":
        # get a list of categories
        categories = Category.query.all()
        # print(categories)
        # call form with categories
        return render_template("form.html", categories=categories, default_entry=default_entry)
    elif request.method == "POST":
        public = True  # default
        # get data from form
        pubpriv_input = request.form.get("pubpriv-input")
        if pubpriv_input == "private":
            public = False
        url_input = request.form.get("url-input")
        title_input = request.form.get("title-input")
        description_input = request.form.get("description-input")
        category_input = request.form.getlist("category-input")
        print("cat input", category_input)
        print(user_id, url_input, title_input,
              description_input, category_input, public)

        # add link and categories
        add_link_and_categories(
            user_id, url_input, title_input, description_input, category_input, public)
        # go back to index with success message
        return redirect(url_for('index', success_msg="Success: Link successfully added."))

# UPDATE LINK: update an existing link
@app.route("/update_link/<string:link_id>", methods=["GET"])
def update_link(link_id):
    user_id = None
    if 'current_user' in session:
        current_user = session["current_user"]
        user_id = current_user.id
    # get out if not logged in
    if user_id is None:
        return redirect(url_for('index', error_msg="Error: Can't update link unless logged in."))

    # get categories
    categories = Category.query.all()

    # get current data using link_id
    link = Link.query.filter_by(id=link_id).first()
    # get a list of string categories in the link
    cat_str_list=[]
    for cat in link.categories:
        cat_str_list.append(cat.description)

    default_entry = {"link_id": link_id, "public": link.public, "url": link.url,
                     "title": link.title, "description": link.description, "categories": cat_str_list}
    return render_template("form.html", categories=categories, default_entry=default_entry)
    
       
@app.route("/process_update_link", methods=["POST"])
def process_update_link():
    user_id = None
    if 'current_user' in session:
        current_user = session["current_user"]
        user_id = current_user.id

    # get out if not logged in
    if user_id is None:
        return redirect(url_for('index', error_msg="Error: Can't update link unless logged in."))

    # print("process update")
    # get data from form
    public = True  # default
    # get data from form
    pubpriv_input = request.form.get("pubpriv-input")
    if pubpriv_input == "private":
        public = False
    link_id = request.form.get("link-id")
    url_input = request.form.get("url-input")
    title_input = request.form.get("title-input")
    description_input = request.form.get("description-input")
    category_input = request.form.getlist("category-input")
    print(link_id,user_id, url_input, title_input,
              description_input, category_input, public)

    update_link_and_categories(link_id,user_id,url_input,title_input, description_input, category_input, public)
    return redirect(url_for('index', success_msg="Success: Link successfully updated."))


# DELETE LINK delete an existing link
@app.route("/delete_link/<string:link_id>", methods=["POST"])
def delete_link(link_id):
    user_id = None
    if 'current_user' in session:
        current_user = session["current_user"]
        user_id = current_user.id

    # get out if not logged in
    if user_id is None:
        return redirect(url_for('index', error_msg="Error: Can't update link unless logged in."))

    link = Link.query.get(link_id)
    db.session.delete(link)
    db.session.commit()
    # go to home with success message
    return redirect(url_for('index', success_msg="Success: Link successfully deleted."))

# add, delete categories

def checkForDuplicateCat(new_cat):
    is_duplicate = False
    categories = Category.query.all()
    for cat in categories:
        if new_cat == cat.description:
            is_duplicate = True
            break
    # print(new_cat)
    return is_duplicate

# ADD new category
@app.route("/delete_category", methods=["POST"])
def delete_category():
    desc_input = request.form.get("desc-input") 
    del_cat = Category.query.filter_by(description=desc_input).first()
    # remove this category from all link category collections
    links = del_cat.link_category
    for link in links:
        link.remove_category(del_cat)
    db.session.delete(del_cat)
    db.session.commit()
    categories = Category.query.all()
    return redirect(url_for('manage_categories',categories=categories, success_msg="Category deleted."))


# ADD new category
@app.route("/add_category", methods=["POST"])
def add_category():
    desc_input = request.form.get("desc-input") #add
    # check for duplicate
    if checkForDuplicateCat(desc_input):
        categories = Category.query.all()
        return redirect(url_for('manage_categories',categories=categories, error_msg="Duplicate categories not allowed."))

    new_cat = Category(description=desc_input)
    db.session.add(new_cat)
    db.session.commit()
    categories = Category.query.all()
    return redirect(url_for('manage_categories',categories=categories, success_msg="Category updated."))


# UPDATE a category
@app.route("/update_category", methods=["POST"])
def update_category():
    desc_input_orig = request.form.get("desc-input-orig") #update
    desc_input_new = request.form.get("desc-input-new") #update

    print(desc_input_orig, desc_input_new)
    orig_cat = Category.query.filter_by(description=desc_input_orig).first()
    #check for duplicate
    categories = Category.query.all()
    if checkForDuplicateCat(desc_input_new):
        return redirect(url_for('manage_categories',categories=categories, error_msg="Cannot rename a category to one that exists."))

    if len(desc_input_new) == 0: #error
        return redirect(url_for('manage_categories',categories=categories, error_msg="Category must have at least 1 character to update."))
    else:
        orig_cat.description = desc_input_new
        db.session.commit() 
        categories = Category.query.all() #get updated list
        return redirect(url_for('manage_categories',categories=categories, success_msg="Category updated."))

# READ and display all categories to be managed
@app.route("/manage_categories", methods=["GET"])
def manage_categories():
    # get categories
    categories = Category.query.all()
    return render_template("categories.html", categories=categories)