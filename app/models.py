from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.declarative import declared_attr


likes = db.Table('likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('question_id', db.Integer, db.ForeignKey('modifiedquestion.id')), 
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    babyname = db.Column(db.String(64), nullable=True)
    babybirth = db.Column(db.Date, nullable=True)
    admin = db.Column(db.Boolean, default=False)

    @property
    def is_admin(self):
        return self.admin

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def __repr__(self):
        return '<User {}>'.format(self.firstname, self.lastname)    

class Question(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text)
    created_on = db.Column(db.DateTime, default=db.func.now())
    user_email = db.Column(db.String(120), index=True)
    @declared_attr
    def created_by(cls):
        return db.Column(db.Integer, db.ForeignKey(User.id))
    type = db.Column(db.String(20))
    _mapper_args__ = {
        'polymorphic_on':type
    }

class RawQuestion(Question):
    __tablename__ = "rawquestion"
    _mapper_args__ = {
        'polymorphic_identity': 'raw'
    }
    

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('question_id', db.Integer, db.ForeignKey('modifiedquestion.id')), 
)

links = db.Table('links',
    db.Column('link_id', db.Integer, db.ForeignKey('link.id')),
    db.Column('question_id', db.Integer, db.ForeignKey('modifiedquestion.id')), 
)

class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

class Link(db.Model):
    __tablename__ = 'link'
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.Text)

class ModifiedQuestion(Question): 
    __tablename__ = 'modifiedquestion'
    answer = db.Column(db.Text)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
        backref=db.backref('modifiedquestion', lazy=True))

    links = db.relationship('Link', secondary=links, lazy='subquery',
    backref=db.backref('modifiedquestion', lazy=True))

    likes = db.relationship('User', secondary=likes, 
        backref=db.backref('modifiedquestion', lazy='dynamic'))

    _mapper_args__ = {
        'polymorphic_identity': 'modified'
    }

    

@login.user_loader
def load_user(id):
    return User.query.get(int(id))