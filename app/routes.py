from flask_login import current_user, login_user
from app.models import User
from app.forms import LoginForm, SignupForm
from app import app
from flask import render_template, flash, redirect, url_for, request
from flask_login import logout_user


@app.route('/')
def index(): 
    return render_template('base.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    loginform = LoginForm()
    signupform = SignupForm()
    if request.method == 'GET':
        return render_template('login.html', title='Sign In', loginform=loginform, signupform=signupform)
    if request.method == 'POST':
        if loginform.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
        return render_template('login.html', title='Sign In', loginform=loginform, signupform=signupform)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))