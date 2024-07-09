# app/routes.py
from flask import Blueprint, render_template, send_from_directory, abort,session
from app.modules.Authentication import Authentication 
from app.modules.Dashbaord import Dashbaord 
import os



url = Blueprint('url', __name__)

@url.route('/')
def home():
    if 'ai_chat_bot_username' in session:
        return render_template('dashboard.html')
    return render_template('login.html')

@url.route("/authentication", methods = ['POST'])
def upload( ):
    return Authentication.authentication()

@url.route("/out", methods = ['POST'])
def logout( ):
    return Authentication.logout()

@url.route("/dashboard", methods = ['GET'])
def show( ):
    return Dashbaord.show()

@url.route("/get_data", methods = ['POST'])
def get_data( ):
    return Dashbaord.getData()

@url.route("/download", methods = ['GET'])
def download( ):
    return Dashbaord.downloadReport()