from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__, template_folder="templates")
app.secret_key = 'kurswork from KPO 2023'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///abiturlist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
manager = LoginManager(app)

from web_app import models, views, db_auto_add

app.app_context().push()

db.create_all()