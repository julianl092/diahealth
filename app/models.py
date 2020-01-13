from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    babyname = db.Column(db.String(64))
    babybirth = db.Column(db.Date)
 
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def __repr__(self):
        return '<User {}>'.format(self.username)    

class RawQuestion(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text)
    created_on = db.Column(db.DateTime, default=db.func.now())
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('modifiedquestion.id'), primary_key=True)
)

class ModifiedQuestion(RawQuestion): 
    __tablename__ = 'modifiedquestion'
    likes = db.Column(db.Integer)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
        backref=db.backref('modifiedquestion', lazy=True))

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))



@login.user_loader
def load_user(id):
    return User.query.get(int(id))