from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.secret_key = '^%^&%^(*^^^&&*^(*^^&$%&*&*%^&$&^'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/manage_student?charset=utf8mb4" % quote("Sinhhung1212@")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)
login = LoginManager(app)
