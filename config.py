import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgres://zbgapnhtldbccx:81d89132f4e31364af1aac9a18e4cdcc8d994d1e9edf969fd9ac6f29fccdd722@ec2-3-224-165-85.compute-1.amazonaws.com:5432/de3l8o743le5nn'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
