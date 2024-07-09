from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_object(Config)

# db = SQLAlchemy()
db = SQLAlchemy(app, session_options = { 'autoflush': True, 'expire_on_commit': True })