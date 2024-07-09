# config.py
import os

class Config:
    SECRET_KEY = os.urandom(24)
    DEBUG = True
    ADMIN_EMAIL="admin@selvamani.com"
    ADMIN_PASSWORD="ChatBot@0507"
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    
