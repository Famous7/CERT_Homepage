import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'famous'
    SQLALCHEMY_DATABASE_URI = os.getenv('CERT_DATABASE_URL') or 'mysql://<user>:<password>@<host>/<db>?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
