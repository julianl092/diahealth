from flask_login import current_user, login_user
from app import app, db, admin
from app.models import User, ModifiedQuestion, likes, Tag, RawQuestion
from app.forms import LoginForm, SignupForm, QuestionForm
from flask import render_template, flash, redirect, url_for, request
from flask_login import logout_user
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import desc, func


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
admin.add_view(SecuredModelView(RawQuestion, db.session))


@app.route('/', defaults={'show': 10})
@app.route("/<int:show>")
def index(show): 
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else: 
        questionform = QuestionForm()
        questions = db.session.query(ModifiedQuestion, func.count(likes.c.user_id).label('total')).join(likes).group_by(ModifiedQuestion).all()
        if len(questions) < show:
            rem_questions = db.session.query(ModifiedQuestion).filter(~ModifiedQuestion.likes.any()).limit(show - len(questions)).all()
        else:
            rem_questions = []
        tags = db.session.query(Tag).all()
        l1 = tags[:len(tags) // 2]
        if len(tags) % 2 == 1: 
            l1.append(" ")
        l2 = tags[len(tags) // 2:]
        zipped = zip(l1, l2)
        return render_template('index.html', questions=questions, rem_questions=rem_questions, questionform=questionform, user=current_user, zipped=zipped)

@app.route("/category/<int:cid>")
def category(cid): 
    questions = db.session.query(ModifiedQuestion, func.count(likes.c.user_id).label('total')).filter(ModifiedQuestion.tags.any(Tag.id == cid)).join(likes).group_by(ModifiedQuestion).all()
    return render_template('category.html', user=current_user, questions=questions)

@app.route('/like', methods=['POST'])
def like():
    qid = request.form['id']
    question = db.session.query(ModifiedQuestion).filter_by(id=qid).first()
    mod = int(request.form['likes'])
    if mod == 1 and current_user not in question.likes:
        question.likes.append(current_user)
    elif current_user in question.likes:
        question.likes.remove(current_user)
    db.session.commit()
    return ('', 200)

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
            print(user)
            if user is None or not user.check_password(loginform.password.data):
                flash('Invalid username or password')
                print("Invalid password")
                return redirect(url_for('login'))
            login_user(user, remember=loginform.remember_me.data)
            return redirect(url_for('index'))
        else: 
            return render_template('login.html', title='Sign In', loginform=loginform, signupform=signupform)

@app.route('/submitquestion', methods=['POST'])
def submitquestion():
    questionform = QuestionForm() 
    if questionform.validate_on_submit(): 
        text = questionform.question.data
        raw = RawQuestion(question_text=text, created_by=current_user.id, user_email=current_user.email)
        db.session.add(raw)
        db.session.commit()
        return redirect(url_for("index"))
    
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
