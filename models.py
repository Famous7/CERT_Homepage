from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from app import login, db
from sqlalchemy.dialects.mysql import ENUM, TINYINT
from sqlalchemy.sql import func


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    __tablename__ ="user_tbl"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(12), index=True, unique=True)
    user_pw = db.Column(db.String(94))
    user_email = db.Column(db.String(120), unique=True)
    user_name = db.Column(db.String(64))
    user_profile_path = db.Column(db.String(255), nullable=True)
    user_department = db.Column(db.String(64))
    user_grade = db.Column(TINYINT(4, unsigned=True, zerofill=True))
    user_gender = db.Column(ENUM('M', 'F'), default='M')
    user_membership = db.Column(ENUM('N', 'A'), default='N')
    user_registration_date = db.Column(db.DATETIME, default=func.now())

    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.user_pw = generate_password_hash(kwargs.get('user_pw'))
        self.user_name = kwargs.get('user_name')
        self.user_email = kwargs.get('user_email')
        self.user_profile_path = kwargs.get('user_profile_path')
        self.user_department = kwargs.get('user_department')
        self.user_grade = kwargs.get('user_grade')
        self.user_gender = kwargs.get('user_gender')

    def __repr__(self):
        return '<USER {}>'.format(self.user_id)

    def set_user_pw(self, password):
        self.user_pw = generate_password_hash(password)

    def check_user_pw(self, password):
        return check_password_hash(self.user_pw, password)
