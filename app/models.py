from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from app import login, db
from sqlalchemy.dialects.mysql import ENUM, TINYINT
from sqlalchemy.sql import func
from hashlib import md5
from datetime import datetime


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    __tablename__ ="user_tbl"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(12), index=True, unique=True)
    user_pw = db.Column(db.String(94))
    user_email = db.Column(db.String(120), unique=True)
    user_name = db.Column(db.String(64))
    user_department = db.Column(db.String(64))
    user_grade = db.Column(TINYINT(4, unsigned=True, zerofill=True))
    user_gender = db.Column(ENUM('M', 'F'), default='M')
    user_membership = db.Column(ENUM('N', 'A'), default='N')
    user_registration_date = db.Column(db.DATETIME, default=func.now())
    user_about_me = db.Column(db.String(140))
    user_last_sign_in = db.Column(db.DateTime, default=datetime.utcnow())
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.user_pw = generate_password_hash(kwargs.get('user_pw'))
        self.user_name = kwargs.get('user_name')
        self.user_email = kwargs.get('user_email')
        self.user_department = kwargs.get('user_department')
        self.user_grade = kwargs.get('user_grade')
        self.user_gender = kwargs.get('user_gender')

    def __repr__(self):
        return '<USER {}>'.format(self.user_id)

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}

    def set_user_pw(self, password):
        self.user_pw = generate_password_hash(password)

    def check_user_pw(self, password):
        return check_password_hash(self.user_pw, password)

    def avatar(self, size):
        digest = md5(self.user_email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{0}?d=identicon&s={1}'.format(digest, size)


class Post(db.Model):
    __tablename__ = "post_tbl"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(128))
    post_image = db.Column(db.String(100))
    post_written_date = db.Column(db.DATETIME, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user_tbl.id'))

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.post_title = kwargs.get('post_title')
        self.post_image = kwargs.get('post_image')

    def __repr__(self):
        return f"<POST('{self.id}', '{self.post_title}', '{self.post_image}')>"

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}

