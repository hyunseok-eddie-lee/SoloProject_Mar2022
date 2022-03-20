from flask import render_template,redirect,session,request,flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.item import Item
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():

    if not User.validate_register(request.form):
        return redirect('/')
    data ={
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password']),
        "gender": request.form['gender'],
        "birth" : request.form['birth'],
        "city" : request.form['city'],
        "state" : request.form['state']
    }
    id = User.save(data)
    session['user_id'] = id

    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password", "login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("dashboard.html", user=User.get_by_id(data), items=Item.get_all())

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



@app.route('/edit/account/<int:id>')
def edit_account(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        "id": id
    }
    user_data ={
        "id": session['user_id']
    }
    return render_template("edit_account.html", edit=User.get_one(data), user=User.get_by_id(user_data))

@app.route('/update/account', methods=['POST'])
def update_account():
    if 'user_id' not in session:
        return redirect('/logout')
    if not User.validate_update(request.form):
        return redirect('/dashboard')
    data ={
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "gender": request.form['gender'],
        "birth" : request.form['birth'],
        "city" : request.form['city'],
        "state" : request.form['state'],
        "id": request.form["id"]
    }
    User.update(data)
    return redirect('/dashboard')