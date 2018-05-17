__author__ = 'Guo'
from os import path

class Config(object):
    SECRET_KEY = 'this is blank guo'
    pass


class prodConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://blank:Guo1006575211@47.94.223.220:3306/lvyou'
