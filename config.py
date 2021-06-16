# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from   decouple import config

class Config(object):

    basedir    = os.path.abspath(os.path.dirname(__file__))

    # Set up the App SECRET_KEY
    SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_007')

    # Set up the App Mail config
    MAIL_SERVER = ''
    MAIL_PORT = 587
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    #
    #  This will create a file in <app> FOLDER    #
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')    #SQLALCHEMY_TRACK_MODIFICATIONS = True
    #SQLALCHEMY_DATABASE_URI = "mysql+pymysql://$(CLEARDB_DATABASE_URL)/pretux"
    SQLALCHEMY_DATABASE_URI = ""
    #SQLALCHEMY_DATABASE_URI = ""
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class ProductionConfig(object):
    
    basedir    = os.path.abspath(os.path.dirname(__file__))

    # Set up the App SECRET_KEY
    SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_007')

    # Set up the App Mail config
    MAIL_SERVER = ''
    MAIL_PORT = 587
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    #
    #  This will create a file in <app> FOLDER    #
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')    #SQLALCHEMY_TRACK_MODIFICATIONS = True
    #SQLALCHEMY_DATABASE_URI = ""
    SQLALCHEMY_DATABASE_URI = ""
    #SQLALCHEMY_DATABASE_URI = ""
    SQLALCHEMY_TRACK_MODIFICATIONS = True

# class ProductionConfig(Config):
#     DEBUG = False
#     SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_007')
#     # Security
#     SESSION_COOKIE_HTTPONLY  = True
#     REMEMBER_COOKIE_HTTPONLY = True
#     REMEMBER_COOKIE_DURATION = 3600

#     MAIL_SERVER = ''
#     MAIL_PORT = 587
#     MAIL_USERNAME = ''
#     MAIL_PASSWORD = ''
#     MAIL_USE_TLS = True
#     MAIL_USE_SSL = False


#     # PostgreSQL database
#     SQLALCHEMY_TRACK_MODIFICATIONS = True
#     SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
#         config( 'DB_ENGINE'   , default='postgresql'    ),
#         config( 'DB_USERNAME' , default='postgres'       ),
#         config( 'DB_PASS'     , default='mysecretpassword'),
#         config( 'DB_HOST'     , default='localhost'     ),
#         config( 'DB_PORT'     , default=5432            ),
#         config( 'DB_NAME'     , default='pretux' )
#     )

class DebugConfig(Config):
    DEBUG = True

# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug'     : DebugConfig
}
