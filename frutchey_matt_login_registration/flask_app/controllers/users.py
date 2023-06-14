from flask_app import app
from flask import render_template, session, redirect, request, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.user import User

# App Routes Go Below:

# Home Page & User Dashboard
@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def welcome_page():
    if 'user_id' not in session:
        return render_template("index.html")
    return render_template("welcome.html")

# Create 
@app.route("/create/user", methods = ["POST", "GET"])
def new_user():
    if request.method == "POST":
        if not User.validate(request.form):
            return redirect("/")
    pw_hashed = bcrypt.generate_password_hash(request.form['password'])
    # print(pw_hashed)  #? Test - Success
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hashed  #? request.form['password'] -- Used to test before implementing bcrypt
    }
    id = User.create_user(data)
    session['user_id'] = id
    session['name'] = request.form['first_name']
    return redirect("/dashboard")

# Read
@app.route('/login', methods = ['POST'])    #? Tried to make this 'skinnier'
def login():
    data = {
        'email': request.form['email']
    }
    valid_user = User.get_user_by_email(data)
    if not valid_user:
        flash("Incorrect Email or Password.", category='login')
        return redirect("/")
    if not bcrypt.check_password_hash(valid_user.password, request.form['password']):
        flash("Incorrect Email or Password.", category='login')
        return redirect("/")
    session['user_id'] = valid_user.id          #! Note for future study: Really get down where this comes from and follow the trail
    session['name'] = valid_user.first_name
    return redirect("/dashboard")

# Update
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")