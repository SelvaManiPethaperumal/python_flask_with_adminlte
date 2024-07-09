from flask import Flask, request,jsonify, g, session
from config import Config
from datetime import timedelta

app = Flask(__name__)
app.config.from_object(Config)

app.secret_key =  app.config['SECRET_KEY']  # Necessary for session management
app.permanent_session_lifetime = timedelta(minutes=1200)  # Set session timeout to 5 minutes

ADMIN_EMAIL = app.config['ADMIN_EMAIL']
ADMIN_PASSWORD= app.config['ADMIN_PASSWORD']

class Authentication:

    """
    Function to authentication the user
    @param  Json
    @return  Json
    """
    @staticmethod
    def authentication():
        try:
            param = request.json 
            if param['email'] != ADMIN_EMAIL :
                 return jsonify({'status': "failed", 'url':'' , 'message' : "Email is not register"}), 200
            if param['password'] != ADMIN_PASSWORD :
                 return jsonify({'status': "failed", 'url':'' , 'message' : "Invalid Password"}), 200
            Authentication.SetSession()
            base_url = request.host_url
            return jsonify({'status': "success", 'url':base_url +'dashboard' , 'message' : "Login Successfully"}), 200
        except ValueError as e:
             return jsonify({'status': "failed", 'url':'' , 'message' : e}), 200
        
    """
    Function to set value session
    @param  void
    @return  void
    """
    @staticmethod
    def SetSession():
        session.permanent = True  # Make the session permanent
        session['ai_chat_bot_username'] = app.config['ADMIN_EMAIL']

    """
    Function to logout
    @param  void
    @return  Json
    """
    @staticmethod
    def logout():
        session.pop('ai_chat_bot_username', None)
        base_url = request.host_url
        return jsonify({'status': "success", 'url':base_url , 'message' : "Logout Successfully"}), 200