from app import app
from flask_sqlalchemy import SQLAlchemy
from os import path, getcwd

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + \
    path.join(getcwd(), 'database.db')
db = SQLAlchemy(app)
