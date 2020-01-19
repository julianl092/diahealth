from flask_login import current_user, login_user
from app.models import User, ModifiedQuestion
from app.forms import LoginForm, SignupForm
from app import app, db, admin
from flask import render_template, flash, redirect, url_for, request
from flask_login import logout_user
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import desc


class SecuredModelView(ModelView):
    
    can_export = True

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

admin.add_view(SecuredModelView(ModifiedQuestion, db.session))

@app.route('/', defaults={'show': 20})
@app.route("/<int:show>")
def index(show): 
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else: 
        questions = db.session.query(ModifiedQuestion).order_by(desc(ModifiedQuestion.likes)).limit(show)
        return render_template('index.html', questions=questions)


@app.route('/register', methods=['POST'])
def register():
    signupform = SignupForm()
    if signupform.validate_on_submit(): 
        print("SignupForm")
        user = User.query.filter_by(email=signupform.email.data).first()
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