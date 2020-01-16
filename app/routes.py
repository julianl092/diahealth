from flask_login import current_user, login_user
from app.models import User
from app.forms import LoginForm, SignupForm
from app import app, db
from flask import render_template, flash, redirect, url_for, request
from flask_login import logout_user


@app.route('/')
def index(): 
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else: 
        return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    signupform = SignupForm()
    if signupform.validate_on_submit(): 
        print("SignupForm")
        user = User.query.filter_by(email=signupform.emailh.data).first()
        if user is not None: 
            flash('Email already taken')
            return redirect(url_for('login'))
        newuser = User(firstname=signupform.firstname.data, lastname=signupform.lastname.data, email=signupform.email.data)
        newuser.set_password(signupform.password.data)
        db.session.add(newuser)
        db.session.commit()
        flash('Registration Completed')
        return redirect(url_for('index'))
    else: 
        return render_template('login.html', title='Sign In', loginform=loginform, signupform=signupform)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    loginform = LoginForm()
    signupform = SignupForm()
    if request.method == 'GET':
        return render_template('login.html', title='Sign In', loginform=loginform, signupform=signupform)
    elif request.method == 'POST':
        if loginform.validate_on_submit():
            print("LoginForm")
            user = User.query.filter_by(email=loginform.email.data).first()
            if user is None or not user.check_password(loginform.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))
            login_user(user, remember=loginform.remember_me.data)
            return redirect(url_for('index'))
        else: 
            return render_template('login.html', title='Sign In', loginform=loginform, signupform=signupform)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    loginform = LoginForm()
    signupform = SignupForm()
    if request.method == 'GET':
        return render_template('login.html', title='Sign In', loginform=loginform, signupform=signupform)
    elif request.method == 'POST':
        if loginform.validate_on_submit():
            print("LoginForm")
            user = User.query.filter_by(email=loginform.email.data).first()
            if user is None or not user.check_password(loginform.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))
            login_user(user, remember=loginform.remember_me.data)
            return redirect(url_for('index'))
        else: 
            return render_template('login.html', title='Sign In', loginform=loginform, signupform=signupform)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))